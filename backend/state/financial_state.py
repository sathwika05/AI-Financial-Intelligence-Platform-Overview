"""
The state every node reads and writes. Trimmed: see backend/README.md.
"""
from typing import Annotated, Any, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class FinancialState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    original_query: str

    # Intent — VALUATION | GROWTH | SENTIMENT | MIXED | OUT_OF_SCOPE
    intent: str
    intent_reason: str

    # Planner — one sub-query per source, plus a fan-out strategy
    sql_query: str
    vector_query: str
    market_query: str
    strategy: str

    # The candidate universe: who is eligible to be ranked, decided once and
    # shared by every retrieval branch.
    #
    # Without this, each branch discovered its own set — SQL inferred a filter
    # from document text while the market branch resolved tickers from the
    # planner's wording — and the scorer ranked the union, so a company nobody
    # asked about could win the query.
    candidate_company_ids: list[int]

    # Retrieval, scoring, drafting, review
    retrieved_contexts: list[dict[str, Any]]
    ranked_companies: list[dict[str, Any]]
    draft_report: dict[str, Any]
    review_result: dict[str, Any]
    final_report: dict[str, Any]

    retry_count: int
