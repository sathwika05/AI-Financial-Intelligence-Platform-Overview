# Security

## Reporting

If you believe you have found a vulnerability in the design described here, or
in the public deployment, open an issue describing the concern without
including exploit detail, and I will follow up.

## What is enforced in the implementation

Six layers run on the request path, in this order, at roughly 0.4 ms in total:

| Layer | Enforces |
|---|---|
| Input guard | prompt-injection and abuse patterns on inbound text |
| PII detection | flags personal data in queries |
| Output validation | checks what the pipeline is about to return |
| Rate limit | per-caller request ceiling, Redis-backed, **fails open** |
| Concurrency | global cap on queries in flight, refuses surplus with `Retry-After` |
| LLM guard | optional model-based classification, off by default |

Every layer records its decision to an append-only event log.

## Design decisions that carry security weight

- **Route absence over route authorization.** In the public deployment mode the
  nine privileged routers are not mounted at all. A route that is not mounted
  cannot be reached by guessing its path.
- **Generated SQL runs as a SELECT-only role** and is validated before execution.
  The model can compose a query; it cannot be given permission to change data.
- **Provider API keys are Fernet-encrypted at rest** in the database. Nothing
  reads a provider key from the environment, and the admin UI can set a key but
  never reads one back.
- **Rate limiting fails open, deliberately.** A cache outage degrades a control;
  it does not take the service down. The global concurrency cap is the ceiling
  that does not depend on Redis.
- **The pipeline refuses rather than guesses.** An answer whose claims cannot be
  checked against retrieved evidence is withheld with a reason, not published
  with a confident tone.

## What is not in this repository

No credentials, connection strings, API keys or benchmark ground truth are
published here.
