import httpx
from typing import Dict, Any
from datetime import datetime

LOCATION_COORDS = {
    "amarnath": {"lat": 34.2157, "lon": 75.5008, "name": "Amarnath, Jammu & Kashmir"},
    "srinagar": {"lat": 34.0837, "lon": 74.7973, "name": "Srinagar, Jammu & Kashmir"},
    "leh": {"lat": 34.1526, "lon": 77.5771, "name": "Leh, Ladakh"},
    "shimla": {"lat": 31.1048, "lon": 77.1734, "name": "Shimla, Himachal Pradesh"},
    "manali": {"lat": 32.2432, "lon": 77.1892, "name": "Manali, Himachal Pradesh"},
    "jaisalmer": {"lat": 26.9157, "lon": 70.9083, "name": "Jaisalmer, Rajasthan"},
    "jaipur": {"lat": 26.9124, "lon": 75.7873, "name": "Jaipur, Rajasthan"},
    "jodhpur": {"lat": 26.2389, "lon": 73.0243, "name": "Jodhpur, Rajasthan"},
    "kochi": {"lat": 9.9312, "lon": 76.2673, "name": "Kochi, Kerala"},
    "guwahati": {"lat": 26.1445, "lon": 91.7362, "name": "Guwahati, Assam"},
    "vadodara": {"lat": 22.3072, "lon": 73.1812, "name": "Vadodara, Gujarat"},
    "ahmedabad": {"lat": 23.0225, "lon": 72.5714, "name": "Ahmedabad, Gujarat"},
    "rajkot": {"lat": 22.3039, "lon": 70.8022, "name": "Rajkot, Gujarat"},
    "surat": {"lat": 21.1702, "lon": 72.8311, "name": "Surat, Gujarat"},
    "pune": {"lat": 18.5204, "lon": 73.8567, "name": "Pune, Maharashtra"},
    "ludhiana": {"lat": 30.9010, "lon": 75.8573, "name": "Ludhiana, Punjab"},
}

def get_wmo_condition(code: int) -> str:
    if code == 0:
        return "Sunny"
    elif code in [1, 2, 3]:
        return "Partly cloudy"
    elif code in [45, 48]:
        return "Fog"
    elif code in [51, 53, 55, 56, 57]:
        return "Light rain"
    elif code in [61, 63, 65, 66, 67, 80, 81, 82]:
        return "Rain"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "Snow"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    return "Partly cloudy"

def get_current_weather_and_forecast(location: str = "Vadodara, Gujarat") -> Dict[str, Any]:
    clean_loc = location.strip().lower()
    
    coord = None
    for key in LOCATION_COORDS:
        if key in clean_loc:
            coord = LOCATION_COORDS[key]
            break
    
    try:
        if not coord:
            # Geocode via open-meteo
            geo_res = httpx.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": location, "count": 1},
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                timeout=5.0
            )
            if geo_res.status_code == 200 and geo_res.json().get("results"):
                res = geo_res.json()["results"][0]
                admin_str = res.get("admin1") or res.get("country") or ""
                coord = {
                    "lat": res["latitude"],
                    "lon": res["longitude"],
                    "name": f"{res['name']}, {admin_str}" if admin_str else res["name"]
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
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                timeout=5.0
            )
            if w_res.status_code == 200:
                data = w_res.json()
                curr = data.get("current", {})
                daily = data.get("daily", {})
                
                temp_c = float(curr.get("temperature_2m", 28.0))
                humidity_pct = float(curr.get("relative_humidity_2m", 68.0))
                wind_kmh = float(curr.get("wind_speed_10m", 12.0))
                rainfall_mm = float(curr.get("precipitation", 0.0))
                curr_wmo = int(curr.get("weather_code", 1))
                
                forecast_days = []
                time_list = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                precip_sums = daily.get("precipitation_sum", [])
                precip_probs = daily.get("precipitation_probability_max", [])
                daily_wmo = daily.get("weather_code", [])
                
                for idx, t_str in enumerate(time_list[:7]):
                    try:
                        dt = datetime.strptime(t_str, "%Y-%m-%d")
                        day_name = dt.strftime("%a")
                    except Exception:
                        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][idx % 7]

                    w_code = daily_wmo[idx] if idx < len(daily_wmo) else 1
                    forecast_days.append({
                        "day": day_name,
                        "temp_c": float(max_temps[idx]) if idx < len(max_temps) else temp_c,
                        "condition": get_wmo_condition(w_code),
                        "rain_chance_pct": int(precip_probs[idx]) if idx < len(precip_probs) else 20,
                        "rainfall_mm": float(precip_sums[idx]) if idx < len(precip_sums) else 0.0
                    })
                
                rain_prob_max = max([f["rain_chance_pct"] for f in forecast_days], default=20)
                
                alerts = []
                if rain_prob_max > 50:
                    alerts.append({
                        "level": "info",
                        "title": "Rain window detected",
                        "description": f"Good moisture window expected for {coord['name']}. Next rain chance around {rain_prob_max}%."
                    })
                else:
                    alerts.append({
                        "level": "success",
                        "title": "Clear conditions",
                        "description": f"Clear weather expected in {coord['name']}. Good window for field operations and harvesting."
                    })
                
                return {
                    "location": coord["name"],
                    "temp_c": temp_c,
                    "humidity_pct": humidity_pct,
                    "wind_kmh": wind_kmh,
                    "rainfall_mm": rainfall_mm,
                    "rain_chance_pct": rain_prob_max,
                    "condition": get_wmo_condition(curr_wmo),
                    "alerts": alerts,
                    "forecast": forecast_days,
                    "is_demo": False
                }
    except Exception as e:
        print(f"Open-Meteo weather fetch notice: {e}")

    # Regional climate fallbacks if external network is unavailable
    if any(k in clean_loc for k in ["amarnath", "srinagar", "leh", "shimla", "manali"]):
        fallback_temp = 7.5
        fallback_humidity = 76.0
        fallback_rain_mm = 5.0
        fallback_cond = "Snow / Fog"
    elif any(k in clean_loc for k in ["jaisalmer", "jodhpur", "bikaner", "rajasthan"]):
        fallback_temp = 34.0
        fallback_humidity = 38.0
        fallback_rain_mm = 0.5
        fallback_cond = "Sunny"
    elif any(k in clean_loc for k in ["kochi", "kerala", "assam", "guwahati"]):
        fallback_temp = 28.0
        fallback_humidity = 86.0
        fallback_rain_mm = 25.0
        fallback_cond = "Rain"
    else:
        fallback_temp = 29.5
        fallback_humidity = 72.0
        fallback_rain_mm = 12.0
        fallback_cond = "Partly cloudy"

    return {
        "location": location if location else "Vadodara, Gujarat",
        "temp_c": fallback_temp,
        "humidity_pct": fallback_humidity,
        "wind_kmh": 12.0,
        "rainfall_mm": fallback_rain_mm,
        "rain_chance_pct": 45,
        "condition": fallback_cond,
        "alerts": [
            {
                "level": "info",
                "title": "Weather conditions active",
                "description": f"Climate parameters retrieved for {location or 'Vadodara, Gujarat'}."
            }
        ],
        "forecast": [
            {"day": "Mon", "temp_c": fallback_temp, "condition": fallback_cond, "rain_chance_pct": 40, "rainfall_mm": fallback_rain_mm},
            {"day": "Tue", "temp_c": fallback_temp - 1, "condition": fallback_cond, "rain_chance_pct": 50, "rainfall_mm": fallback_rain_mm + 2},
            {"day": "Wed", "temp_c": fallback_temp + 1, "condition": "Partly cloudy", "rain_chance_pct": 20, "rainfall_mm": 0.0},
            {"day": "Thu", "temp_c": fallback_temp, "condition": fallback_cond, "rain_chance_pct": 30, "rainfall_mm": 2.0},
            {"day": "Fri", "temp_c": fallback_temp + 2, "condition": "Sunny", "rain_chance_pct": 10, "rainfall_mm": 0.0},
            {"day": "Sat", "temp_c": fallback_temp + 1, "condition": "Sunny", "rain_chance_pct": 15, "rainfall_mm": 0.0},
            {"day": "Sun", "temp_c": fallback_temp, "condition": "Partly cloudy", "rain_chance_pct": 25, "rainfall_mm": 1.0},
        ],
        "is_demo": True
    }
