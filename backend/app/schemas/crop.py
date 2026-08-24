from pydantic import BaseModel
from typing import Optional, List

class CropBase(BaseModel):
    name: str
    hindi_name: Optional[str] = None
    gujarati_name: Optional[str] = None
    category: str
    season: str
    soil_type: str
    water_req: str
    duration_days: int = 90
    min_temp: float = 15.0
    max_temp: float = 38.0
    min_rainfall: float = 400.0
    max_rainfall: float = 1500.0
    ideal_ph_min: float = 6.0
    ideal_ph_max: float = 7.5
    expected_yield: str = "Regional estimate"
    image_url: Optional[str] = None
    description: Optional[str] = None
    byproducts: Optional[str] = None
    common_pests: Optional[str] = None

class CropCreate(CropBase):
    pass

class CropResponse(CropBase):
    id: int

    class Config:
        from_attributes = True

class CropListResponse(BaseModel):
    total: int
    showing: int
    items: List[CropResponse]
