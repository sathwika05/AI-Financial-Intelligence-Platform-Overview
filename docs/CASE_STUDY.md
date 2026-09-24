# Screening 50 companies without reading 50 filings

## The problem

An analyst screening a sector for a shortlist does the same thing every time.
Pull the metrics that filter — P/E, revenue growth, margin. Then, for anything
that survives the filter, go and read what the company actually *said*: the
earnings call, the risk factors, the management commentary. The numbers tell
you which companies to look at. Only the filings tell you whether the numbers
mean what they appear to mean.

The filter is fast. The reading is not, and it does not parallelise, so the
practical effect is that the shortlist gets shorter than it should be — you
read the top five because you cannot read the top twenty.

Two systems already solve half of this each. A screener ranks on columns and
knows nothing about narrative. A document search returns passages and cannot
rank. Putting them in the same answer is the actual work, and the hard part is
not retrieval — it is being able to say, for each sentence in the output,
which retrieved thing supports it, and refusing to answer when nothing does.

**That refusal is the product.** A screening tool that is confidently wrong is
worse than no tool, because it is faster at being wrong than a person is.

## What this is, and what it is not

This is a working system with a public demo, a 100-question benchmark, and a
production deployment target on AWS.

**It has not yet been used by a working analyst.** Everything below is
engineering evidence — defects found, fixes measured, decisions recorded. The
user evidence is in progress and is tracked in [§9](#9-what-real-users-said)
as pending. Where a number here is derived rather than observed, it says so.

I would rather this document be short and true than long and impressive.

## What it does

A question goes through six stages: classify the intent, plan the retrieval,
run SQL / vector / market lookups in parallel, score and rank the candidates,
write the analysis, then review that analysis against the evidence that was
actually retrieved. The reviewer can send the answer back, and can refuse to
publish it.

The interesting behaviour is all at the end. A ranked list is easy. A ranked
list that withholds itself when its own evidence does not hold up is the part
that took the longest and broke the most times.

---

## The five things that broke

Written up in full in [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md);
summarised here because they are the substance of the project.

| What broke | Root cause | Measured after |
|---|---|---|
| API OOM-restarting, 502s mid-query | `langchain_core` feature-detects `transformers` at import; installed transitively via `docling` → `docling-slim[standard]` → torch | 404.5MB → **235.3MB** |
| A report with 14 unresolved flags rendered as *Reviewed* | Two paths returned `passed: True, decision: forced_pass`; the escalation branch below 0.30 confidence had never fired, because self-reported confidence floors near 0.49 | Both paths withhold; **23 tests** |
| `hello` returned 5 ranked companies at 52% confidence | The classifier diagnosed it correctly, logged the reason, and had no intent to return it as | **121s → 1s** |
| Every numeric question refused | The reviewer demanded a document chunk for a database column | **150s → 22s**, hallucination rate **1.0 → 0.0** |
| Every factor at 0% weight; composite = model opinion × 0 | A regression I introduced fixing the one above, over a real bug: scoring gated on whether SQL ran, not on what the scorer reads | Caught by my own preset questions failing |
| The demo silently served dense-only retrieval | Groq rejected its own tool call; the keywords it generated were discarded with the error | **0/5 → 5/5**, by reading the rejection body |
| Company filters silently off | Same rejection, different schema — this one fixed by describing it | **6/12 → 12/12** |
| A rate limit reported as total hallucination, causing a retry storm | The reviewer caught every exception and returned `hallucination_rate: 1.0`, which is above the retry threshold | Withholds without retrying |
| "The analysis produced no draft report" on a spent token budget | Provider failure and content failure shared one exit | Its own terminal and notice |

The last row is the one worth reading twice. I caused it, and I found it
because two of the four example questions on my own console stopped working.
Every change that day was verified against a `git stash` baseline diffed **by
failing-test name**, not by count — 25 failed / 1482 passed against 25 / 1474,
identical failure sets.

## What I deliberately did not build

- **A Slack or Teams integration.** No user has asked for one. Building
  integrations nobody requested is how you end up with a platform instead of a
  product.
- **The cross-encoder, in the demo.** Implemented, works, off by default. It
  loads torch for real and needs four times preprod's instance. It stays off
  until there is a
  measurement showing what it improves.
- **Multi-tenancy.** A nullable `workspace_id` and one enforced filter is the
  whole shape; it is two hours and it is not written, because nothing needs it.
- **Anything that made the RAGAS number go up.** Three edit-and-measure cycles
  landed inside judge variance. The noise floor is 0.04. I stopped.

## The constraint that shapes everything

The public demo — preprod, one Render instance at 0.5 CPU and 512 MB — runs on
a Groq free tier allowing **200,000 tokens per day across the whole
organisation**. Production is metered and has no equivalent cliff; every tight
number in this document is a preprod number unless it says otherwise. A single question with retries can spend ten to twenty
thousand of them, so the demo answers roughly ten to thirty questions a day
before it goes dark.

That number is not in any diagram, and it is the single most important fact
about running this. It is why the retry loop being wasteful was a *budget* bug
and not only a latency one, why a 429 had to stop meaning "hallucination", and
why concurrent callers are refused rather than queued. Three of the day's
fixes trace to one line in an error message.

## What is still wrong

Named here rather than discovered later.

- ~~The public demo serves pure dense ordering.~~ **Fixed.** Groq's small tier
  returned the keywords as message content instead of a tool call and then
  rejected its own response with `400 tool_use_failed`, so `bm25_rerank` took
  its empty-keyword branch and handed back the pgvector order untouched. Four
  plausible fixes measured 0/5 — a described schema, a larger tier, and a
  rewritten prompt all failed. The rejection body turned out to contain the
  correct keywords every time, so they are now recovered from it: 5/5, no extra
  call. See decision 3.
- **Reciprocal rank fusion is benchmark-only, by design and undocumented.**
  There are two BM25 stages. `bm25_rerank` reorders what pgvector already
  returned, and runs everywhere. `search_chunks_lexical` ranks the whole corpus
  independently so RRF has a list that can *disagree* with dense — and it runs
  only when `retrieval_flags.rrf_enabled` is set, which happens in exactly one
  place, `evaluation_routes.py:638`, mounted in `full` mode only. That scoping
  is defensible; not writing it down is what let the docs read as a claim about
  the demo.
- ~~The public endpoint has no concurrency bound.~~ **Fixed** — two at a time,
  the third refused with a `Retry-After`. Process-local, so it bounds a task
  rather than a service; on more than one task the count belongs in Redis.
- **The LLM's holistic judgment moves the ranking by a hardcoded 30%** with
  nothing justifying 30 over 10 or 50.
- **Operational tables have no writers.** p50 and p95 are architected for and
  not implemented.
- **Escalations are recorded on the public demo and cannot be read there** — the
  writer runs in both modes, the router is mounted in one.

---

## Sections still to be written

**§9 What real users said.** Pending. Three finance people, two identical
tasks, time to complete, whether they clicked a citation, whether they could
explain the score, every confusion recorded verbatim. Then one change shipped
because of a recurring complaint, and the same task measured again.

The bar for this section is a commit whose existence traces to a named person
who is not me. Until that exists, this section stays empty rather than
simulated.

**§10 Business metrics.** Blocked on §9. Any before/after here that is not
observed will be labelled as derived.

**§11 Demo video.** Three minutes, the actual workflow, including a query the
system refuses.
