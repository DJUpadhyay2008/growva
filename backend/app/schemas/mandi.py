from pydantic import BaseModel
from typing import List, Optional

class MandiPriceResponse(BaseModel):
    id: int
    state: str
    district: str
    market: str
    commodity: str
    variety: Optional[str] = None
    min_price: float
    max_price: float
    modal_price: float
    arrival_date: str

    class Config:
        from_attributes = True

class MandiPriceListResponse(BaseModel):
    total: int
    items: List[MandiPriceResponse]
