from pydantic import BaseModel, Field
from typing import List, Optional

class Application(BaseModel):
    name: str = Field(..., description="Name of the application/use case")
    category: str = Field(..., description="Category (Biomass, Composting, Animal Feed, Mushroom Cultivation, Industrial Material, Bio-Based Products, Soil Amendment)")
    description: str = Field(..., description="Explanation of why and how this application works")
    processingSteps: List[str] = Field(default_factory=list, description="Sequential processing steps from residue to end product")
    equipment: Optional[List[str]] = Field(default=None, description="Required processing equipment")
    marketChannel: Optional[str] = Field(default=None, description="Potential market/use channel")
    source: Optional[str] = Field(default=None, description="Verified agronomic source")

class ScoreFactors(BaseModel):
    availability: int = Field(..., description="Residue availability score (0-100)")
    demand: int = Field(..., description="Market/application demand score (0-100)")
    processingEffort: int = Field(..., description="Processing ease score (0-100)")
    localSuitability: int = Field(..., description="Regional/local suitability score (0-100)")

class ValueRange(BaseModel):
    min: float
    max: float
    unit: str = "₹ / tonne"

class ByProduct(BaseModel):
    id: str
    sourceCrop: str = Field(..., description="Primary crop producing this residue")
    residueName: str = Field(..., description="Name of the residue (e.g. Rice Straw, Sugarcane Bagasse)")
    description: str = Field(..., description="Overview of the residue")
    applications: List[Application] = Field(..., description="List of verified applications")
    residueFactor: Optional[float] = Field(None, description="Residue-to-crop yield ratio (e.g., 1.4 tonnes straw per tonne grain)")
    residueFactorSource: Optional[str] = Field(None, description="Verified agricultural data source for residue factor")
    processingDifficulty: str = Field("medium", description="low, medium, or high")
    requiredProcessing: Optional[List[str]] = Field(default_factory=list, description="Required processing techniques")
    demandLevel: str = Field("medium", description="low, medium, or high")
    opportunityScore: int = Field(80, description="Growva Opportunity Score (0-100)")
    scoreFactors: ScoreFactors
    valueRange: Optional[ValueRange] = None
    valueSource: Optional[str] = None
    lastVerified: Optional[str] = "Aug 2026"

class ResidueAnalysisRequest(BaseModel):
    crop: str = Field(..., description="Crop name (e.g. Rice, Wheat, Sugarcane, Groundnut)")
    area_acres: float = Field(3.0, description="Farm land area in acres")
    expected_yield_tonnes: Optional[float] = Field(None, description="Expected crop harvest yield in tonnes")
    location: Optional[str] = Field("Vadodara, Gujarat", description="Farmer district/location")

class ResidueAnalysisResponse(BaseModel):
    crop: str
    residue_id: str
    residue_name: str
    farm_area_acres: float
    estimated_production_tonnes: float
    yield_source: str
    residue_factor: float
    residue_factor_source: str
    estimated_residue_tonnes: float
    opportunity_score: int
    score_factors: ScoreFactors
    top_opportunity: Application
    opportunities: List[Application]
    processing_difficulty: str
    processing_requirements: List[str]
    potential_value_display: str
    location: str
