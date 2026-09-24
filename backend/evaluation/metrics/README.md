# backend/evaluation/metrics

**Retrieval metrics.** Recorded per benchmark question so two retrieval arms can be diffed by which chunks they actually surfaced.

| | |
|---|---|
| `retrieval_metrics.py` | coverage of the contexts the ground truth cites |
| `evidence_recorder.py` | the chunks a run retrieved, kept for comparison |

_Implementations are private. This file lists what lives here and what it is responsible for._
