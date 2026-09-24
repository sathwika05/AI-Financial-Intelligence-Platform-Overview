# backend/nodes

**Graph nodes.** One module per stage. Each reads and writes only the shared state, which is what lets a stage be timed, traced and replaced independently.

| | |
|---|---|
| `intent_node.py` | classifies the query, or exits the graph as out of scope |
| `planner_node.py` | splits it into per-source sub-queries and a fan-out strategy |
| `sql_node.py / vector_node.py / market_node.py` | the three single-source retrievals |
| `reranker_node.py` | reorders heterogeneous evidence before drafting |
| `scoring_node.py` | ranks companies and attaches citations |
| `analysis_node.py` | drafts the cited report |
| `reviewer_node.py` | fact-checks the draft, and can withhold it |

_Implementations are private. This file lists what lives here and what it is responsible for._
