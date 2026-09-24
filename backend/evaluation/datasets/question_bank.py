"""
Specifications the derived questions are generated from.

A specification says what to ask and how to compute the answer from the
database; it never carries the answer itself, which is why the derived half
must be regenerated after a reseed rather than hand-edited.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionSpec:
    question_id: str
    intent: str                 # VALUATION | GROWTH
    template: str               # the natural-language question
    expected_sql: str           # run against the frozen snapshot to derive truth
    order_requirement: str      # "top_k" | "exact" | "none"
    k: int


VALUATION_SPECS: list[QuestionSpec] = [...]
GROWTH_SPECS: list[QuestionSpec] = [...]
