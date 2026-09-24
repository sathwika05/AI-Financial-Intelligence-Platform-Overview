"""
A ceiling on queries running *at once*, across all callers.

Not a substitute for the per-caller limit: several callers are several
addresses, each inside its own limit, and all their pipelines start together
on one small instance. Surplus work is refused with `Retry-After` rather than
queued — a queued request on a 10-45 second pipeline is a request that will
time out somewhere else instead.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from contextlib import asynccontextmanager


class CapacityExceeded(Exception):
    """Raised instead of waiting. Carries the Retry-After the caller gets."""

    retry_after_seconds: int


@asynccontextmanager
async def occupy_a_slot():
    """Hold one of the concurrent-query slots, or raise CapacityExceeded.

    Process-local. That is the true ceiling on a single instance and bounds
    each task rather than the service once there is more than one, at which
    point the count belongs in Redis.
    """
    ...
