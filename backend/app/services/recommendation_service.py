from sqlalchemy.orm import Session
from app.database.models import CropModel
from app.schemas.recommendation import (
    RecommendationRequest, RecommendationResponse, CropRecommendationItem,
    ScoreBreakdown, RiskBreakdown, GrowthStageSchema
)
from app.services.weather_service import get_current_weather_and_forecast
from typing import List
import math

def generate_crop_recommendations(db: Session, req: RecommendationRequest) -> RecommendationResponse:
    # Get weather data for the location
    loc_str = req.location or "Vadodara, Gujarat"
    weather = get_current_weather_and_forecast(loc_str)
    
    user_temp = weather.get("temp_c", 28.0)
    user_humidity = weather.get("humidity_pct", 68.0)
    user_rain_prob = weather.get("rain_chance_pct", 64.0)
    user_rain_mm = weather.get("rainfall_mm", 45.0)
    weather_cond = weather.get("condition", "Partly cloudy")
    is_demo = weather.get("is_demo", True)
    
    user_soil = (req.soil_type or "Fertile loam").lower()
    user_ph = req.ph if req.ph is not None else 6.8
    
    crops = db.query(CropModel).all()
    results = []

    for crop in crops:
        # 1. Climate Suitability (400-1500mm standard)
        climate_score = 90
        if crop.min_rainfall <= 800 <= crop.max_rainfall:
            climate_score = 95
        elif 800 < crop.min_rainfall:
            penalty = min(30, (crop.min_rainfall - 800) / 20)
            climate_score -= int(penalty)
        climate_score = max(50, min(99, climate_score))

        # 2. Season Suitability
        season_score = 92
        if "kharif" in crop.season.lower() or "year-round" in crop.season.lower() or "varies" in crop.season.lower():
            season_score = 95
        else:
            season_score = 78

        # 3. Current Conditions Suitability (temp & soil/pH)
        current_score = 88
        if crop.min_temp <= user_temp <= crop.max_temp:
            current_score = 92
        else:
            penalty = min(25, abs(user_temp - (crop.min_temp + crop.max_temp)/2) * 1.5)
            current_score -= int(penalty)
        current_score = max(45, min(99, current_score))

        # 4. Forecast Suitability (7-14 day forecast window)
        forecast_score = 85
        if user_rain_prob > 75:
            forecast_score = 65 # heavy rain might hamper immediate sowing
        elif 30 <= user_rain_prob <= 70:
            forecast_score = 92 # ideal moisture for sowing
        else:
            forecast_score = 80 # dry window

        # Weighted final score
        match_score = int(
            0.30 * climate_score +
            0.25 * season_score +
            0.25 * current_score +
            0.20 * forecast_score
        )
        match_score = max(45, min(98, match_score))

        if match_score >= 86:
            rating = "Highly Suitable"
        elif match_score >= 70:
            rating = "Suitable"
        else:
            rating = "Moderate"

        # Risk breakdown & warnings
        risk_warnings = []
        if user_rain_prob > 70 or user_rain_mm > 50:
            risk_warnings.append(f"Heavy rainfall risk expected in short-term forecast ({user_rain_prob}% rain chance)")
            sowing_status = "WAIT"
            sowing_win = f"Consider delaying sowing by 3–5 days due to high rain probability ({user_rain_prob}%)."
        elif user_temp > crop.max_temp - 2:
            risk_warnings.append(f"High temperature warning ({user_temp}°C near crop max limit of {crop.max_temp}°C)")
            sowing_status = "HEAT_RISK"
            sowing_win = "Wait for temperature to cool slightly for optimal germination."
        else:
            sowing_status = "GOOD"
            sowing_win = f"Favorable conditions! Sow within the next 3–5 days."

        if not risk_warnings:
            risk_level = "LOW"
            risk_score = 88
            risk_warnings.append("No major weather risks detected for current sowing window.")
        elif len(risk_warnings) == 1:
            risk_level = "MEDIUM"
            risk_score = 68
        else:
            risk_level = "HIGH"
            risk_score = 45

        # Reasons
        reasons = [
            f"Climate is suitable for {crop.name} in this region",
            f"Temperature ({user_temp}°C) is within growth range ({crop.min_temp}°C - {crop.max_temp}°C)",
            f"Water requirement ({crop.water_req}) matches local availability"
        ]
        
        risk_factors = risk_warnings[:]

        # Growth stages calculation
        dur = crop.duration_days or 90
        s1 = max(5, int(dur * 0.08))
        s2 = s1 + max(10, int(dur * 0.22))
        s3 = s2 + max(20, int(dur * 0.30))
        s4 = s3 + max(20, int(dur * 0.25))
        
        growth_stages = [
            GrowthStageSchema(name="Prepare field", start_day=0, end_day=s1),
            GrowthStageSchema(name="Sowing window", start_day=s1+1, end_day=s2),
            GrowthStageSchema(name="Germination & Vegetative", start_day=s2+1, end_day=s3),
            GrowthStageSchema(name="Flowering & Pods", start_day=s3+1, end_day=s4),
            GrowthStageSchema(name="Expected harvest", start_day=s4+1, end_day=dur)
        ]

        results.append(CropRecommendationItem(
            crop_name=crop.name,
            category=crop.category,
            match_score=match_score,
            suitability_rating=rating,
            scores=ScoreBreakdown(
                climate_suitability=climate_score,
                season_suitability=season_score,
                current_conditions=current_score,
                forecast_suitability=forecast_score
            ),
            risk=RiskBreakdown(
                level=risk_level,
                score=risk_score,
                warnings=risk_warnings
            ),
            duration_days=dur,
            growth_stages=growth_stages,
            reasons=reasons,
            risk_factors=risk_factors,
            expected_yield=crop.expected_yield,
            suggested_sowing_window=sowing_win,
            sowing_status=sowing_status
        ))

    # Sort by match_score descending
    results.sort(key=lambda x: x.match_score, reverse=True)

    top_crop = results[0] if results else None
    if top_crop:
        if top_crop.sowing_status == "GOOD":
            advisory = (
                f"Conditions are favorable for sowing {top_crop.crop_name} in {weather['location']}. "
                f"The upcoming 7-day forecast shows manageable rainfall risk ({user_rain_prob}%) "
                f"and ideal temperature ({user_temp}°C), making this an optimal sowing window."
            )
        elif top_crop.sowing_status == "WAIT":
            advisory = (
                f"Heavy rainfall ({user_rain_mm} mm expected, {user_rain_prob}% rain chance) is forecasted in {weather['location']}. "
                f"Consider delaying sowing {top_crop.crop_name} by 4–6 days until field moisture stabilizes."
            )
        else:
            advisory = (
                f"High temperature ({user_temp}°C) is expected over the next week in {weather['location']}. "
                f"Consider waiting for a slightly cooler moisture window before sowing {top_crop.crop_name}."
            )
    else:
        advisory = "No recommendation advisory generated."

    return RecommendationResponse(
        location=weather["location"],
        temperature=user_temp,
        humidity=user_humidity,
        rain_probability=user_rain_prob,
        rainfall_expected=user_rain_mm,
        condition=weather_cond,
        soil_type=req.soil_type or "Fertile loam",
        top_recommendations=results[:10],
        sowing_advisory=advisory,
        is_demo=is_demo
    )
