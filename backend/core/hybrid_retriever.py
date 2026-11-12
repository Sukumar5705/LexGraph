"""
hybrid_retriever.py

Purpose
-------
Combines lexical (BM25) and vector retrieval results into a single ranked candidate set, prior to knowledge-graph-based re-ranking.

Status: SKELETON ONLY — no implementation yet.
This file intentionally contains no logic, no sample/fake data, and no
hardcoded credentials. Implementation will be added in a later development
phase, once the corresponding design decision has been finalized.
"""


# TODO: Decide on fusion strategy (e.g. reciprocal rank fusion, weighted sum)
# TODO: Integrate with retrieval/bm25/bm25_retriever.py and retrieval/vector/*
# TODO: Define candidate result schema (case_id, score, source)


def not_implemented(*args, **kwargs):
    """Placeholder entry point. Raise until implemented."""
    raise NotImplementedError(f"hybrid_retriever.py is not implemented yet.")
