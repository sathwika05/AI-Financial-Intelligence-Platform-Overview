"""
Roles, and what each may reach.

Enforced per router rather than per request handler, so a new endpoint on an
existing router inherits the router's requirement instead of defaulting to
open.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from enum import StrEnum


class Role(StrEnum):
    VIEWER = "viewer"     # read answers
    ANALYST = "analyst"   # ask questions
    ADMIN = "admin"       # configure providers, review escalations, index


def requires(role: Role):
    """FastAPI dependency: reject a caller whose token lacks `role`."""
    ...
