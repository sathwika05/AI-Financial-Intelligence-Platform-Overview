# backend/services

**External services.** Thin clients, each tolerant of its dependency being unavailable.

| | |
|---|---|
| `postgres_service.py` | async engine and session factory |
| `redis_service.py` | cache and rate-limit store; unreachable is tolerated |
| `market_api_service.py` | live market data, with ticker extraction |

_Implementations are private. This file lists what lives here and what it is responsible for._
