# backend/evaluation/evaluators

**Per-gate evaluators.** A question passes only if every applicable gate passes, which is why a question can score highly overall and still fail.

| | |
|---|---|
| `intent_evaluator.py` | was it routed correctly |
| `tool_evaluator.py` | were the right tools called |
| `sql_evaluator.py` | do the rows match expected, and is the SQL equivalent |
| `ranking_evaluator.py` | precision@k, recall@k, MRR, nDCG |
| `ragas_evaluator.py` | faithfulness, relevancy, context precision and recall |
| `market_evaluator.py` | live-data claims |

_Implementations are private. This file lists what lives here and what it is responsible for._
