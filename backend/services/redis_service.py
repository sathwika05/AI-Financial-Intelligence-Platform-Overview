"""
Cache and rate-limit store.

Unreachable is tolerated — every caller fails open. A *blank* URL is not:
missing falls back to the default, while blank is a string the client rejects
at import, which turns a typo into a startup crash rather than a warning.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from typing import Any


async def get_client() -> Any | None:
    """The shared client, or None when Redis cannot be reached."""
    ...


async def cached_embedding(key: str) -> list[float] | None:
    """A query embedding, keyed on a hash of (model, exact text).

    Exact rather than semantic on purpose: the benchmark contains questions
    that differ by one digit — "the 5 companies with the strongest growth"
    and "the 10" — and have different correct answers.
    """
    ...
