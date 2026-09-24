"""
Runs a question set and records what happened.

Run-level metrics are written at completion, so a run finished across two
invocations has to be rebuilt from its per-question rows.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class QuestionResult:
    question_id: str
    passed: bool           # every applicable gate passed
    overall_score: float   # weighted, and not what decides `passed`
    evaluator_results: dict
    latency_ms: float
    cost_usd: float | None


async def run_benchmark(
    run_id: UUID,
    question_set: str,       # valuation | growth | sentiment | mixed | smoke | focus | all
    provider_id: UUID,
    rrf_enabled: bool = False,
    cross_encoder_enabled: bool = False,
    llm_blend_weight: float | None = None,
) -> None:
    """Answer every question, grade it, persist it.

    The retrieval switches travel on the run config rather than the
    deployment, so baseline, RRF, cross-encoder and both can be launched as
    four runs and compared against the same questions.
    """
    ...
