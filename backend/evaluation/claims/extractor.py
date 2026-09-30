"""
Splits an answer into individually checkable factual claims.

A claim is what a reader would have to believe for the sentence to be true,
which is not always a sentence — a ranking sentence carries one claim per
placement.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    index: int
    text: str
    is_numeric: bool
    numeric_values: list[float]


def extract_claims(answer: str) -> list[Claim]:
    """Claims out of prose, in the order they appear."""
    ...
