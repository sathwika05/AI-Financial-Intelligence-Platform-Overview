"""
Grades generated SQL two ways.

Row accuracy against the expected result set is the primary signal; semantic
equivalence of the query text is secondary, because two correct queries can
differ in text and an identical query can be correct by accident.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from dataclasses import dataclass

WEIGHTS = {"sql_accuracy": 0.75, "sql_equivalence": 0.25}


@dataclass(frozen=True)
class SqlEvaluation:
    passed: bool
    sql_accuracy: float | None       # row-level F1 against expected
    sql_equivalence: float | None    # judged, not string-compared
    read_only: bool
    errors: list[str]


def evaluate_sql(generated: str | None, expected: str, rows, expected_rows) -> SqlEvaluation:
    """A missing query fails regardless of whether the rows came back right."""
    ...
