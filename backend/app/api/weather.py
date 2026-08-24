from fastapi import APIRouter, Query
from app.schemas.weather import WeatherResponse
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("", response_model=WeatherResponse)
def get_weather(location: str = Query("Ahmedabad, Gujarat", description="Location name")):
    data = weather_service.get_current_weather_and_forecast(location=location)
    return WeatherResponse(**data)
