import httpx
from typing import Dict, Any

# Known location coordinates for instant lookup
LOCATION_COORDS = {
    "vadodara": {"lat": 22.3072, "lon": 73.1812, "name": "Vadodara, Gujarat"},
    "ahmedabad": {"lat": 23.0225, "lon": 72.5714, "name": "Ahmedabad, Gujarat"},
    "rajkot": {"lat": 22.3039, "lon": 70.8022, "name": "Rajkot, Gujarat"},
    "surat": {"lat": 21.1702, "lon": 72.8311, "name": "Surat, Gujarat"},
    "pune": {"lat": 18.5204, "lon": 73.8567, "name": "Pune, Maharashtra"},
    "ludhiana": {"lat": 30.9010, "lon": 75.8573, "name": "Ludhiana, Punjab"},
    "jaipur": {"lat": 26.9124, "lon": 75.7873, "name": "Jaipur, Rajasthan"},
}

def get_current_weather_and_forecast(location: str = "Vadodara, Gujarat") -> Dict[str, Any]:
    clean_loc = location.strip().lower()
    
    # Try online geocoding + open-meteo weather API first
    try:
        coord = None
        for key in LOCATION_COORDS:
            if key in clean_loc:
                coord = LOCATION_COORDS[key]
                break
        
        if not coord:
            # Geocode via open-meteo
            geo_res = httpx.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": location, "count": 1},
                timeout=2.0
            )
            if geo_res.status_code == 200 and geo_res.json().get("results"):
                res = geo_res.json()["results"][0]
                coord = {
                    "lat": res["latitude"],
                    "lon": res["longitude"],
                    "name": f"{res['name']}, {res.get('admin1', res.get('country', ''))}"
                }

        if coord:
            w_res = httpx.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": coord["lat"],
                    "longitude": coord["lon"],
                    "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
                    "daily": "temperature_2m_max,precipitation_sum,precipitation_probability_max,weather_code",
                    "timezone": "auto"
                },
                timeout=2.5
            )
            if w_res.status_code == 200:
                data = w_res.json()
                curr = data.get("current", {})
                daily = data.get("daily", {})
                
                temp_c = float(curr.get("temperature_2m", 28.0))
                humidity_pct = float(curr.get("relative_humidity_2m", 68.0))
                wind_kmh = float(curr.get("wind_speed_10m", 12.0))
                rainfall_mm = float(curr.get("precipitation", 2.5))
                
                forecast_days = []
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                time_list = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                precip_sums = daily.get("precipitation_sum", [])
                precip_probs = daily.get("precipitation_probability_max", [])
                
                for idx, t_str in enumerate(time_list[:7]):
                    day_name = days[idx % 7]
                    forecast_days.append({
                        "day": day_name,
                        "temp_c": float(max_temps[idx]) if idx < len(max_temps) else 28.0,
                        "condition": "Rain" if (idx < len(precip_sums) and precip_sums[idx] > 2.0) else "Partly Cloudy",
                        "rain_chance_pct": int(precip_probs[idx]) if idx < len(precip_probs) else 20,
                        "rainfall_mm": float(precip_sums[idx]) if idx < len(precip_sums) else 0.0
                    })
                
                rain_prob_max = max([f["rain_chance_pct"] for f in forecast_days], default=20)
                
                alerts = []
                if rain_prob_max > 60:
                    alerts.append({
                        "level": "info",
                        "title": "Rain window detected",
                        "description": "Good moisture window expected in upcoming forecast."
                    })
                
                return {
                    "location": coord["name"],
                    "temp_c": temp_c,
                    "humidity_pct": humidity_pct,
                    "wind_kmh": wind_kmh,
                    "rainfall_mm": rainfall_mm,
                    "rain_chance_pct": rain_prob_max,
                    "condition": "Partly cloudy" if rainfall_mm < 2.0 else "Rainy",
                    "alerts": alerts,
                    "forecast": forecast_days,
                    "is_demo": False
                }
    except Exception as e:
        pass

    # Deterministic fallback per location
    if "vadodara" in clean_loc:
        loc_name = "Vadodara, Gujarat"
        temp_c = 29.5
        humidity_pct = 74.0
        rain_prob = 64
        rain_mm = 62.0
    elif "ludhiana" in clean_loc or "punjab" in clean_loc:
        loc_name = "Ludhiana, Punjab"
        temp_c = 26.0
        humidity_pct = 62.0
        rain_prob = 15
        rain_mm = 12.0
    elif "pune" in clean_loc or "maharashtra" in clean_loc:
        loc_name = "Pune, Maharashtra"
        temp_c = 25.5
        humidity_pct = 78.0
        rain_prob = 70
        rain_mm = 85.0
    else:
        loc_name = location if location else "Vadodara, Gujarat"
        temp_c = 28.0
        humidity_pct = 68.0
        rain_prob = 64
        rain_mm = 45.0

    forecast_days = [
        {"day": "Tue", "temp_c": temp_c - 1, "condition": "Light Rain", "rain_chance_pct": rain_prob, "rainfall_mm": 12.0},
        {"day": "Wed", "temp_c": temp_c + 1, "condition": "Partly Cloudy", "rain_chance_pct": 20, "rainfall_mm": 0.0},
        {"day": "Thu", "temp_c": temp_c - 2, "condition": "Moderate Rain", "rain_chance_pct": 75, "rainfall_mm": 25.0},
        {"day": "Fri", "temp_c": temp_c, "condition": "Sunny", "rain_chance_pct": 10, "rainfall_mm": 0.0},
        {"day": "Sat", "temp_c": temp_c + 2, "condition": "Clear Sky", "rain_chance_pct": 5, "rainfall_mm": 0.0},
        {"day": "Sun", "temp_c": temp_c - 1, "condition": "Scattered Showers", "rain_chance_pct": 50, "rainfall_mm": 8.0},
        {"day": "Mon", "temp_c": temp_c, "condition": "Partly Cloudy", "rain_chance_pct": 15, "rainfall_mm": 0.0},
    ]

    return {
        "location": loc_name,
        "temp_c": temp_c,
        "humidity_pct": humidity_pct,
        "wind_kmh": 14.0,
        "rainfall_mm": rain_mm,
        "rain_chance_pct": rain_prob,
        "condition": "Partly cloudy",
        "alerts": [
            {
                "level": "success",
                "title": "Rain window detected",
                "description": "Favorable moisture window for sowing in the upcoming forecast."
            }
        ],
        "forecast": forecast_days,
        "is_demo": True
    }
