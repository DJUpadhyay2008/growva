from typing import Dict, Any, List
import math

# Historical Monthly Climate Data Generator for Indian Agro-Climatic Regions
def get_historical_monthly_climate(location: str, lat: float = 22.3, lon: float = 73.2) -> List[Dict[str, float]]:
    """
    Returns 12-month historical climate averages (temp_c, rainfall_mm, humidity_pct)
    based on geographic coordinates and location profile.
    Months indexed 1 to 12 (Jan to Dec).
    """
    loc_lower = location.lower()
    
    # 1. Cold Himalayan / High Altitude (Amarnath, Srinagar, Leh, Shimla, Manali)
    if any(k in loc_lower for k in ["amarnath", "srinagar", "leh", "shimla", "manali", "ladakh", "kashmir"]):
        return [
            {"month": 1, "temp_c": -1.5, "rainfall_mm": 55.0, "humidity_pct": 80.0},
            {"month": 2, "temp_c": 1.0, "rainfall_mm": 65.0, "humidity_pct": 78.0},
            {"month": 3, "temp_c": 6.5, "rainfall_mm": 80.0, "humidity_pct": 72.0},
            {"month": 4, "temp_c": 12.0, "rainfall_mm": 60.0, "humidity_pct": 65.0},
            {"month": 5, "temp_c": 17.5, "rainfall_mm": 50.0, "humidity_pct": 60.0},
            {"month": 6, "temp_c": 21.0, "rainfall_mm": 45.0, "humidity_pct": 62.0},
            {"month": 7, "temp_c": 23.5, "rainfall_mm": 130.0, "humidity_pct": 75.0},
            {"month": 8, "temp_c": 22.8, "rainfall_mm": 120.0, "humidity_pct": 78.0},
            {"month": 9, "temp_c": 18.5, "rainfall_mm": 50.0, "humidity_pct": 70.0},
            {"month": 10, "temp_c": 12.5, "rainfall_mm": 25.0, "humidity_pct": 68.0},
            {"month": 11, "temp_c": 6.0, "rainfall_mm": 20.0, "humidity_pct": 72.0},
            {"month": 12, "temp_c": 1.0, "rainfall_mm": 40.0, "humidity_pct": 76.0},
        ]

    # 2. Arid / Desert Western Rajasthan (Jaisalmer, Barmer, Bikaner, Jodhpur)
    if any(k in loc_lower for k in ["jaisalmer", "barmer", "bikaner", "jodhpur", "desert"]):
        return [
            {"month": 1, "temp_c": 15.0, "rainfall_mm": 3.0, "humidity_pct": 42.0},
            {"month": 2, "temp_c": 18.5, "rainfall_mm": 4.0, "humidity_pct": 38.0},
            {"month": 3, "temp_c": 24.5, "rainfall_mm": 3.0, "humidity_pct": 32.0},
            {"month": 4, "temp_c": 31.0, "rainfall_mm": 5.0, "humidity_pct": 28.0},
            {"month": 5, "temp_c": 35.5, "rainfall_mm": 8.0, "humidity_pct": 26.0},
            {"month": 6, "temp_c": 36.0, "rainfall_mm": 25.0, "humidity_pct": 40.0},
            {"month": 7, "temp_c": 33.5, "rainfall_mm": 90.0, "humidity_pct": 58.0},
            {"month": 8, "temp_c": 31.8, "rainfall_mm": 85.0, "humidity_pct": 62.0},
            {"month": 9, "temp_c": 31.0, "rainfall_mm": 30.0, "humidity_pct": 52.0},
            {"month": 10, "temp_c": 27.5, "rainfall_mm": 5.0, "humidity_pct": 40.0},
            {"month": 11, "temp_c": 21.5, "rainfall_mm": 2.0, "humidity_pct": 38.0},
            {"month": 12, "temp_c": 16.5, "rainfall_mm": 2.0, "humidity_pct": 42.0},
        ]

    # 3. High Rainfall Coastal / Southern (Kochi, Kerala, Assam, Goa, Konkan)
    if any(k in loc_lower for k in ["kochi", "kerala", "assam", "guwahati", "goa", "konkan", "trivandrum"]):
        return [
            {"month": 1, "temp_c": 27.0, "rainfall_mm": 20.0, "humidity_pct": 72.0},
            {"month": 2, "temp_c": 28.0, "rainfall_mm": 25.0, "humidity_pct": 74.0},
            {"month": 3, "temp_c": 29.5, "rainfall_mm": 40.0, "humidity_pct": 75.0},
            {"month": 4, "temp_c": 30.0, "rainfall_mm": 110.0, "humidity_pct": 78.0},
            {"month": 5, "temp_c": 29.5, "rainfall_mm": 280.0, "humidity_pct": 82.0},
            {"month": 6, "temp_c": 27.0, "rainfall_mm": 650.0, "humidity_pct": 92.0},
            {"month": 7, "temp_c": 26.5, "rainfall_mm": 580.0, "humidity_pct": 94.0},
            {"month": 8, "temp_c": 26.8, "rainfall_mm": 380.0, "humidity_pct": 90.0},
            {"month": 9, "temp_c": 27.2, "rainfall_mm": 240.0, "humidity_pct": 86.0},
            {"month": 10, "temp_c": 27.5, "rainfall_mm": 300.0, "humidity_pct": 84.0},
            {"month": 11, "temp_c": 27.2, "rainfall_mm": 180.0, "humidity_pct": 80.0},
            {"month": 12, "temp_c": 27.0, "rainfall_mm": 40.0, "humidity_pct": 75.0},
        ]

    # 4. Northern Indo-Gangetic Plains (Ludhiana, Punjab, Haryana, UP, Delhi)
    if any(k in loc_lower for k in ["ludhiana", "punjab", "haryana", "delhi", "kanpur", "lucknow", "patna"]):
        return [
            {"month": 1, "temp_c": 12.5, "rainfall_mm": 25.0, "humidity_pct": 75.0},
            {"month": 2, "temp_c": 15.8, "rainfall_mm": 30.0, "humidity_pct": 70.0},
            {"month": 3, "temp_c": 21.5, "rainfall_mm": 25.0, "humidity_pct": 58.0},
            {"month": 4, "temp_c": 28.0, "rainfall_mm": 15.0, "humidity_pct": 42.0},
            {"month": 5, "temp_c": 33.5, "rainfall_mm": 20.0, "humidity_pct": 36.0},
            {"month": 6, "temp_c": 35.0, "rainfall_mm": 70.0, "humidity_pct": 50.0},
            {"month": 7, "temp_c": 31.5, "rainfall_mm": 230.0, "humidity_pct": 78.0},
            {"month": 8, "temp_c": 30.5, "rainfall_mm": 210.0, "humidity_pct": 82.0},
            {"month": 9, "temp_c": 29.5, "rainfall_mm": 110.0, "humidity_pct": 75.0},
            {"month": 10, "temp_c": 25.0, "rainfall_mm": 15.0, "humidity_pct": 62.0},
            {"month": 11, "temp_c": 19.0, "rainfall_mm": 8.0, "humidity_pct": 65.0},
            {"month": 12, "temp_c": 14.0, "rainfall_mm": 15.0, "humidity_pct": 72.0},
        ]

    # 5. Default Central & Western Plains (Vadodara, Ahmedabad, Rajkot, Pune, MP, MH)
    return [
        {"month": 1, "temp_c": 20.5, "rainfall_mm": 2.0, "humidity_pct": 52.0},
        {"month": 2, "temp_c": 23.0, "rainfall_mm": 1.0, "humidity_pct": 45.0},
        {"month": 3, "temp_c": 27.8, "rainfall_mm": 3.0, "humidity_pct": 38.0},
        {"month": 4, "temp_c": 31.5, "rainfall_mm": 4.0, "humidity_pct": 35.0},
        {"month": 5, "temp_c": 33.8, "rainfall_mm": 12.0, "humidity_pct": 48.0},
        {"month": 6, "temp_c": 32.0, "rainfall_mm": 140.0, "humidity_pct": 68.0},
        {"month": 7, "temp_c": 29.0, "rainfall_mm": 320.0, "humidity_pct": 84.0},
        {"month": 8, "temp_c": 28.2, "rainfall_mm": 280.0, "humidity_pct": 86.0},
        {"month": 9, "temp_c": 28.8, "rainfall_mm": 150.0, "humidity_pct": 80.0},
        {"month": 10, "temp_c": 28.0, "rainfall_mm": 30.0, "humidity_pct": 62.0},
        {"month": 11, "temp_c": 24.5, "rainfall_mm": 10.0, "humidity_pct": 55.0},
        {"month": 12, "temp_c": 21.5, "rainfall_mm": 2.0, "humidity_pct": 54.0},
    ]


def calculate_lifecycle_climate_score(
    location: str,
    start_month: int,
    duration_days: int,
    crop_min_temp: float,
    crop_max_temp: float,
    crop_min_rainfall: float,
    crop_max_rainfall: float,
    water_req_str: str
) -> int:
    """
    Calculates the Lifecycle Climate Score over the full growth duration (90 to 180+ days)
    by evaluating historical monthly climate data for the location.
    """
    months_count = max(1, math.ceil(duration_days / 30.0))
    monthly_data = get_historical_monthly_climate(location)
    
    growing_months = []
    curr_m = start_month
    for _ in range(months_count):
        # find matching month (1-12)
        m_idx = ((curr_m - 1) % 12) + 1
        m_item = next((item for item in monthly_data if item["month"] == m_idx), monthly_data[0])
        growing_months.append(m_item)
        curr_m += 1

    # 1. Temperature suitability over lifecycle
    temp_scores = []
    for m in growing_months:
        avg_t = m["temp_c"]
        if crop_min_temp <= avg_t <= crop_max_temp:
            temp_scores.append(98)
        elif avg_t < crop_min_temp:
            diff = crop_min_temp - avg_t
            if diff > 10.0:
                temp_scores.append(max(5, int(40 - diff * 3.0)))
            else:
                temp_scores.append(max(15, int(85 - diff * 6.5)))
        else:
            diff = avg_t - crop_max_temp
            if diff > 8.0:
                temp_scores.append(max(5, int(45 - diff * 4.0)))
            else:
                temp_scores.append(max(20, int(85 - diff * 6.5)))
    
    avg_temp_score = sum(temp_scores) / len(temp_scores)

    # 2. Cumulative rainfall suitability over lifecycle
    total_historical_rainfall = sum(m["rainfall_mm"] for m in growing_months)
    if crop_min_rainfall <= total_historical_rainfall <= crop_max_rainfall:
        rainfall_score = 96
    elif total_historical_rainfall < crop_min_rainfall:
        shortfall = crop_min_rainfall - total_historical_rainfall
        rainfall_score = max(10, int(92 - (shortfall / max(1.0, crop_min_rainfall)) * 75))
    else:
        excess = total_historical_rainfall - crop_max_rainfall
        rainfall_score = max(25, int(92 - (excess / max(1.0, crop_max_rainfall)) * 50))

    # 3. Average humidity suitability over lifecycle
    avg_humidity = sum(m["humidity_pct"] for m in growing_months) / len(growing_months)
    w_req = water_req_str.lower()
    if "very high" in w_req or "high" in w_req:
        humidity_score = 95 if avg_humidity >= 65 else max(20, int(95 - (65 - avg_humidity) * 2.0))
    elif "low" in w_req:
        humidity_score = 95 if avg_humidity <= 60 else max(20, int(95 - (avg_humidity - 60) * 2.0))
    else:
        humidity_score = 92 if 45 <= avg_humidity <= 80 else max(30, int(92 - abs(avg_humidity - 62) * 1.5))

    # Combined Lifecycle Climate Score
    lifecycle_score = int(0.45 * avg_temp_score + 0.35 * rainfall_score + 0.20 * humidity_score)
    
    # Severe temperature penalty cap
    if avg_temp_score < 25:
        lifecycle_score = min(lifecycle_score, int(avg_temp_score + 10))

    return max(5, min(99, lifecycle_score))
