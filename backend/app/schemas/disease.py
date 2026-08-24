from pydantic import BaseModel
from typing import List, Optional

class DiseaseDiagnosisRequest(BaseModel):
    crop_name: str
    symptoms_text: str
    affected_part: Optional[str] = "leaves" # leaves, stem, fruit, root

class DiseaseDiagnosisResponse(BaseModel):
    crop_name: str
    diagnosed_disease: str
    confidence_score: float
    symptoms_matched: List[str]
    organic_treatment: str
    chemical_treatment: str
    preventive_measures: str
