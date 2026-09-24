# backend/observability

**Logging and tracing.** LangSmith owns the trace hierarchy; the database keeps what has to be joined or aggregated. The split is deliberate — see the root README.

| | |
|---|---|
| `tracing.py` | node-boundary spans and the timing wrapper |
| `langsmith_setup.py` | tracer configuration |
| `logging.py` | structured logging |
| `query_log.py` | per-query rows for latency and withheld-share reporting |

_Implementations are private. This file lists what lives here and what it is responsible for._
