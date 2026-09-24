# backend/api

**FastAPI routers.** One router per surface. Which of these mount at all is decided by `DEPLOYMENT_MODE` — a public deployment does not mount the nine privileged routers, rather than mounting them behind a check.

| | |
|---|---|
| `financial_routes.py` | the query route, the only one public in every mode |
| `auth_routes.py` | sign-in, token issue, current user |
| `sql_routes.py / vector_routes.py` | the single-source agents, exposed alone |
| `ingestion_routes.py` | upload, EDGAR collection, job status |
| `evaluation_routes.py` | benchmark runs, metrics, per-question results |
| `claim_routes.py / escalation_routes.py` | claim audit, and answers queued for human review |
| `security_routes.py / admin_llm_routes.py` | event feed, provider and model configuration |

_Implementations are private. This file lists what lives here and what it is responsible for._
