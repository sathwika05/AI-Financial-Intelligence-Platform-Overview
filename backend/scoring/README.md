# backend/scoring

**Ranking and evidence.** Four normalized dimension scores per company, weighted by which sources actually returned. Dimensions with no data are reported as unmeasured rather than scored zero.

| | |
|---|---|
| `ranker.py` | dimension scores, weighting, optional LLM blend |
| `evidence_builder.py` | per-company citations |
| `score_normalizer.py` | the explainability breakdown and recommendation bucket |

_Implementations are private. This file lists what lives here and what it is responsible for._
