"""
Checkpointer construction.

Graphs compile with one so a run's state stays addressable by `thread_id`
after the invocation returns, rather than being discarded with it.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from typing import Any


def build_checkpointer() -> Any:
    """The checkpointer every graph compiles with."""
    ...
