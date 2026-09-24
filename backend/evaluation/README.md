# backend/evaluation

**Benchmark and evaluators.** The harness that makes the pipeline's quality measurable: 100 questions, versioned ground truth, per-gate evaluators and a claim-level audit.

| | |
|---|---|
| `benchmark_runner.py` | runs a question set, writes per-question results |
| `aggregation.py` | run-level metrics |
| `judges.py` | the judge clients, with bounded timeouts |
| `schemas.py / metrics.py` | result shapes and metric definitions |

_Implementations are private. This file lists what lives here and what it is responsible for._
