# backend/security

**Request-path security.** Roughly 0.4 ms in total against a pipeline that takes 10-45 seconds. Every layer records what it did, which the admin feed reads.

| | |
|---|---|
| `input_guard.py` | prompt-injection and abuse patterns |
| `pii.py` | detection over inbound text |
| `output_validator.py` | checks on what is about to be returned |
| `rate_limit.py` | per-caller ceiling, Redis-backed, **fails open** by design |
| `concurrency.py` | a ceiling on queries running at once, refusing surplus with Retry-After |
| `llm_guard.py` | an optional model-based check, off by default |
| `events.py / events_feed.py` | the security event log |

_Implementations are private. This file lists what lives here and what it is responsible for._
