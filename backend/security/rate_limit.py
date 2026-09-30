"""
Per-caller request ceiling.

**Fails open.** A cache outage must not become an outage: if Redis cannot be
reached the limiter allows the request and records that it could not count.
The alternative — refusing every caller because the counter is unavailable —
converts a degraded dependency into a total one.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitVerdict:
    allowed: bool
    remaining: int | None      # None when the counter was unreachable
    retry_after_seconds: int | None


async def check_rate_limit(caller_id: str) -> RateLimitVerdict:
    """Count this caller's requests in the current window."""
    ...


async def _increment(key: str, window_seconds: int) -> int | None:
    """Returns None rather than raising when the store is unreachable."""
    ...
