# backend

The backend's shape: how the graph is wired, what the state contract is, and
what the one public route accepts and returns.

| File | What it shows |
|---|---|
| `main.py` | router mounting driven by `DEPLOYMENT_MODE` |
| `api/financial_routes.py` | the one route available in every mode |
| `graph/financial_graph.py` | node registration and the conditional edges |
| `state/financial_state.py` | the state every node reads and writes |
| `retrieval/fusion.py` | rank fusion across retrievers |
| `llm/tiers.py` | the tier a caller asks for instead of a model name |

The full architecture is described in [the root README](../README.md).
