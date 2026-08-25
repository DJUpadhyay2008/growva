from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.market import MarketAnalysisRequest, MarketAnalysisResponse, MandiPriceListResponse, MandiPriceItem
from app.services.market_analysis_service import analyze_market_options
from app.services.market_service import fetch_market_prices_by_commodity

router = APIRouter(prefix="/markets", tags=["Market Intelligence"])

@router.post("/market-analysis", response_model=MarketAnalysisResponse)
def post_market_analysis(payload: MarketAnalysisRequest):
    """
    Core Agronomic Market Intelligence Endpoint:
    Calculates estimated net realization (Gross Revenue - Transport Cost) across candidate APMC markets,
    ranks them, and identifies the best market for maximum financial returns.
    """
    try:
        location_name = payload.location.name
        lat = payload.location.latitude
        lon = payload.location.longitude
        crop = payload.crop
        qty = payload.quantity_quintals
        radius = payload.radius_km or 250.0

        res = analyze_market_options(
            location_name=location_name,
            crop=crop,
            quantity_quintals=qty,
            radius_km=radius,
            lat=lat,
            lon=lon
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market analysis error: {str(e)}")

@router.get("", response_model=MandiPriceListResponse)
def get_markets(
    commodity: Optional[str] = Query(None, description="Crop / commodity name e.g. Groundnut, Wheat"),
    state: Optional[str] = Query(None, description="State filter e.g. Gujarat"),
    limit: int = Query(50, ge=1, le=100)
):
    """Retrieves normalized APMC market prices across commodities."""
    comm = commodity or "Wheat"
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

    return MandiPriceListResponse(
        total=len(formatted),
        items=formatted
    )
