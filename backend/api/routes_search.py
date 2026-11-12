"""
Search API routes.

Runs the existing authority-aware GraphRAG pipeline
and exposes it through the backend API.
"""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.rag_pipeline import RAGPipeline


router = APIRouter()


# =========================================================
# REQUEST MODEL
# =========================================================

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    retrieval_k: int = 20
    reference_date: Optional[str] = "2024-01-01"


# =========================================================
# PIPELINE INSTANCE
# =========================================================

_pipeline = None


def get_pipeline():
    """
    Lazily initialize the RAG pipeline.

    This prevents the heavy models from loading when
    the API module is merely imported.
    """

    global _pipeline

    if _pipeline is None:
        print("[DEBUG] Creating RAGPipeline instance...", flush=True)

        _pipeline = RAGPipeline()

        print("[DEBUG] RAGPipeline instance created.", flush=True)

    return _pipeline


# =========================================================
# SEARCH ENDPOINT
# =========================================================

@router.post("/")
def search(request: SearchRequest):

    query = request.query.strip()

    if not query:
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    if request.top_k < 1:
        raise HTTPException(
            status_code=400,
            detail="top_k must be at least 1.",
        )

    if request.retrieval_k < 1:
        raise HTTPException(
            status_code=400,
            detail="retrieval_k must be at least 1.",
        )

    try:

        print("\n========================================", flush=True)
        print("[DEBUG] SEARCH REQUEST RECEIVED", flush=True)
        print("========================================", flush=True)

        print("[DEBUG] Query:", query, flush=True)
        print("[DEBUG] top_k:", request.top_k, flush=True)
        print("[DEBUG] retrieval_k:", request.retrieval_k, flush=True)
        print("[DEBUG] reference_date:", request.reference_date, flush=True)

        print("\n[DEBUG] Getting pipeline...", flush=True)

        pipeline = get_pipeline()

        print("[DEBUG] Pipeline ready successfully.", flush=True)

        print("\n[DEBUG] Starting pipeline.run()...", flush=True)

        result = pipeline.run(
            query=query,
            top_k=request.top_k,
            retrieval_k=request.retrieval_k,
            reference_date=request.reference_date,
        )

        print("[DEBUG] pipeline.run() finished successfully.", flush=True)

        return {
            "success": True,
            "query": result.get(
                "query",
                query,
            ),
            "answer": result.get(
                "answer",
                "",
            ),
            "sources": result.get(
                "sources",
                [],
            ),
            "relevant_sources": result.get(
                "relevant_sources",
                [],
            ),
            "citation_verification": result.get(
                "citation_verification",
                {},
            ),
            "conflict_report": result.get(
                "conflict_report",
                {},
            ),
            "reference_date": result.get(
                "reference_date",
                request.reference_date,
            ),
        }

    except Exception as exc:

        print(
            "\n========================================",
            flush=True,
        )

        print(
            "SEARCH API ERROR",
            flush=True,
        )

        print(
            "========================================",
            flush=True,
        )

        print(
            repr(exc),
            flush=True,
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )