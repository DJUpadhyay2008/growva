from sqlalchemy.orm import Session
from app.database.models import GovernmentSchemeModel
from app.schemas.scheme import SchemeEligibilityCheckRequest, SchemeEligibilityCheckResponse
from typing import List, Optional

def get_all_schemes(db: Session, category: Optional[str] = None) -> List[GovernmentSchemeModel]:
    q = db.query(GovernmentSchemeModel)
    if category and category.lower() != 'all':
        q = q.filter(GovernmentSchemeModel.category.ilike(f"%{category}%"))
    return q.all()

def check_scheme_eligibility(db: Session, req: SchemeEligibilityCheckRequest) -> SchemeEligibilityCheckResponse:
    scheme = db.query(GovernmentSchemeModel).filter(GovernmentSchemeModel.code.ilike(req.scheme_code)).first()
    
    if not scheme:
        return SchemeEligibilityCheckResponse(
            scheme_code=req.scheme_code,
            is_eligible=False,
            status="Scheme Not Found",
            reasons=["The requested scheme code is not recognized."],
            documents_needed=[],
            next_steps="Please check the scheme code and try again."
        )

    is_eligible = True
    reasons = []
    
    if not req.is_registered_farmer:
        is_eligible = False
        reasons.append("Land registration / Farmer ID verification is required.")
    else:
        reasons.append("Farmer registration status verified.")

    if req.land_holding_acres > 15 and req.scheme_code == "PM-KISAN":
        is_eligible = False
        reasons.append("PM-KISAN targets small and marginal landholding farmers.")
    else:
        reasons.append("Land holding criteria satisfied.")

    docs = [d.strip() for d in scheme.required_documents.split(",") if d.strip()]

    return SchemeEligibilityCheckResponse(
        scheme_code=scheme.code,
        is_eligible=is_eligible,
        status="Eligible for Subsidy" if is_eligible else "Action Required",
        reasons=reasons,
        documents_needed=docs,
        next_steps=f"Visit {scheme.apply_url} or your local Krishi Vigyan Kendra to submit application."
    )
