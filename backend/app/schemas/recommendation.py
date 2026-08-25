from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    location: Optional[str] = "Vadodara, Gujarat"

class ScoreBreakdown(BaseModel):
    lifecycle_climate: int
    season: int
    current_conditions: int
    forecast: int

class SowingWindowSchema(BaseModel):
    status: str  # "GOOD", "CAUTION", "WAIT"
    recommended_start: str  # e.g. "2026-08-25"
    recommended_end: str    # e.g. "2026-08-29"
    reason: str

class RiskBreakdown(BaseModel):
    level: str  # "LOW", "MEDIUM", "HIGH"
    score: int
    warnings: List[str]

class GrowthStageSchema(BaseModel):
    name: str
    start_day: int
    end_day: int

class CropRecommendationItem(BaseModel):
    crop_name: str
    category: str
    match_score: int
    suitability_rating: str
    scores: ScoreBreakdown
    risk: RiskBreakdown
    sowing_window: SowingWindowSchema
    duration_days: int
    growth_stages: List[GrowthStageSchema]
    reasons: List[str]
    risk_factors: List[str]
    expected_yield: str
    suggested_sowing_window: str
    sowing_status: str

class RecommendationResponse(BaseModel):
    location: str
    season: str  # e.g. "Kharif", "Rabi", "Zaid"
    temperature: float
    humidity: float
    rain_probability: float
    rainfall_expected: float
    condition: str
    top_recommendations: List[CropRecommendationItem]
    sowing_advisory: str
    is_demo: bool = False
