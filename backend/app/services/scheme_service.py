"""
Scheme Service for querying government schemes and executing eligibility checks.
"""

from typing import List, Dict, Any, Optional
from app.data.schemes_data import SCHEMES_DATABASE
from app.services.eligibility_service import evaluate_scheme_answers, match_farmer_profile_all

def get_all_schemes(category: Optional[str] = None, state: Optional[str] = None) -> List[Dict[str, Any]]:
    results = SCHEMES_DATABASE
    if category and category.lower() != 'all':
        results = [s for s in results if category.lower() in s.get("category", "").lower() or category.lower() in s.get("categoryLabel", "").lower()]
    if state and state.lower() != 'all':
        results = [
            s for s in results 
            if "All States" in s.get("states", []) or "All States & UTs" in s.get("states", []) or any(state.lower() in st.lower() for st in s.get("states", []))
        ]
    return results

def get_scheme_by_id(scheme_id: str) -> Optional[Dict[str, Any]]:
    for s in SCHEMES_DATABASE:
        if s["id"].lower() == scheme_id.lower() or s["code"].lower() == scheme_id.lower():
            return s
    return None

def check_single_scheme_eligibility(scheme_id: str, answers: Dict[str, Any]) -> Dict[str, Any]:
    scheme = get_scheme_by_id(scheme_id)
    if not scheme:
        return {
            "scheme_id": scheme_id,
            "scheme_name": "Unknown Scheme",
            "status": "not_eligible",
            "reasons": ["Scheme record not found in verified database."],
            "required_documents": [],
            "application_steps": [],
            "official_website": "https://myscheme.gov.in"
        }
    
    status, reasons = evaluate_scheme_answers(scheme, answers)
    return {
        "scheme_id": scheme["id"],
        "scheme_name": scheme["name"],
        "status": status,
        "reasons": reasons,
        "required_documents": scheme.get("requiredDocuments", []),
        "application_steps": scheme.get("applicationSteps", []),
        "official_website": scheme.get("officialWebsite", "https://myscheme.gov.in")
    }

def match_schemes_for_farmer(profile: Dict[str, Any]) -> Dict[str, Any]:
    return match_farmer_profile_all(profile)
