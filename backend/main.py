"""
FastAPI application entry point.

Status: SKELETON. Routes are registered but their internal logic is not
yet implemented (see backend/api/*).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.api import (
    routes_search,
    routes_cases,
    routes_graph,
    routes_health,
)

settings = get_settings()

app = FastAPI(
    title="Authority- and Temporal-Aware GraphRAG for Indian Legal Precedent Retrieval",
    description="Backend API skeleton. Implementation pending.",
    version="0.0.1",
)

# CORS — tighten allow_origins before production use.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix="/api/health", tags=["health"])
app.include_router(routes_search.router, prefix="/api/search", tags=["search"])
app.include_router(routes_cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(routes_graph.router, prefix="/api/graph", tags=["graph"])


@app.get("/")
def root():
    return {
        "project": "Authority- and Temporal-Aware GraphRAG",
        "status": "skeleton",
        "message": "Backend is running. Endpoints are not yet implemented.",
    }
