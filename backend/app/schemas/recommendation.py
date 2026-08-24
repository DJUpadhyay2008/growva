from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    location: Optional[str] = "Vadodara, Gujarat"
    soil_type: Optional[str] = "Fertile loam"
    temperature: Optional[float] = None
    rainfall: Optional[float] = None
    ph: Optional[float] = 6.8
    season: Optional[str] = None
    land_area_acres: Optional[float] = 2.0

class ScoreBreakdown(BaseModel):
    climate_suitability: int
    season_suitability: int
    current_conditions: int
    forecast_suitability: int

class RiskBreakdown(BaseModel):
    level: str # LOW, MEDIUM, HIGH
    score: int
    warnings: List[str]

class GrowthStageSchema(BaseModel):
    name: str
    start_day: int
    end_day: int

class CropRecommendationItem(BaseModel):
    crop_name: str
    category: str
    match_score: int # 0 to 100%
    suitability_rating: str # Highly Suitable, Suitable, Moderate
    scores: ScoreBreakdown
    risk: RiskBreakdown
    duration_days: int
    growth_stages: List[GrowthStageSchema]
    reasons: List[str]
    risk_factors: List[str]
    expected_yield: str
    suggested_sowing_window: str
    sowing_status: str # GOOD, WAIT, HEAT_RISK

class RecommendationResponse(BaseModel):
    location: str
    temperature: float
    humidity: float
    rain_probability: float
    rainfall_expected: float
    condition: str
    soil_type: str
    top_recommendations: List[CropRecommendationItem]
    sowing_advisory: str
    is_demo: bool = False
