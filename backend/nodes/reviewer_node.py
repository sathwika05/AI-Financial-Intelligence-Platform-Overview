"""
The fact-checking stage, and the only one that can refuse to answer.

Four terminals, two of which withhold the ranking rather than present it as
reviewed. A transport failure is not a finding about the answer, and telling a
reader "the reviewer raised 0 unresolved issues" while withholding the
reviewer's result is worse than telling them nothing.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from typing import Any, Literal

from backend.state.financial_state import FinancialState

Decision = Literal[
    "approved",
    "forced_pass",                     # retry limit reached
    "withheld_review_unavailable",     # the judge could not be reached
    "withheld_provider_unavailable",   # the provider refused the draft call
]

MAX_RETRIES = 3


async def reviewer_node(state: FinancialState, config) -> dict[str, Any]:
    """Check the draft against its evidence; approve, redraft or withhold."""
    ...


def route_after_review(state: FinancialState) -> str:
    """`analysis` to redraft, `output` to finish.

    Never back to retrieval: by this point the query, the cohort and the
    corpus are fixed, so re-retrieving returns the same documents and raises
    the same flags. A retry is also skipped when this attempt's feedback is
    identical to the last one's.
    """
    ...


def _validate_citations(draft: dict, evidence: list[dict]) -> list[str]:
    """Flag every claim whose citation id is absent from the evidence."""
    ...
