from pydantic import BaseModel, Field
from typing import List, Optional

class LocationModel(BaseModel):
    name: str = Field(..., example="Vadodara, Gujarat")
    latitude: Optional[float] = Field(None, example=22.3072)
    longitude: Optional[float] = Field(None, example=73.1812)

class MarketAnalysisRequest(BaseModel):
    location: LocationModel
    crop: str = Field(..., example="Groundnut")
    quantity_quintals: float = Field(10.0, ge=0.1, le=1000.0, example=10.0)
    radius_km: Optional[float] = Field(250.0, ge=10.0, le=1000.0, example=250.0)

class MarketAnalysisItem(BaseModel):
    rank: int
    market: str
    district: str
    state: str
    commodity: str
    variety: str
    modal_price: float
    min_price: float
    max_price: float
    unit: str = "quintal"
    distance_km: float
    transport_cost: float
    transport_cost_per_quintal: float
    gross_revenue: float
    net_realization: float
    net_realization_per_quintal: float
    price_date: str
    freshness_status: str  # "Fresh", "Recent", "Stale", "Demo Data"
    data_source: str
    latitude: float
    longitude: float

class MarketAnalysisResponse(BaseModel):
    crop: str
    farmer_location: str
    farmer_latitude: float
    farmer_longitude: float
    quantity_quintals: float
    radius_km: float
    best_market: MarketAnalysisItem
    markets: List[MarketAnalysisItem]
    potential_additional_realization: float
    baseline_market_name: str
    analysis_summary: str
    is_demo_data: bool = False

class MandiPriceItem(BaseModel):
    id: Optional[int] = None
    state: str
    district: str
    market: str
    commodity: str
    variety: str
    min_price: float
    max_price: float
    modal_price: float
    arrival_date: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    freshness_status: Optional[str] = "Fresh"

class MandiPriceListResponse(BaseModel):
    total: int
    items: List[MandiPriceItem]
