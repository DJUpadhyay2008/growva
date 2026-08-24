from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.mandi import MandiPriceListResponse, MandiPriceResponse
from app.services import mandi_service
from typing import Optional

router = APIRouter(prefix="/mandi", tags=["Mandi Prices"])

@router.get("", response_model=MandiPriceListResponse)
def get_mandi_prices(
    commodity: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    market: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items = mandi_service.get_mandi_prices(db, commodity=commodity, state=state, market=market, limit=limit)
    total = mandi_service.count_mandi_prices(db, commodity=commodity)
    return MandiPriceListResponse(
        total=total,
        items=[MandiPriceResponse.from_orm(item) for item in items]
    )
