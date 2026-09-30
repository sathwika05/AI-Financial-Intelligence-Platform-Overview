"""
Authored questions — the sentiment half.

Reference answers and reference contexts are written by hand. A model-written
reference would only confirm the model's own output, which is why this half
is never generated the way the valuation and growth sets are.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthoredQuestion:
    question_id: str
    question: str
    expected_intent: str            # SENTIMENT
    reference_answer: str           # written by a human
    reference_contexts: list[str]   # the chunks that answer must rest on
    expected_companies: list[str]


QUESTIONS: list[AuthoredQuestion] = [...]   # 25 of them
