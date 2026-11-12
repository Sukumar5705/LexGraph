"""
Case lookup / detail routes.

Will expose endpoints for retrieving a single legal case, its citations,
and its authority/temporal metadata once the data layer is implemented.
"""
from fastapi import APIRouter

router = APIRouter()

# TODO: GET /api/cases/{case_id}          -> case detail
# TODO: GET /api/cases/{case_id}/citations -> citation network for a case
