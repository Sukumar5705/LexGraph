"""
Pydantic model(s) for a search query result returned by the API.

Status: SKELETON.
"""
from typing import List, Optional
from pydantic import BaseModel

from .case import Case


class SearchResult(BaseModel):
    query: str
    results: List[Case] = []
    answer: Optional[str] = None
    conflicts: Optional[list] = None
    # TODO: add authority/temporal explanation fields once those modules exist
