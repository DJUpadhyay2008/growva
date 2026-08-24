from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.scheme import SchemeResponse, SchemeEligibilityCheckRequest, SchemeEligibilityCheckResponse
from app.services import scheme_service
from typing import List, Optional

router = APIRouter(prefix="/schemes", tags=["Government Schemes"])

@router.get("", response_model=List[SchemeResponse])
def get_schemes(category: Optional[str] = Query(None), db: Session = Depends(get_db)):
    schemes = scheme_service.get_all_schemes(db, category=category)
    return [SchemeResponse.from_orm(s) for s in schemes]

@router.post("/eligibility", response_model=SchemeEligibilityCheckResponse)
def check_eligibility(req: SchemeEligibilityCheckRequest, db: Session = Depends(get_db)):
    return scheme_service.check_scheme_eligibility(db, req)
