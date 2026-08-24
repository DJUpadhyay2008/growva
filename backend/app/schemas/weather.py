from pydantic import BaseModel
from typing import List, Optional

class DailyForecast(BaseModel):
    day: str # e.g. "Tue", "Wed"
    temp_c: float
    condition: str
    rain_chance_pct: int
    rainfall_mm: float

class WeatherAlert(BaseModel):
    level: str # warning, info, success
    title: str
    description: str

class WeatherResponse(BaseModel):
    location: str
    temp_c: float
    humidity_pct: float
    wind_kmh: float
    rainfall_mm: float
    condition: str
    alerts: List[WeatherAlert]
    forecast: List[DailyForecast]
