"""
The pipeline graph. Wiring only — node bodies are private.

    intent → planner → retrieval → scoring → [reranker] → analysis → reviewer

Two edges carry most of the design:

- **intent can exit to END.** A greeting is answered in about a second rather
  than researched for forty.
- **the reviewer loops back to analysis, not retrieval.** By that point the
  query, the cohort and the corpus are fixed, so re-retrieving returns the same
  documents and raises the same flags. What can differ is the draft, because
  the rejected claims are handed back to the analysis prompt.
"""
from langgraph.graph import END, START, StateGraph

from backend.state.financial_state import FinancialState


def build_financial_graph():
    graph = StateGraph(FinancialState)

    # Every node is registered through a timing wrapper so the evaluation
    # dashboard can break latency down per stage. The wrapper changes no
    # node's behaviour.
    for name, node in (
        ("intent", intent_node),
        ("planner", planner_node),
        ("retrieval", retrieval_node),
        ("reranker", reranker_node),
        ("scoring", scoring_node),
        ("analysis", analysis_node),
        ("reviewer", reviewer_node),
    ):
        graph.add_node(name, timed_node(name, node))

    graph.add_edge(START, "intent")

    graph.add_conditional_edges(
        "intent",
        route_after_intent,
        {
            "planner": "planner",
            "output": END,          # not a research question -> stop here
        },
    )

    graph.add_edge("planner", "retrieval")
    graph.add_edge("retrieval", "scoring")

    graph.add_conditional_edges(
        "scoring",
        route_after_scoring,
        {
            "reranker": "reranker",  # narrative evidence to reorder
            "analysis": "analysis",  # columns only, nothing to rerank
        },
    )

    graph.add_edge("reranker", "analysis")
    graph.add_edge("analysis", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "analysis": "analysis",  # ungrounded claims -> redraft
            "output": END,           # approved, forced through, or withheld
        },
    )

    # Compiled with a checkpointer, so a run's state stays addressable by
    # thread_id after it finishes rather than being discarded.
    return graph.compile(checkpointer=build_checkpointer())
