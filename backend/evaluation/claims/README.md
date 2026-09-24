# backend/evaluation/claims

**Claim audit.** Extracts individual factual claims from an answer and checks each against the retrieved evidence, so an answer that is right overall but unsupported in one sentence is visible as such.

| | |
|---|---|
| `extractor.py` | claims out of prose |
| `checker.py` | each claim against its evidence |
| `policy.py` | what counts as supported |
| `runner.py / store.py` | orchestration and persistence |

_Implementations are private. This file lists what lives here and what it is responsible for._
