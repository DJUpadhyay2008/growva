from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Optional, Dict, Any
from app.services import scheme_service

router = APIRouter(prefix="/schemes", tags=["Government Schemes"])

@router.get("")
def get_schemes(category: Optional[str] = Query(None), state: Optional[str] = Query(None)):
    """Retrieve all verified government schemes with category and state filters."""
    return scheme_service.get_all_schemes(category=category, state=state)

@router.get("/{scheme_id}")
def get_scheme_detail(scheme_id: str):
    """Retrieve a single detailed government scheme object."""
    scheme = scheme_service.get_scheme_by_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.post("/{scheme_id}/eligibility")
def check_scheme_eligibility(scheme_id: str, payload: Dict[str, Any] = Body(...)):
    """Evaluate farmer answers against scheme-specific deterministic rules."""
    answers = payload.get("answers", payload)
    return scheme_service.check_single_scheme_eligibility(scheme_id, answers)

@router.post("/match")
def match_schemes_for_profile(profile: Dict[str, Any] = Body(...)):
    """Match a farmer profile against the entire database of verified schemes."""
    return scheme_service.match_schemes_for_farmer(profile)
