# backend/retrieval

**Hybrid retrieval.** Intent decides which sources run and how their results are weighted. Two retrieval stages exist behind per-run flags so variants stay measurable against the same questions.

| | |
|---|---|
| `hybrid_retrieval.py` | the fan-out, its timeouts and graceful degradation |
| `vector_search.py` | pgvector ANN search and the BM25 rerank over its results |
| `lexical_search.py` | BM25 over the whole corpus — the independent list RRF needs |
| `fusion.py` | reciprocal rank fusion — **complete in this repo** |
| `cross_encoder.py` | optional joint query-document rerank; fails open |
| `embedding_cache.py` | query embeddings, cached on exact text |
| `sql_executor.py` | schema lookup, generation, validation, execution, repair |
| `query_filters.py / theme_resolver.py` | filter extraction and cohort resolution |

_Implementations are private. This file lists what lives here and what it is responsible for._
