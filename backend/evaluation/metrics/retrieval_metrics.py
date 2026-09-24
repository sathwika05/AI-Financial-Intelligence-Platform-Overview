"""
Retrieval quality, measured by coverage rather than by a judge.

How many of the contexts the ground truth cites actually appear in what was
retrieved. Chosen over `context_recall`, which moved 0.289 between two
identical runs and would therefore report noise.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
def context_coverage(retrieved: list[str], cited: list[str]) -> float:
    """Share of cited contexts present in the retrieved set."""
    ...


def evidence_diff(arm_a: list[str], arm_b: list[str]) -> dict[str, list[str]]:
    """What one retrieval arm surfaced that the other did not."""
    ...
