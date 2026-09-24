"""
Company ranking.

Four normalized dimensions, weighted by which sources actually returned data.
A dimension with no data is reported as `unmeasured` rather than scored zero —
scoring it zero is a claim that the company did badly, which is not what a
missing source means.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from typing import Any

from langchain_core.runnables import RunnableConfig

Dimension = str  # "valuation" | "growth" | "relevance" | "sentiment"

# How much of the final ranking is the model's holistic opinion rather than
# the computed dimensions. Made a per-run parameter so an ablation could
# decide it; see docs/BENCHMARKS.md for what the ablation found.
DEFAULT_LLM_BLEND_WEIGHT: float = 0.3


def score_company_valuation(company: dict[str, Any]) -> float | None:
    """0-1 from P/E and price momentum. None when neither is present."""
    ...


def score_company_growth(company: dict[str, Any]) -> float | None:
    """0-1 from revenue growth and the sign of EPS."""
    ...


def blend_llm_score(computed: float, llm: float | None, weight: float) -> float:
    """Combine the computed composite with the model's own score."""
    ...


async def rank_companies(
    companies: list[dict[str, Any]],
    intent: str,
    config: RunnableConfig,
) -> list[dict[str, Any]]:
    """Rank, attach evidence, and explain each placement."""
    ...
