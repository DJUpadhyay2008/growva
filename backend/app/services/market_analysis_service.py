import math
from typing import Dict, Any, List
from app.services.location_service import resolve_location
from app.services.transport_service import estimate_transport_cost
from app.services.market_service import fetch_market_prices_by_commodity, normalize_commodity_name
from app.schemas.market import MarketAnalysisResponse, MarketAnalysisItem

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates geodesic distance between two latitude/longitude points in kilometers."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 1)

def analyze_market_options(
    location_name: str,
    crop: str,
    quantity_quintals: float = 10.0,
    radius_km: float = 250.0,
    lat: float = None,
    lon: float = None
) -> Dict[str, Any]:
    """
    Core Intelligence Engine:
    Ranks nearby APMC markets based on Estimated Net Realization (Gross Revenue minus Logistics/Transport Cost).
    """
    # 1. Resolve Farmer Location
    loc_data = resolve_location(location_name, lat=lat, lon=lon)
    farmer_lat = loc_data["lat"]
    farmer_lon = loc_data["lon"]
    formatted_location = loc_data["name"]

    # 2. Fetch Raw Market Prices for Crop
    normalized_crop = normalize_commodity_name(crop)
    raw_markets = fetch_market_prices_by_commodity(normalized_crop)

    # 3. Calculate Distance, Transport Cost & Net Realization for Each Market
    evaluated_markets = []

    for item in raw_markets:
        m_lat = item["lat"]
        m_lon = item["lon"]
        dist = calculate_haversine_distance(farmer_lat, farmer_lon, m_lat, m_lon)

        # Estimate Transport Cost
        trans = estimate_transport_cost(dist, quantity_quintals)
        total_trans_cost = trans["total_transport_cost"]
        trans_cost_per_q = trans["transport_cost_per_quintal"]

        # Calculate Financial Metrics
        modal = float(item["modal_price"])
        gross_rev = round(modal * quantity_quintals, 2)
        net_realization = round(gross_rev - total_trans_cost, 2)
        net_per_q = round(net_realization / max(1.0, quantity_quintals), 2)

        evaluated_markets.append({
            "market": item["market"],
            "district": item["district"],
            "state": item["state"],
            "commodity": normalized_crop,
            "variety": item["variety"],
            "modal_price": modal,
            "min_price": float(item["min_price"]),
            "max_price": float(item["max_price"]),
            "unit": "quintal",
            "distance_km": dist,
            "transport_cost": total_trans_cost,
            "transport_cost_per_quintal": trans_cost_per_q,
            "gross_revenue": gross_rev,
            "net_realization": net_realization,
            "net_realization_per_quintal": net_per_q,
            "price_date": item["arrival_date"],
            "freshness_status": item.get("freshness_status", "Fresh"),
            "data_source": item.get("source", "AGMARKNET / Official APMC"),
            "latitude": m_lat,
            "longitude": m_lon
        })

    # 4. Filter by Radius (Expand dynamically if radius is too small)
    filtered_markets = [m for m in evaluated_markets if m["distance_km"] <= radius_km]
    if len(filtered_markets) < 2:
        # Fallback to all evaluated markets so comparison is always available
        filtered_markets = evaluated_markets

    # 5. Rank Markets by Estimated Net Realization (Descending)
    filtered_markets.sort(key=lambda x: x["net_realization"], reverse=True)

    # Assign Ranks
    ranked_items = []
    for idx, item in enumerate(filtered_markets):
        item["rank"] = idx + 1
        ranked_items.append(MarketAnalysisItem(**item))

    best_market = ranked_items[0]

    # Find Nearest / Baseline Local Market for comparison
    nearest_market = min(ranked_items, key=lambda x: x.distance_km)
    baseline_market_name = nearest_market.market

    potential_addl = 0.0
    if best_market.market != nearest_market.market:
        potential_addl = round(best_market.net_realization - nearest_market.net_realization, 2)

    # 6. Generate Contextual Intelligence Summary
    if best_market.market == nearest_market.market:
        summary = (
            f"The nearest mandi ({best_market.market}, {best_market.distance_km} km away) yields the highest "
            f"estimated net realization of ₹{best_market.net_realization:,.0f} for {quantity_quintals} quintals of {normalized_crop}. "
            f"Selling locally minimizes transport overhead."
        )
    else:
        summary = (
            f"{best_market.market} is the optimal choice with a higher modal price of ₹{best_market.modal_price:,.0f}/quintal. "
            f"Although it is {best_market.distance_km} km away, the price premium generates an estimated additional net realization "
            f"of +₹{potential_addl:,.0f} compared to selling locally at {nearest_market.market} ({nearest_market.distance_km} km)."
        )

    return {
        "crop": normalized_crop,
        "farmer_location": formatted_location,
        "farmer_latitude": farmer_lat,
        "farmer_longitude": farmer_lon,
        "quantity_quintals": quantity_quintals,
        "radius_km": radius_km,
        "best_market": best_market,
        "markets": ranked_items,
        "potential_additional_realization": potential_addl,
        "baseline_market_name": baseline_market_name,
        "analysis_summary": summary,
        "is_demo_data": False
    }
