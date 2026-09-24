# backend/evaluation/datasets/question_sets

**Question sets.** 100 questions split 30 valuation / 30 growth / 25 sentiment / 15 mixed, plus a 4-question `smoke` set and an env-driven `focus` set for iterating on specific questions.

| | |
|---|---|
| `valuation.py / growth.py` | derived — generated from specifications by querying the frozen snapshot |
| `sentiment.py / mixed.py` | authored — human-written reference answers and reference contexts |
| `_generated.py` | the generated rows, rebuilt after any reseed |

_Implementations are private. This file lists what lives here and what it is responsible for._
