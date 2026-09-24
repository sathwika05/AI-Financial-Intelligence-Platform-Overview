# backend/ingestion

**Corpus ingestion.** Upload and EDGAR collection through chunking and embedding. One event row is written per attempt, including attempts that produced no document — duplicates, unreadable PDFs.

| | |
|---|---|
| `edgar.py / collector.py` | SEC collection, rate-limited |
| `extract.py / normalize.py / chunking.py` | text out of filings, then into chunks |
| `indexing_service.py` | embedding and indexing |
| `dedupe.py` | content-hash deduplication |
| `aws.py / publisher.py / consumer.py / queue_worker.py` | the S3 to SQS to worker path |
| `events.py / events_log.py` | one row per attempt |

_Implementations are private. This file lists what lives here and what it is responsible for._
