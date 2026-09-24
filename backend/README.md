# backend — minimal excerpt

Enough of the backend to show its shape: how the graph is wired, what the
state contract is, and what the one public route accepts and returns.

**This is not the implementation.** Node bodies, prompts, retrieval, scoring,
evaluation and the security layer live in a private repository. Files here are
trimmed to their structure, except `retrieval/fusion.py`, which is complete —
reciprocal rank fusion is a published algorithm and there is nothing in it to
withhold.

| File | What it shows | Complete? |
|---|---|---|
| `main.py` | router mounting driven by `DEPLOYMENT_MODE` | trimmed |
| `api/financial_routes.py` | the one route available in every mode | trimmed |
| `graph/financial_graph.py` | node registration and the conditional edges | wiring only |
| `state/financial_state.py` | the state every node reads and writes | trimmed |
| `retrieval/fusion.py` | rank fusion across retrievers | **complete** |
| `llm/tiers.py` | the tier a caller asks for instead of a model name | complete |

The full architecture is described in [the root README](../README.md).
