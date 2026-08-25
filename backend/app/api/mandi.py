from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.market import MarketAnalysisRequest, MarketAnalysisResponse, MandiPriceListResponse, MandiPriceItem
from app.services.market_analysis_service import analyze_market_options
from app.services.market_service import fetch_market_prices_by_commodity

router = APIRouter(prefix="/mandi", tags=["Mandi Prices & Market Intelligence"])

@router.get("", response_model=MandiPriceListResponse)
def get_mandi_prices(
    commodity: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    comm = commodity or "Groundnut"
    items = fetch_market_prices_by_commodity(comm, state_filter=state)
    formatted = []
    for idx, it in enumerate(items[:limit]):
        formatted.append(MandiPriceItem(
            id=idx + 1,
            state=it["state"],
            district=it["district"],
            market=it["market"],
            commodity=it["commodity"],
            variety=it["variety"],
            min_price=float(it["min_price"]),
            max_price=float(it["max_price"]),
            modal_price=float(it["modal_price"]),
            arrival_date=it["arrival_date"],
            latitude=it.get("lat"),
            longitude=it.get("lon"),
            freshness_status=it.get("freshness_status", "Fresh")
        ))
    return MandiPriceListResponse(total=len(formatted), items=formatted)

@router.post("/market-analysis", response_model=MarketAnalysisResponse)
def analyze_mandi_markets(payload: MarketAnalysisRequest):
    return analyze_market_options(
        location_name=payload.location.name,
        crop=payload.crop,
        quantity_quintals=payload.quantity_quintals,
        radius_km=payload.radius_km or 250.0,
        lat=payload.location.latitude,
        lon=payload.location.longitude
    )
