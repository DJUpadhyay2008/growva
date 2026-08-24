from pydantic import BaseModel
from typing import List, Optional

class SchemeResponse(BaseModel):
    id: int
    code: str
    title: str
    category: str
    short_description: str
    full_description: str
    benefit_amount: str
    eligibility_criteria: str
    required_documents: str
    apply_url: str

    class Config:
        from_attributes = True

class SchemeEligibilityCheckRequest(BaseModel):
    scheme_code: str
    land_holding_acres: float
    is_registered_farmer: bool
    state: str
    category: Optional[str] = "General"

class SchemeEligibilityCheckResponse(BaseModel):
    scheme_code: str
    is_eligible: bool
    status: str
    reasons: List[str]
    documents_needed: List[str]
    next_steps: str
