from typing import List, Optional
from app.data.byproducts_data import BYPRODUCTS_DATABASE, CROP_TO_BYPRODUCT_MAP
from app.schemas.byproduct import ByProduct, ResidueAnalysisRequest, ResidueAnalysisResponse
from app.services.residue_estimator import estimate_crop_residue
from app.services.opportunity_service import calculate_growva_opportunity_score

def get_all_byproducts(
    search: Optional[str] = None,
    crop: Optional[str] = None,
    category: Optional[str] = None,
    difficulty: Optional[str] = None
) -> List[ByProduct]:
    results = BYPRODUCTS_DATABASE

    if search:
        q = search.lower().strip()
        filtered = []
        for item in results:
            match_name = q in item.residueName.lower()
            match_crop = q in item.sourceCrop.lower()
            match_desc = q in item.description.lower()
            match_app = any(
                q in app.name.lower() or q in app.category.lower() or q in app.description.lower()
                for app in item.applications
            )
            if match_name or match_crop or match_desc or match_app:
                filtered.append(item)
        results = filtered

    if crop and crop.strip() and crop.lower() != "all":
        c = crop.lower().strip()
        results = [item for item in results if c in item.sourceCrop.lower() or item.sourceCrop.lower() in c]

    if category and category.strip() and category.lower() != "all":
        cat = category.lower().strip()
        results = [
            item for item in results
            if any(cat in app.category.lower() for app in item.applications)
        ]

    if difficulty and difficulty.strip() and difficulty.lower() != "all":
        diff = difficulty.lower().strip()
        results = [item for item in results if item.processingDifficulty.lower() == diff]

    return results

def get_byproduct_by_id(byproduct_id: str) -> Optional[ByProduct]:
    for item in BYPRODUCTS_DATABASE:
        if item.id == byproduct_id:
            return item
    return None

def get_byproduct_by_crop(crop_name: str) -> Optional[ByProduct]:
    c_lower = crop_name.lower().strip()
    target_id = CROP_TO_BYPRODUCT_MAP.get(c_lower)
    if target_id:
        return get_byproduct_by_id(target_id)

    for item in BYPRODUCTS_DATABASE:
        if item.sourceCrop.lower() in c_lower or c_lower in item.sourceCrop.lower():
            return item

    return BYPRODUCTS_DATABASE[0] # Default fallback

def analyze_crop_byproduct(req: ResidueAnalysisRequest) -> ResidueAnalysisResponse:
    item = get_byproduct_by_crop(req.crop)

    # Estimate quantity
    est = estimate_crop_residue(
        crop_name=req.crop,
        area_acres=req.area_acres,
        user_expected_yield=req.expected_yield_tonnes,
        residue_factor=item.residueFactor or 1.4,
        residue_factor_source=item.residueFactorSource or "ICAR Agricultural Residue Ratios"
    )

    opp_score = calculate_growva_opportunity_score(
        availability=item.scoreFactors.availability,
        demand=item.scoreFactors.demand,
        processing_effort=item.scoreFactors.processingEffort,
        local_suitability=item.scoreFactors.localSuitability
    )

    top_app = item.applications[0] if item.applications else None

    val_display = (
        f"₹{item.valueRange.min:,.0f} – ₹{item.valueRange.max:,.0f} / tonne ({item.valueRange.unit})"
        if item.valueRange else "Market value varies by location & quality"
    )

    return ResidueAnalysisResponse(
        crop=req.crop,
        residue_id=item.id,
        residue_name=item.residueName,
        farm_area_acres=est["farm_area_acres"],
        estimated_production_tonnes=est["estimated_production_tonnes"],
        yield_source=est["yield_source"],
        residue_factor=est["residue_factor"],
        residue_factor_source=est["residue_factor_source"],
        estimated_residue_tonnes=est["estimated_residue_tonnes"],
        opportunity_score=opp_score,
        score_factors=item.scoreFactors,
        top_opportunity=top_app,
        opportunities=item.applications,
        processing_difficulty=item.processingDifficulty,
        processing_requirements=item.requiredProcessing or [],
        potential_value_display=val_display,
        location=req.location or "Vadodara, Gujarat"
    )
