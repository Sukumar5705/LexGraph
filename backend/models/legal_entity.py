"""
Pydantic model(s) for legal entities extracted from case text
(e.g. statutes, sections, courts, judges).

Status: SKELETON.
"""
from typing import Optional
from pydantic import BaseModel


class LegalEntity(BaseModel):
    entity_id: str
    entity_type: Optional[str] = None  # e.g. "statute", "section", "court", "judge"
    name: Optional[str] = None
    # TODO: finalize entity taxonomy alongside knowledge_graph/schema/nodes.md
