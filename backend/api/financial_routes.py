"""
The one route available in every deployment mode. Trimmed: see backend/README.md.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/retrieve", tags=["financial"])


class FinancialQueryRequest(BaseModel):
    # Bounded at both ends: too short to be a question, or long enough to be
    # a prompt-injection payload rather than a query.
    query: str = Field(min_length=3, max_length=500)


@router.post("/financial")
async def financial_query(request: FinancialQueryRequest):
    """
    Run the graph and return the reviewed report.

    In `full` mode this route requires the analyst role. In `portfolio` mode it
    is public and the per-caller rate limit is the only ceiling.

    The response carries `final_report` — which may be withheld, with a reason,
    rather than presented as reviewed — alongside the raw `result`.
    """
    ...
