"""
SQLAlchemy models. 23 tables.

Embeddings live on `document_chunks`, not `documents` — a filing is far
longer than one embedding can represent, and chunk-level vectors are what
retrieval actually compares against.
"""
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    ...


class Company(Base):
    __tablename__ = "companies"
    ticker: Mapped[str]
    name: Mapped[str]
    sector: Mapped[str]
    market_cap: Mapped[float | None]


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    document_id: Mapped[int]
    chunk_index: Mapped[int]
    content: Mapped[str]
    # Vector(1536), indexed HNSW with vector_cosine_ops. The operator class
    # must match the query's operator or the index is never chosen, silently.
    embedding: Mapped[list[float] | None]


# Also: financial_metrics, documents, themes, company_themes, llm_providers,
# llm_models, users, benchmark_runs, evaluation_metrics, question_results,
# claim_evaluations, escalations, ingestion_events, system_logs,
# retrieval_logs, retrieved_evidence, model_costs.
