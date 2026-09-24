# Benchmark results

Nine runs against the same 100 questions, varying one thing at a time.

Read the control first. Everything else depends on it.

## The noise floor

The baseline was run twice with no change between the runs — same code, same
frozen snapshot, same questions, same provider.

**The two runs disagreed on 11 of the 100 questions**, scoring 84 and 83.

That is the measurement error of this benchmark. A configuration that moves the
total by two or three questions has demonstrated nothing, and reporting such a
move as an improvement would be reporting noise. Every number below is written
against that bar.

The questions that flip are not random: they cluster at the RAGAS gate, where a
judge model scores a borderline answer either side of a threshold. Questions
answered from database columns essentially never flip.

## Retrieval arms

All on the same provider, varying only the retrieval configuration.

| Arm | Valuation | Growth | Sentiment | Mixed | Total |
|---|---|---|---|---|---|
| Dense + BM25Plus rerank (baseline) | 30/30 | 30/30 | 18/25 | 6/15 | **84** |
| The same baseline, repeated | — | — | — | — | **83** |
| LLM ranking weight removed | 30/30 | 30/30 | 18/25 | 8/15 | **86** |
| Cross-encoder rerank | 30/30 | 30/30 | 21/25 | 6/15 | **87** |

Reciprocal rank fusion was measured on the 40 sentiment and mixed questions
only — the 60 database questions do not retrieve documents, so fusing document
rankings cannot affect them. It scored 25/40 against the baseline's 24/40 on
the same subset.

**No retrieval configuration cleared the noise floor.** The spread across every
arm is three questions against a measured error of eleven.

Two results are worth stating precisely, because the temptation is to round
them up:

- **Removing the LLM from the ranking cost nothing.** The component was blended
  in at a hardcoded 30% with no justification for that number over any other.
  Setting the weight to zero — removing it entirely — scored 86 against the
  baseline's 84. The honest conclusion is not that removing it helps, but that
  *the component does not earn its weight*.
- **The cross-encoder's only visible movement was on sentiment**, 21/25 against
  18/25, the best any arm produced on that intent. At this corpus size the
  shortlist handed to the cross-encoder is smaller than the evidence budget, so
  it reorders the evidence but never discards any of it. Its ceiling here is
  ordering effects alone, which makes a three-question move on 25 questions
  exactly the kind of result the noise floor exists to discipline.

## Provider arms

The same pipeline, the same retrieval, a different model provider. Both scored
far below the baseline, and **neither number measures the model's reasoning.**

| Arm | Total | What the number actually measures |
|---|---|---|
| Provider B | 57/100 | SQL generation that omits `LIMIT` and filter clauses |
| Provider C | 13/100 | A rate-limit ceiling the pipeline cannot run inside |

### Provider C: the score is the rate limit

The provider's free tier allows 8,000 tokens per minute. A single mixed
question costs roughly 29,000 tokens across the graph. The result:

- 454 of 731 calls returned HTTP 429
- the analysis node failed outright on 93 questions
- 186 answers returned `withheld_provider_unavailable` — the pipeline correctly
  refusing to publish an answer it could not generate

The metric shape proves it. On the same question with the same retrieved
contexts:

| Metric | Derived from | Baseline | Provider C |
|---|---|---|---|
| faithfulness | the answer | 0.824 | **0.000** |
| response relevancy | the answer | 0.773 | **0.000** |
| noise sensitivity | the answer | 0.294 | **0.000** |
| context precision | the contexts | 0.531 | 0.617 |
| context recall | the contexts | 1.000 | 1.000 |
| context entity recall | the contexts | 0.571 | 0.429 |

Every metric computed from the answer is exactly zero. Every metric computed
from the contexts scores normally — context precision is marginally *better*
than the baseline's. That is the signature of no answer to grade, not of a
wrong answer.

## What the provider swaps were actually worth

Neither provider arm produced a usable quality number. Both produced something
more useful: each exposed a latent defect that six runs on a single provider
had never touched.

**Response shape.** One provider's client returns the model reply as a list of
content blocks rather than a string. Nine call sites in the pipeline read that
reply as a string. Every one of them raised, so the arm produced no SQL, no
ranking scores and no draft report on any question until the reply was read
through a provider-agnostic accessor.

**Tool-schema validity.** Two tool parameters were annotated as required
strings while defaulting to null, producing a JSON schema that forbids its own
default. The original provider does not validate tool arguments server-side, so
the contradiction was invisible. A provider that does validate rejected every
SQL tool call outright. The fix is one annotation per parameter; the guard is a
test that walks every registered tool and fails on any parameter whose schema
rejects a null it defaults to.

Both are the same category of bug — an assumption that held because only one
implementation had ever been exercised. Neither was findable without a second
provider, and neither would have surfaced in a unit test written against the
first.

## What this measures, and what it does not

The benchmark grades four things per question: routing (did it choose the right
intent), tool use, SQL correctness against expected rows, and answer quality
against authored ground truth. A question passes only if every applicable gate
passes, which is why a question can score 0.88 overall and still fail.

Ground truth is maintained in two halves. The 60 database questions are
generated from specifications by querying the frozen snapshot, and are
regenerated after any reseed rather than hand-edited. The 40 narrative
questions carry reference answers and reference contexts written by hand — a
model-written reference would only confirm the model's own output.

What the benchmark does not measure: live market data moves between runs and is
fetched at query time, so a mixed question varies by however much prices moved.
Cost and latency per question are recorded but are not pass criteria.
