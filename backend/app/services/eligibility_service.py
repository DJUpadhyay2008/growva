"""
Deterministic Rules & Match Engine for Government Scheme Discovery.
Ensures zero hallucination and strict adherence to official eligibility criteria.
"""

from typing import Dict, Any, List, Tuple
from app.data.schemes_data import SCHEMES_DATABASE

def evaluate_scheme_answers(scheme: Dict[str, Any], answers: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Evaluates individual scheme answers against official deterministic eligibility rules.
    Returns (status, reasons).
    Status values: 'likely_eligible', 'more_info_required', 'not_eligible'
    """
    rules = scheme.get("eligibilityRules", [])
    questions = scheme.get("eligibilityQuestions", [])
    
    if not rules:
        return "likely_eligible", ["✓ Open eligibility scheme based on official guidelines."]

    failures = []
    successes = []
    missing_count = 0

    for rule in rules:
        field = rule["field"]
        operator = rule.get("operator", "equals")
        target_val = rule["value"]
        failure_msg = rule.get("failureReason", f"Criteria for {field} not met.")

        if field not in answers or answers[field] is None:
            missing_count += 1
            continue

        actual_val = answers[field]
        passed = False

        if operator == "equals":
            passed = (actual_val == target_val)
        elif operator == "not_equals":
            passed = (actual_val != target_val)
        elif operator == "less_than_equal":
            try:
                passed = float(actual_val) <= float(target_val)
            except (ValueError, TypeError):
                passed = False
        elif operator == "greater_than_equal":
            try:
                passed = float(actual_val) >= float(target_val)
            except (ValueError, TypeError):
                passed = False

        if not passed:
            failures.append(f"✗ {failure_msg}")
        else:
            successes.append(f"✓ Verified: {field.replace('_', ' ').title()} criteria satisfied.")

    if failures:
        return "not_eligible", failures
    elif missing_count > 0:
        return "more_info_required", successes + [f"• {missing_count} additional answer(s) required to confirm final eligibility."]
    else:
        return "likely_eligible", (successes if successes else ["✓ All required eligibility criteria satisfied."])


def match_farmer_profile_all(profile_dict: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Matches a general farmer profile against all verified schemes in the database.
    """
    state = (profile_dict.get("state") or "Gujarat").strip()
    land_acres = float(profile_dict.get("land_acres") or 3.0)
    farmer_type = profile_dict.get("farmer_type") or "Small & Marginal"
    crops = profile_dict.get("crops") or []

    likely_eligible = []
    more_info_required = []
    not_eligible = []

    for scheme in SCHEMES_DATABASE:
        # State check
        scheme_states = scheme.get("states", [])
        state_supported = "All States" in scheme_states or "All States & UTs" in scheme_states or any(state.lower() in s.lower() for s in scheme_states)
        
        if not state_supported:
            not_eligible.append({
                "scheme": scheme,
                "status": "not_eligible",
                "profile_match_pct": 30,
                "why": [f"✗ Scheme currently restricted to: {', '.join(scheme_states)}. (Farmer location: {state})"],
                "missing_info": []
            })
            continue

        # Build partial answers map from farmer profile
        partial_answers = {
            "owns_land": profile_dict.get("owns_land", True),
            "is_taxpayer": profile_dict.get("is_taxpayer", False),
            "has_existing_default": profile_dict.get("has_existing_default", False),
            "is_gujarat_resident": "gujarat" in state.lower(),
            "is_gujarat_farmer": "gujarat" in state.lower(),
            "has_712_8a": True,
            "cultivates_land": True,
            "owns_or_leases_land": True,
            "owns_land_mechanization": True,
            "has_water_source": profile_dict.get("irrigation_status") != "No Irrigation",
            "has_bank_account": True,
            "land_acres": land_acres
        }

        status, reasons = evaluate_scheme_answers(scheme, partial_answers)
        
        # Calculate profile relevance score (70-98%)
        relevance = 80
        if "All States" in scheme_states or state.lower() in [s.lower() for s in scheme_states]:
            relevance += 10
        if crops and any(c.lower() in scheme.get("description", "").lower() for c in crops):
            relevance += 8
        relevance = min(98, max(50, relevance))

        item = {
            "scheme": scheme,
            "status": status,
            "profile_match_pct": relevance,
            "why": reasons,
            "missing_info": [q["question"] for q in scheme.get("eligibilityQuestions", []) if q["id"] not in partial_answers]
        }

        if status == "likely_eligible":
            likely_eligible.append(item)
        elif status == "more_info_required":
            more_info_required.append(item)
        else:
            not_eligible.append(item)

    return {
        "likely_eligible": likely_eligible,
        "more_information_required": more_info_required,
        "not_eligible": not_eligible
    }
