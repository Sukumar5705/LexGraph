"""
Health check route(s).
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health_check():
    """Basic liveness check. Extend later with DB / vector-store checks."""
    return {"status": "ok"}
