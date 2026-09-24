# backend/graph

**LangGraph state graphs.** Three graphs and the runner that invokes them. The financial graph orchestrates the full pipeline; the SQL and vector graphs are ReAct tool-calling agents used alone.

| | |
|---|---|
| `financial_graph.py` | the pipeline graph — wiring shown in this repo |
| `sql_graph.py` | an LLM bound to SQL tools, looping until done or three failed repairs |
| `vector_graph.py` | an LLM bound to a single retrieval tool |
| `runner.py` | invocation, config assembly, checkpointing |

_Implementations are private. This file lists what lives here and what it is responsible for._
