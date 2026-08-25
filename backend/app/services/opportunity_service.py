from app.schemas.byproduct import ScoreFactors

def calculate_growva_opportunity_score(
    availability: int = 90,
    demand: int = 85,
    processing_effort: int = 75,
    local_suitability: int = 85
) -> int:
    """
    Computes explainable Growva Opportunity Score (0-100)
    Weighted Formula:
    - Availability: 25%
    - Market Demand: 35%
    - Processing Ease (Effort): 20%
    - Local / Regional Suitability: 20%
    """
    score = (
        (availability * 0.25) +
        (demand * 0.35) +
        (processing_effort * 0.20) +
        (local_suitability * 0.20)
    )
    return int(round(score))
