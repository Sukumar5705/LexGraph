"""
Pydantic model(s) for a legal case / precedent record.

Status: SKELETON. Fields are illustrative placeholders based on the planned
knowledge graph schema (see knowledge_graph/schema/nodes.md) and are subject
to change once the final dataset schema is confirmed.
"""
from datetime import date
from typing import Optional
from pydantic import BaseModel


class Case(BaseModel):
    case_id: str
    title: Optional[str] = None
    court: Optional[str] = None
    decision_date: Optional[date] = None
    citation: Optional[str] = None
    # TODO: add authority_score, temporal_status once those modules are implemented
