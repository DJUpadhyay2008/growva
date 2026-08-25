from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class EligibilityQuestion(BaseModel):
    id: str
    type: str  # "boolean", "select", "number", "text"
    question: str
    options: Optional[List[str]] = []
    unit: Optional[str] = None

class EligibilityRule(BaseModel):
    field: str
    operator: str  # "equals", "not_equals", "less_than", "greater_than"
    value: Any
    failureReason: str

class SchemeDetailResponse(BaseModel):
    id: str
    code: str
    name: str
    shortName: Optional[str] = None
    category: str
    categoryLabel: Optional[str] = None
    description: str
    benefits: List[str]
    targetBeneficiaries: List[str]
    states: List[str]
    eligibilityQuestions: List[EligibilityQuestion]
    eligibilityRules: List[EligibilityRule]
    requiredDocuments: List[str]
    applicationSteps: List[str]
    officialWebsite: str
    officialSourceName: str
    sourceLastVerified: str
    active: bool = True

class SchemeCheckSingleRequest(BaseModel):
    scheme_id: str
    answers: Dict[str, Any]  # Keyed by question id, e.g. {"owns_land": true, "is_taxpayer": false}

class SchemeCheckSingleResponse(BaseModel):
    scheme_id: str
    scheme_name: str
    status: str  # "likely_eligible" | "more_info_required" | "not_eligible"
    reasons: List[str]
    required_documents: List[str]
    application_steps: List[str]
    official_website: str

class FarmerProfileRequest(BaseModel):
    state: Optional[str] = "Gujarat"
    district: Optional[str] = "Vadodara"
    farmer_type: Optional[str] = "Small & Marginal"
    land_acres: Optional[float] = 3.0
    irrigation_status: Optional[str] = "Irrigated"
    crops: Optional[List[str]] = ["Groundnut"]
    farmer_category: Optional[str] = "General"
    owns_land: Optional[bool] = True
    is_taxpayer: Optional[bool] = False
    has_existing_default: Optional[bool] = False

class SchemeMatchItem(BaseModel):
    scheme: SchemeDetailResponse
    status: str  # "likely_eligible" | "more_info_required" | "not_eligible"
    profile_match_pct: int
    why: List[str]
    missing_info: Optional[List[str]] = []

class SchemeMatchResponse(BaseModel):
    likely_eligible: List[SchemeMatchItem]
    more_information_required: List[SchemeMatchItem]
    not_eligible: List[SchemeMatchItem]
