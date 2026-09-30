"""
The human review queue.

An answer the reviewer could not approve is queued here rather than shown as
reviewed. This is the review loop that matters — a second loop for grading
benchmark output was considered and rejected, because authored ground truth
is written before a run, not rated after it.
"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Escalation:
    id: UUID
    query: str
    reason: str                 # why the reviewer withheld it
    status: str                 # open | resolved
    reviewed_by: str | None
    resolution_note: str | None


async def queue(query: str, draft: dict, review: dict) -> UUID:
    """Record an answer for human review; returns its id."""
    ...


async def resolve(escalation_id: UUID, reviewer: str, note: str) -> None:
    """Close one, recording who decided and what they concluded."""
    ...
