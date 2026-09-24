# Architecture decisions

Thirteen decisions that changed the system, in the order they were made.

Each is written the same way: what was there, what broke, what replaced it,
what it measured afterwards, and what it cost. Decisions that earned nothing
are included and marked, because a record that only contains wins is a
brochure.

Where a number depends on where the code is running, the entry says which
environment. **local** is docker compose in `full` mode; **preprod** is one
Render instance at 0.5 CPU and 512 MB, in `portfolio` mode, on Neon and Groq's
free tier; **production** is ECS Fargate in `full` mode, on RDS, with a Redis
sidecar. Most tight numbers here are preprod numbers, because preprod is the
constrained deployment and the one the public can reach.

The system ships in two deployment modes. `portfolio` is the public demo: one
unauthenticated query route and health. `full` mounts the other nine routers
behind a login — admin, SQL, vector, ingestion, evaluation, escalation, claim
and security (`main.py:161`). Most of what follows runs in both, and says
nothing about mode. A **Mode** line appears only where the decision does *not*
apply everywhere, and it is the first thing to check before quoting one of
these numbers.

---

## 1. HNSW rather than IVFFlat for the vector index

**Was.** No index at all. Vector search ordered by `embedding <=> query`, so
every question sequentially scanned `document_chunks`.

**Problem.** Nothing, yet. At 327 rows a sequential scan is 2.674 ms and
Postgres will keep choosing it over any index. The problem is the corpus that
does not fit in memory, not the one that does.

**Change.** An HNSW index with `vector_cosine_ops`. IVFFlat needs training
data to build its lists and degrades as the corpus grows past what it was
built against, so it needs rebuilding as documents arrive. HNSW does not.

**Result.** *Nothing measurable.* Retrieval is unchanged, benchmark scores are
unchanged, and `EXPLAIN` still shows `Seq Scan on document_chunks`. The
planner will start choosing the index somewhere in the tens of thousands of
rows.

**Cost.** HNSW is approximate, so at a corpus size where it is actually used,
retrieval can return a different set than an exact scan would — which matters
for a benchmark that grades retrieval. `ef_search` is left at its default;
raising it recovers recall at the cost of latency, and neither is worth tuning
against 327 rows. The index was also built without `CONCURRENTLY`, which is
fine at this size and wrong at the size that makes the index matter.

> The operator class is the trap worth naming: an index built for a different
> operator than the query uses is never chosen, silently. Nothing errors. The
> scan just stays sequential.

`alembic/versions/ed2de6d3b0f7_add_hnsw_index_on_document_chunk_.py`

---

## 2. Router absence as the security control

**Was.** One application with role checks on each endpoint, and a UI that hid
the controls a role could not use.

**Problem.** Hiding a UI route is not protecting an API endpoint. A public
demo that ships 39 routes and relies on every one of them checking a role
correctly has 39 chances to be wrong.

**Change.** Two deployment modes. In `portfolio` mode the admin, SQL, vector,
ingestion, evaluation, escalation, claim and security routers are never
mounted — `main.py:161` puts them inside `if mode == "full":`. The public demo
serves 3 routes, not 39 with guards.

**Result.** The attack surface is the router list, which is one file and
reviewable in a minute. A missing role check on an unmounted route cannot be
exploited because the route returns 404 from the framework, before any of my
code runs.

**Cost.** Two configurations to keep working, and a class of bug where a
feature works locally in full mode and 404s in the demo. It has bitten twice.

*Escalations are written where they cannot be read.* `record_escalation` runs
on every query at `financial_routes.py:242`, but `escalation_router` is
full-mode only — so the public demo files rows with no route to retrieve them.

*Reciprocal rank fusion is unreachable in `portfolio`, and nothing says so.*
There are two BM25 stages, and the distinction matters. `bm25_rerank` reorders
what pgvector already returned, and runs in every mode. `search_chunks_lexical`
ranks the whole corpus independently — the point being that RRF needs lists
that can *disagree*, and a rerank of the dense result cannot surface anything
dense retrieval missed. That second stage runs only inside `if rrf_enabled:`
(`vector_search.py:245`), and the flag comes from
`config["configurable"]["retrieval_flags"]`, set in exactly one place —
`evaluation_routes.py:638` — in a router mounted in `full` only.

That second one is the more instructive failure, because nothing is broken.
The flag defaults to off, absence means off, and every test passes. It is a
scoping decision — hybrid retrieval is an *evaluated* capability, not a
*serving* one — that was never written down, and so read as a claim about what
the demo does. Mounting by mode makes the security boundary auditable in one
file; it also makes capability boundaries invisible unless they are documented
deliberately. This file exists partly because of that.

---

## 3. Three model tiers instead of one model

**Was.** One model for every call in the graph.

**Problem.** Intent classification and keyword extraction are cheap
classification tasks. Analysis and review are not. Paying the large model's
price and latency for "is this a valuation question?" is most of the cost of a
query for none of its quality.

**Change.** `LLMTier.SMALL` for intent and keywords, `MEDIUM` for the planner,
SQL generation and reranking, `LARGE` for analysis and review. Temperature
zero throughout; OpenAI for embeddings, Groq for generation.

**Result.** Six LLM calls per query where the expensive tier runs twice.

**Cost.** Groq's small tier does not honour structured output on this prompt.
Keyword generation asks for a tool call, the model returns the list as content,
and Groq rejects its own response with `400 tool_use_failed`. The exception was
caught and `[]` returned, `bm25_rerank` took its `if not rows or not keywords`
branch, and the demo served the pgvector order untouched — logging
`[BM25] No rows or keywords — skipping rerank` and nothing else.

**Fixed, and the measurement is the point.** Four plausible fixes were tried
first, five serial attempts each on `gpt-oss-20b` at temperature zero:

| Attempt | Result |
|---|---|
| Bare schema (as shipped) | 0/5 |
| Docstring + `Field(description=...)` | 0/5, later 2/5 — flaky, not fixed |
| Escalate to MEDIUM (`gpt-oss-120b`) | 0/5 |
| Rewrite the prompt's array-shaped examples | 0/5 |

None of them work, and the rejection says why: `failed_generation` contains
`'["revenue growth", "year over year", ...]'` — the right answer, every time,
emitted as content. The problem was never the model's ability or the tier. So
the fix is not to make the tool call succeed; it is to keep the answer already
generated. Structured output stays primary, because it works natively on the
providers `full` mode uses; on `tool_use_failed` the keywords are recovered
from the rejection body.

    structured output alone          2/5
    structured output + recovery     5/5

No extra call and no added latency. A second plain invocation parsed as JSON
also measured 5/5 and is the documented fallback if Groq stops returning
`failed_generation`.

**Also fixed, and unrelated.** `generate_ranking_keywords` and
`extract_filters` both called `.invoke()` synchronously inside `async`
functions, holding the event loop for a full LLM round trip. On a single-CPU
preprod instance that is every concurrent request waiting on one. Both now `await
ainvoke`.

**Mode.** The failure is Groq-specific, and Groq serves the preprod demo only —
the provider is database configuration, and `full` runs a different one. So
this degrades `portfolio` and leaves benchmark runs intact. Worth stating
because the opposite conclusion is the tempting one: a provider chosen for one
deployment carries a capability difference into that deployment alone, and
nothing in the code marks the boundary.

**Kept deliberately.** The `except` stays broad and stays fail-open. An empty
keyword list degrades retrieval to dense-only; it must not fail the query.
What was wrong was that it was silent, not that it caught — recovery now
logs `Provider rejected its own tool call; recovered N keywords from the
payload`, which says exactly what happened.

---

## 4. Redis as a task sidecar, not a managed cluster

**Was.** Nothing. Cache and rate limiting were in-process dictionaries.

**Problem.** In-process state is wrong the moment there is more than one
process, and ElastiCache is a monthly bill and a subnet group for a portfolio
project.

**Mode.** `full` only, and only on ECS. The Render preprod instance runs
`portfolio` with no Redis at all — the query rate limiter there fails open,
which is why the public demo still has no concurrency bound.

**Change.** A `redis:7-alpine` container in the same ECS task definition,
reached at `redis://localhost:6379/0`.

**Result.** Cache and rate limiting work, cost nothing, and disappear with the
task.

**Cost.** Stated plainly because it is the question an interviewer should ask:
**this does not scale horizontally.** Two tasks means two caches and two
independent rate limiters, so the per-IP limit becomes per-IP-per-task. At
`desired_count = 1` it is correct. At two it is quietly wrong. Moving to
ElastiCache is a URL change and a security group, which is why the sidecar was
acceptable — the migration is cheap and the decision is reversible.

---

## 5. A frozen corpus snapshot for the benchmark

**Was.** The benchmark ran against live data.

**Mode.** `full` only. `evaluation_router` is not mounted in `portfolio`, so
no benchmark or evaluation figure quoted here is reproducible from the public
demo.

**Problem.** Correct results were graded incorrect between runs. Market data
changed ranking membership underneath the benchmark, so a code regression and
data drift produced the same symptom and were indistinguishable.

**Change.** The corpus and its embeddings are frozen into a snapshot the
benchmark restores before running.

**Result.** Reruns became comparable — which is the precondition for every
number in the evaluation work, and specifically what made the LLM-judge noise
floor measurable at 0.04.

**Cost.** The benchmark now measures the system against a fixed past, so
retrieval quality on genuinely new documents is not covered by it.

---

## 6. Stopped tuning against RAGAS

**Was.** RAGAS faithfulness and relevancy as the optimisation target.

**Mode.** `full` only, as above.

**Problem.** Three separate edit-and-measure cycles produced score movements
that all landed inside judge variance. The metric was not measuring my
changes; it was measuring the judge.

**Change.** Established the noise floor first — 0.04 — and stopped treating
movements below it as signal. RAGAS is still reported. It is no longer steered
by.

**Result.** No more work spent chasing noise. Two known artefacts documented
rather than chased: a recurring 0.9375 and a `response_relevancy` zero.

**Cost.** Losing a headline number that moves. The honest version of that
number does not move, and saying so is the point.

> RAGAS also covers only 40 of the 100 golden questions — faithfulness
> averages the sentiment and mixed sets only. The denominator varies by
> question set, which is worth stating whenever the figure is quoted.

---

## 7. A serialised lock, not a token bucket, for SEC EDGAR

**Was.** Unthrottled requests.

**Mode.** `full` only. `ingestion_router` is admin-gated *and* unmounted in
`portfolio`, so nothing in the public demo can reach SEC. Every EDGAR request
originates from an authenticated admin clicking in the ingestion screen —
there is no scheduler, no cron and no EventBridge rule.

**Problem.** SEC publishes a rate limit and blocks addresses that exceed it.
On shared cloud egress, being blocked means blocking strangers too.

**Change.** `RateLimiter` — one `asyncio.Lock` and a floor of 0.11s between
requests, giving ~9 req/s against SEC's 10. A token bucket was considered and
rejected: the limit is low and the caller is a single worker, so the simplest
thing that *cannot* exceed the rate is a serialised queue.

**Result.** Correct by construction for one process. `request_headers()` also
refuses an empty User-Agent rather than sending a default, because a generic
string gets the address blocked for everyone behind it.

**Cost.** The correctness property depends on a deployment fact that is
recorded nowhere in the code. The lock is process-local; the NAT gateway's
Elastic IP is not. Two API tasks means 18 req/s from one address, and SEC sees
one address. `desired_count = 1` today, with no autoscaling — so this is
currently correct and one Terraform line away from being silently wrong.

`backend/ingestion/edgar.py:65,86,247`

---

## 8. Two independent dedupe identities

**Was.** One identity per document.

**Mode.** `full` only. Both writers live behind `ingestion_router`.

**Problem.** The same filing arrives by two routes — the EDGAR collector and a
manual upload. Canonical URL alone misses a re-upload under a different name;
content hash alone misses a document legitimately republished at a new URL.
Either identity used alone leaks duplicates.

**Change.** `dedupe.py` keeps both, and both writers import it rather than
implementing their own check, so the identity cannot diverge between the two
paths.

**Result.** Duplicates do not reach the corpus from either direction.

**Cost.** Two identities to maintain, and no answer yet for the case that
actually matters in finance: a filing that was later *restated*. That needs
`is_current` / `supersedes_document_id` on documents, which do not exist.

---

## 9. Metrics count as evidence — when the question is about numbers

**Was.** Every claim required a supporting document chunk.

**Problem.** "Healthcare companies with the strongest revenue growth" was
withheld with 21 flags, five reading *"no retrieval evidence — backed only by
database metrics"*. Revenue growth **is** a column. There is no filing to cite
for it. Demanding a document for a database fact set `has_missing_evidence` on
every company, forced three retries, and — once the reviewer was made to fail
closed — turned every numeric question into a refusal, including two of the
four questions the console offers as examples.

**Change.** `_METRICS_DRIVEN_INTENTS = {"VALUATION", "GROWTH"}`. For those,
metrics-only evidence is grounded. Narrative intents still require a document.
No evidence at all is still a failure for every intent.

**Result.** 150s → 22s. Hallucination rate 1.0 → 0.0. Decision `approved`.
Re-measured live at 45s end to end with zero retries.

**Cost.** The reviewer now trusts the metrics table without checking it. That
is defensible — it is our own database, not model output — but it means a bad
seed is invisible to the reviewer.

> Same mistake the retrieval-precision metric made: judging a structured
> result by document-retrieval criteria.

---

## 10. Refuse the question rather than answer it badly

**Was.** Four intents — VALUATION, GROWTH, SENTIMENT, MIXED — and no way to
decline.

**Problem.** `hello` returned five ranked companies at 52% confidence with a
*Reviewed* badge, in 121 seconds. The classifier had **already diagnosed it
correctly** and logged `reason=User greeted; no financial query provided` — then
returned SENTIMENT anyway, because the schema demanded one of four financial
intents. The right answer was produced and discarded in the same call. The
ranker then fell back to the whole corpus ordered by revenue growth.

**Change.** `OUT_OF_SCOPE` as a fifth intent with an exit edge straight to
`END`, and a report shape distinct from *withheld* — because "the evidence was
too thin" is the wrong thing to tell someone who typed a greeting.

**Result.** 121s → 1s. Six LLM calls to zero.

**Cost.** A classifier that can refuse can refuse wrongly, which is a worse
failure than answering a vague question. The prompt and the tests are
deliberately asymmetric: a bare company name stays *in* scope, an unrecognised
classification falls back to MIXED rather than to a refusal, and this is only
for input with no financial content whatsoever.

---

## 11. A runtime import guard, not a dependency removal

**Was.** `backend.main` imported at 404.5MB on preprod's 512MB instance, OOM-restarting
mid-query and returning 502s.

**Mode.** Runs identically in both — it is called unconditionally from
`backend/__init__.py`, which is the only placement that works, because
`main.py` is not the only entry point: the worker and the tests import
`backend.*` directly. Both modes therefore start with `_HAS_TRANSFORMERS`
False.

Mode decides what happens *after*. The guard removes itself, so `full` can
still import transformers when `sentence_transformers` asks for it and the
reranker works. A permanently blocked module would have turned reranking into a
silent no-op through `cross_encoder`'s own except-and-degrade path — fixing the
preprod instance by quietly breaking the feature on production, which has room
for it.

The only thing the False flag costs, in either mode, is
`BaseLanguageModel.get_num_tokens` falling back to a character heuristic.
Nothing calls it: token counts come from the provider, through
`usage_tracker`.

**Problem.** `langchain_core` feature-detects `transformers` at module scope
with a bare try/import. The probe keys on the package being *installed*, not
wanted — and it is installed transitively, because `docling` resolves to
`docling-slim[standard]`, which requires torch. Importing `langchain_openai`
loaded the entire torch stack for a reranker that cannot execute in that
deployment.

**Change.** My first instinct — drop `sentence-transformers` — was wrong, and
the lockfile said so. Instead: a meta-path finder hides `transformers` for
exactly one import of `langchain_core.language_models.base`, then removes
itself, so full mode's reranker still works.

**Result.** 404.5MB → 235.3MB.

**Cost.** A guard that depends on the private import path of a third-party
library. It is covered by four tests that fail if importing the app loads torch
again — this is the second time this happened through a different library,
which is why it is a test and not a comment.

---

## 12. A transport failure is not a content failure

**Was.** Two places treated "I could not reach the model" as a finding about
the answer. `_llm_hallucination_check` caught every exception and returned
`hallucination_rate: 1.0`, commented "Fail safely instead of silently
approving". The analysis node's empty report said "The analysis produced no
draft report" regardless of why it was empty.

**Problem.** Preprod runs on a Groq free tier capped at **200,000 tokens per
day for the whole organisation** — a ceiling that does not appear anywhere in
the code, and that a single question with retries can spend ten to twenty
thousand of. When it was reached:

    429 -- tokens per day (TPD): Limit 200000, Used 199833, Requested 451

1.0 is above `HALLUCINATION_THRESHOLD`, so a rate limit set `quality_failure`,
so the graph retried — regenerating the draft on the LARGE tier and asking the
judge again, against the budget that had just refused it. The failure fed
itself until the retry limit, and then withheld the report while blaming the
draft.

**Change.** Both provider calls moved behind their own function. Everything
outside those lines that raises is a fact about the draft; everything they
raise is a fact about the account. Two new terminals —
`withheld_review_unavailable` and `withheld_provider_unavailable` — each with
its own notice, because "the reviewer raised 0 unresolved issues" and "this
demo has reached its daily capacity" are not the same sentence.

**Result.** Verified by the failure itself: a run that exhausted the budget
mid-query returned `withheld_provider_unavailable` where it had returned
`withheld_empty_draft`.

**Cost.** Neither terminal approves, so an unreachable provider still withholds
the answer — correctly, but it means a quota problem and a quality problem look
equally serious to a reader who only sees that something was withheld. The
notice is the only thing distinguishing them.

---

## 13. Refusing concurrent callers rather than queueing them

**Was.** A per-IP rate limiter and nothing else.

**Problem.** That bounds one caller over time. It says nothing about how many
queries run at the same instant, because five testers clicking together are
five addresses, each comfortably inside its own limit. All five pipelines then
start on preprod's 0.5 CPU and 512MB, against the 200,000-token daily ceiling
above. Both
ends have been hit: an OOM restart that returned 502 to whoever was mid-query,
and the 429 in decision 12.

**Change.** `ConcurrencyBound`, default 2. The third caller gets a 429 with
`Retry-After` and a sentence saying the demo is answering as many questions as
it can.

Refusing rather than queueing, deliberately: a caller held behind a 45-second
query waits 90 seconds with no explanation, and a browser cannot tell that from
a hang. Worse service, better experience.

**Result.** Six concurrent requests against the real app: 2 served, 4 refused,
`in_flight` back to zero afterwards — including a round where one request 500'd
and still returned its permit.

**Cost.** The release is the whole risk. A permit held by a request that raised
is gone for the life of the process, and two of those means the demo answers
nothing until it restarts — a worse outage than the one being prevented. It is
in a `finally`, guarded by a flag set only once a permit is actually held, so a
refused request cannot release someone else's.

Process-local, like the rate limiter's fallback. One task today, so this is the
real ceiling; on several tasks it bounds each task rather than the service, and
the fix is the same as decision 4 — move the count to Redis.

---

## 14. What was removed

**The cross-encoder is off by default, and cannot run in `portfolio` at all.**
It is implemented and it works. Turning it on loads torch for real and needs
`1c-2g` instead of `0.5c-512mb`, so the public demo is not a deployment it
could be enabled on — only `full` on ECS is.
It stays off until there is a measurement showing what it improves — which is
the honest state, and the question to ask about every other component here.

**The LLM's holistic score is still in the ranking and should not be.**
`ranker.py:706` computes `(final_score * 0.7) + (llm_score * 0.3)`. There is
nothing justifying 30 over 10 or 50. Either an ablation defends that weight or
the component goes. This is a known open item, not a defended decision.
