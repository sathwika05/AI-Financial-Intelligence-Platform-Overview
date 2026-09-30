"""
Node-boundary tracing.

LangGraph already opens one run per registered node, so this deliberately
does **not** add a second span per node — it wraps a node to record its
timing and token cost, and leaves the trace hierarchy to LangSmith.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from typing import Any, Callable


def timed_node(name: str, node: Callable) -> Callable:
    """Wrap a node so its latency and tokens land in `node_timings`.

    Changes no node's behaviour. A node that raises still raises.
    """
    ...


def node_span(name: str):
    """Context manager for a sub-node boundary, e.g. one retrieval branch."""
    ...
