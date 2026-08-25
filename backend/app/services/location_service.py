import httpx
from typing import Dict, Any, Optional

INDIAN_CITY_COORDS: Dict[str, Dict[str, Any]] = {
    "vadodara": {"lat": 22.3072, "lon": 73.1812, "name": "Vadodara, Gujarat", "district": "Vadodara", "state": "Gujarat"},
    "ahmedabad": {"lat": 23.0225, "lon": 72.5714, "name": "Ahmedabad, Gujarat", "district": "Ahmedabad", "state": "Gujarat"},
    "rajkot": {"lat": 22.3039, "lon": 70.8022, "name": "Rajkot, Gujarat", "district": "Rajkot", "state": "Gujarat"},
    "surat": {"lat": 21.1702, "lon": 72.8311, "name": "Surat, Gujarat", "district": "Surat", "state": "Gujarat"},
    "gondal": {"lat": 21.9619, "lon": 70.7924, "name": "Gondal, Gujarat", "district": "Rajkot", "state": "Gujarat"},
    "anand": {"lat": 22.5645, "lon": 72.9289, "name": "Anand, Gujarat", "district": "Anand", "state": "Gujarat"},
    "nadiad": {"lat": 22.6916, "lon": 72.8634, "name": "Nadiad, Gujarat", "district": "Kheda", "state": "Gujarat"},
    "unjha": {"lat": 23.8037, "lon": 72.3912, "name": "Unjha, Gujarat", "district": "Mehsana", "state": "Gujarat"},
    "junagadh": {"lat": 21.5222, "lon": 70.4579, "name": "Junagadh, Gujarat", "district": "Junagadh", "state": "Gujarat"},
    "amreli": {"lat": 21.6032, "lon": 71.2221, "name": "Amreli, Gujarat", "district": "Amreli", "state": "Gujarat"},
    "mehsana": {"lat": 23.5880, "lon": 72.3693, "name": "Mehsana, Gujarat", "district": "Mehsana", "state": "Gujarat"},
    "ludhiana": {"lat": 30.9010, "lon": 75.8573, "name": "Ludhiana, Punjab", "district": "Ludhiana", "state": "Punjab"},
    "jalandhar": {"lat": 31.3260, "lon": 75.5762, "name": "Jalandhar, Punjab", "district": "Jalandhar", "state": "Punjab"},
    "bathinda": {"lat": 30.2110, "lon": 74.9455, "name": "Bathinda, Punjab", "district": "Bathinda", "state": "Punjab"},
    "bhatinda": {"lat": 30.2110, "lon": 74.9455, "name": "Bathinda, Punjab", "district": "Bathinda", "state": "Punjab"},
    "khanna": {"lat": 30.7028, "lon": 76.2201, "name": "Khanna, Punjab", "district": "Ludhiana", "state": "Punjab"},
    "karnal": {"lat": 29.6857, "lon": 76.9905, "name": "Karnal, Haryana", "district": "Karnal", "state": "Haryana"},
    "lasalgaon": {"lat": 20.1472, "lon": 74.2304, "name": "Lasalgaon, Maharashtra", "district": "Nashik", "state": "Maharashtra"},
    "nashik": {"lat": 19.9975, "lon": 73.7898, "name": "Nashik, Maharashtra", "district": "Nashik", "state": "Maharashtra"},
    "pune": {"lat": 18.5204, "lon": 73.8567, "name": "Pune, Maharashtra", "district": "Pune", "state": "Maharashtra"},
    "latur": {"lat": 18.4088, "lon": 76.5604, "name": "Latur, Maharashtra", "district": "Latur", "state": "Maharashtra"},
    "nagpur": {"lat": 21.1458, "lon": 79.0882, "name": "Nagpur, Maharashtra", "district": "Nagpur", "state": "Maharashtra"},
    "indore": {"lat": 22.7196, "lon": 75.8577, "name": "Indore, Madhya Pradesh", "district": "Indore", "state": "Madhya Pradesh"},
    "ujjain": {"lat": 23.1765, "lon": 75.7885, "name": "Ujjain, Madhya Pradesh", "district": "Ujjain", "state": "Madhya Pradesh"},
    "jaipur": {"lat": 26.9124, "lon": 75.7873, "name": "Jaipur, Rajasthan", "district": "Jaipur", "state": "Rajasthan"},
    "jodhpur": {"lat": 26.2389, "lon": 73.0243, "name": "Jodhpur, Rajasthan", "district": "Jodhpur", "state": "Rajasthan"},
    "guntur": {"lat": 16.3067, "lon": 80.4365, "name": "Guntur, Andhra Pradesh", "district": "Guntur", "state": "Andhra Pradesh"},
}

def resolve_location(location_name: str, lat: Optional[float] = None, lon: Optional[float] = None) -> Dict[str, Any]:
    """Resolves a location name into latitude, longitude, district, state, and formatted name."""
    if lat is not None and lon is not None:
        return {
            "name": location_name,
            "lat": lat,
            "lon": lon,
            "district": location_name.split(",")[0].strip(),
            "state": location_name.split(",")[-1].strip() if "," in location_name else "India"
        }

    clean_name = location_name.strip().lower()
    for key, data in INDIAN_CITY_COORDS.items():
        if key in clean_name:
            return data

    # Try Open-Meteo Geocoding API for dynamic resolution
    try:
        res = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location_name, "count": 1},
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=4.0
        )
        if res.status_code == 200 and res.json().get("results"):
            item = res.json()["results"][0]
            admin1 = item.get("admin1", "India")
            district = item.get("admin2") or item.get("name")
            return {
                "name": f"{item['name']}, {admin1}",
                "lat": item["latitude"],
                "lon": item["longitude"],
                "district": district,
                "state": admin1
            }
    except Exception as e:
        print(f"Geocoding fallback exception: {e}")

    # Fallback to Vadodara if completely unknown
    return INDIAN_CITY_COORDS["vadodara"]
