# Operations

What this service does under load, what it does when a dependency is gone, and
what is known to be wrong with it.

Numbers marked **preprod** describe the constrained public deployment: one
instance at 0.5 CPU and 512 MB, `portfolio` mode. They are the tightest numbers
in the system and the ones most likely to bind.

---

## Service level

| | |
|---|---|
| Query latency | 10–45 s typical; p95 60 s on the heaviest intent |
| Slowest stage | the analysis call — **91% of cost, 63% of latency** |
| Fastest path | an out-of-scope question exits at the classifier in ~1 s |
| Throughput ceiling | a concurrency cap, not CPU — see below |
| Cost per question | ~$0.08 simple, ~$0.14 heaviest (measured, OpenAI) |

A question takes tens of seconds because it runs a seven-stage graph with a
parallel retrieval fan-out and a fact-checking pass. That is the design, not a
regression. The per-node breakdown exists because a run total cannot show that
one call dominates both budgets.

## Timeouts, and what happens when they fire

| Boundary | Limit | On expiry |
|---|---|---|
| SQL retrieval | 45 s | branch returns nothing; query continues on the others |
| Vector retrieval | 10 s | same |
| Market data | 8 s | same |
| Whole fan-out | 60 s | whatever returned is used |
| Judge call (evaluation) | 120 s, 2 retries | the metric reports no value |
| Judge metric total | 600 s | metric dropped, **not** zeroed — a missing measurement is not a score of zero |

**Partial failure is a normal outcome.** Confidence is derived only from the
sources that actually returned, and a dimension whose source is missing is
reported as `unmeasured` rather than scored zero. Scoring it zero would assert
the company did badly, which is not what a dead branch means.

## Degradation

| Dependency | If unavailable | Rationale |
|---|---|---|
| Redis | tolerated — rate limiting and caching fail **open** | a cache outage must not become a service outage |
| Market API | branch returns nothing, weights redistribute | prices are the least essential of three sources |
| Vector store | narrative intents lose their evidence and the answer is withheld | an unsupported narrative answer is worse than none |
| Provider (analysis) | answer withheld as `withheld_provider_unavailable` | a transport failure is not a finding about the answer |
| Provider (reviewer) | answer withheld as `withheld_review_unavailable` | unverified is not the same as verified-and-clean |

The last two exist because telling a reader *"the reviewer raised 0 unresolved
issues"* while the reviewer never ran is worse than telling them nothing.

## Capacity

Two independent ceilings, both **process-local**:

- **Per-caller rate limit** — a request budget per window, per caller. Redis-backed,
  fails open.
- **Global concurrency cap** — how many queries run *at once*, across all callers.
  Surplus is refused with `Retry-After` rather than queued: on a pipeline that
  takes 10–45 s, a queued request is one that times out somewhere else instead.

The second is not redundant with the first. Several callers are several
addresses, each inside its own per-caller budget, and all their pipelines start
together on one small instance.

> **Known limit.** Both counters live in the process. On preprod that is the
> true ceiling, because there is one instance. Above `desired_count = 1` they
> bound each task rather than the service, and the count belongs in Redis. The
> EDGAR request lock has the same shape — per-process, while the egress address
> is shared — so it is correct at one instance and one Terraform line away from
> being silently wrong.

## Memory

| | |
|---|---|
| Import footprint | ~235 MB |
| Was | 404 MB, until an import guard stopped a transitive pull of torch |
| Cross-encoder | +270 MB — **will not fit a 512 MB instance** |

The cross-encoder is therefore a per-run flag rather than a build-time
dependency: production could hold it, preprod cannot, and the same image has to
serve both.

## Startup

Two failure modes that are obscure if you have not met them:

1. **`backend.main` cannot be imported without `OPENAI_API_KEY`.** The embeddings
   client is constructed at module scope and validates credentials on
   construction, so the server exits at import from a clean shell. Export the
   environment first.
2. **A blank `REDIS_URL` is worse than a missing one.** Missing falls back to the
   default; blank is a string the client rejects at import, turning a typo into a
   startup crash rather than a warning.

## Migrations

The Alembic chain **cannot build a database from scratch.** Its first revision
*alters* tables that the ORM's `create_all` is expected to have made, because
those tables already existed when the chain started.

Run the startup migration helper, which looks for the version table and stamps
rather than replays when the schema came from the models. Calling
`alembic upgrade head` directly against an empty database fails on a table that
does not exist yet.

## Security posture

Six layers on the request path, together about **0.4 ms** against a pipeline
measured in tens of seconds: input guard, PII detection, output validation,
per-caller rate limit, global concurrency, and an optional LLM-based check that
is off by default because it costs an API round trip per query.

Every layer writes what it did to an event log, which the admin feed reads.

**Route absence is the control.** In `portfolio` mode the nine privileged
routers are not mounted at all. Unlinking a route from the UI leaves it
reachable; not mounting it does not.

Generated SQL executes as a SELECT-only role, and is validated before execution
as well.

## Observability

| Signal | Where | Why there |
|---|---|---|
| Trace hierarchy | LangSmith, 57 instrumented spans | nothing here competes with it for inspecting one query |
| Latency, cost, decisions | Postgres | *"p95 latency for withheld answers on healthcare questions last week"* is one SQL query and an export-and-spreadsheet exercise anywhere else |

The split is deliberate. The database half also survives a third party's
retention policy and an enterprise deployment that cannot send data outside its
own network.

Three tables were dropped rather than filled, each because something else
already answered the question — threshold alerting with no destination for an
alert, a trace table duplicating four columns held elsewhere, and a second
human-review loop for grading benchmark output, which authored ground truth
makes unnecessary.

## Known limitations

- **No CORS middleware.** Every deployment shares an origin or rewrites `/api`
  and `/health` to the API. Deliberate, but it constrains how the API can be
  consumed.
- **Counters are process-local** (above). Correct at one instance.
- **The Alembic chain cannot bootstrap** (above).
- **An LLM opinion is blended into the ranking at a hardcoded 30%.** The weight
  was made a per-run parameter and measured: removing the component entirely
  scored no worse. It survives only because that result sits inside the noise
  floor in both directions. See [BENCHMARKS.md](BENCHMARKS.md).
- **Reseeding invalidates the benchmark.** Live fundamentals move, so the
  membership of a "top five" can change and the benchmark marks a correct answer
  wrong. The frozen snapshot exists to prevent this; use it.

## What to check first

| Symptom | Look at |
|---|---|
| Every answer withheld | provider reachability and quota — the pipeline is refusing correctly |
| Answers slow, not failing | per-node latency; the analysis stage dominates by design |
| 429s from the API | the concurrency cap, not the per-caller limit, if callers are distinct |
| Benchmark score moved | whether the corpus was reseeded before blaming the code |
| An ablation shows nothing | whether the flag actually engaged — recording a flag is not running it |
