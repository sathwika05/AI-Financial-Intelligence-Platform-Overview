# tests

**Test suite.** 101 modules, written as statements about behaviour rather than coverage of functions — a test is named for the guarantee it defends, so a failure names what broke.

| | |
|---|---|
| `fixtures/` | filings that exercise the hard paths: a scanned PDF with no text layer, a password-protected one |
| `(modules)` | named for their guarantee, e.g. that events survive a restore, that run totals survive a crash, that every question resolves its cohort |

_Implementations are private. This file lists what lives here and what it is responsible for._
