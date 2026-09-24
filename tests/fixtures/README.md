# tests/fixtures

**Test fixtures.** Filings chosen to exercise the paths that actually break ingestion.

| | |
|---|---|
| `filing_with_text_layer.pdf` | the ordinary case |
| `filing_scanned_no_text_layer.pdf` | a scan — extraction must fail honestly, not return empty text |
| `filing_password_protected.pdf` | unreadable, and recorded as an attempt that produced no document |

_Implementations are private. This file lists what lives here and what it is responsible for._
