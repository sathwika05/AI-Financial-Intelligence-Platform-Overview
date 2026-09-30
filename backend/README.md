# backend

The backend's shape: how the graph is wired, what the state contract is, and
what the one public route accepts and returns.

This is the interface surface: how the graph is wired, what each package is
responsible for, and the contracts between them. `retrieval/fusion.py` is
included in full — reciprocal rank fusion is a published algorithm.

| File | What it shows | Complete? |
|---|---|---|
| `main.py` | router mounting driven by `DEPLOYMENT_MODE` | interface |
| `api/financial_routes.py` | the one route available in every mode | interface |
| `graph/financial_graph.py` | node registration and the conditional edges | wiring only |
| `state/financial_state.py` | the state every node reads and writes | interface |
| `retrieval/fusion.py` | rank fusion across retrievers | **full** |
| `llm/tiers.py` | the tier a caller asks for instead of a model name | full |

The full architecture is described in [the root README](../README.md).
