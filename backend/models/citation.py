"""
Pydantic model(s) for citation relationships between cases.

Status: SKELETON.
"""
from typing import Optional
from pydantic import BaseModel


class Citation(BaseModel):
    source_case_id: str
    target_case_id: str
    relationship_type: Optional[str] = None  # e.g. "follows", "distinguishes", "overrules"
    # TODO: finalize relationship_type taxonomy in knowledge_graph/schema/relationships.md
