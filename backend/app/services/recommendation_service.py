from sqlalchemy.orm import Session
from app.database.models import CropModel
from app.schemas.recommendation import (
    RecommendationRequest, RecommendationResponse, CropRecommendationItem,
    ScoreBreakdown, RiskBreakdown, GrowthStageSchema
)
from app.services.weather_service import get_current_weather_and_forecast
from typing import List
from datetime import datetime

def generate_crop_recommendations(db: Session, req: RecommendationRequest) -> RecommendationResponse:
    # 1. Fetch live weather & forecast for requested location
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

    current_month = datetime.now().month # 1 to 12

    # Estimate annual rainfall potential based on live humidity, precipitation, & weather condition
    w_cond_lower = weather_cond.lower()
    if user_humidity < 50 or "sunny" in w_cond_lower or "dry" in w_cond_lower:
        est_rainfall = max(180.0, user_rain_mm * 10.0 + 220.0)
    elif user_humidity > 80 or "rain" in w_cond_lower or "thunderstorm" in w_cond_lower:
        est_rainfall = max(850.0, user_rain_mm * 20.0 + 800.0)
    else:
        est_rainfall = max(450.0, user_rain_mm * 15.0 + 480.0)

    for crop in crops:
        # -------------------------------------------------------------
        # A. Temperature Suitability (0 - 100)
        # -------------------------------------------------------------
        if crop.min_temp <= user_temp <= crop.max_temp:
            ideal_center = (crop.min_temp + crop.max_temp) / 2.0
            dist = abs(user_temp - ideal_center)
            half_range = max(1.0, (crop.max_temp - crop.min_temp) / 2.0)
            temp_score = 98 - int((dist / half_range) * 15)
        elif user_temp < crop.min_temp:
            deficit = crop.min_temp - user_temp
            if deficit > 10.0 or user_temp <= 3.0:
                temp_score = max(2, int(25 - deficit * 3.0))
            else:
                temp_score = max(10, int(80 - deficit * 7.0))
        else: # user_temp > crop.max_temp
            excess = user_temp - crop.max_temp
            if excess > 8.0:
                temp_score = max(5, int(35 - excess * 4.0))
            else:
                temp_score = max(15, int(80 - excess * 6.5))

        # -------------------------------------------------------------
        # B. Humidity & Water Requirement Alignment (0 - 100)
        # -------------------------------------------------------------
        w_req = crop.water_req.lower()
        if "very high" in w_req or "high" in w_req:
            if user_humidity >= 65:
                humidity_score = 95
            else:
                humidity_score = max(20, int(95 - (65 - user_humidity) * 2.0))
        elif "low" in w_req:
            if user_humidity <= 60:
                humidity_score = 96
            else:
                humidity_score = max(25, int(96 - (user_humidity - 60) * 2.0))
        else: # Medium
            if 50 <= user_humidity <= 80:
                humidity_score = 92
            else:
                humidity_score = max(35, int(92 - abs(user_humidity - 65) * 1.4))

        # Current Conditions combined (Temp 70% + Humidity 30%)
        current_score = int(0.70 * temp_score + 0.30 * humidity_score)
        current_score = max(2, min(99, current_score))

        # -------------------------------------------------------------
        # C. Climate & Water Availability Suitability (0 - 100)
        # -------------------------------------------------------------
        if crop.min_rainfall <= est_rainfall <= crop.max_rainfall:
            climate_score = 96
        elif est_rainfall < crop.min_rainfall:
            shortfall = crop.min_rainfall - est_rainfall
            climate_score = max(15, int(92 - (shortfall / crop.min_rainfall) * 65))
        else:
            overflow = est_rainfall - crop.max_rainfall
            climate_score = max(30, int(92 - (overflow / crop.max_rainfall) * 45))

        # Soil & pH adjustment
        crop_soil_lower = crop.soil_type.lower()
        soil_match = False
        soil_keywords = ["loam", "clay", "sandy", "black", "alluvial", "red"]
        for kw in soil_keywords:
            if kw in user_soil and kw in crop_soil_lower:
                soil_match = True
                break
        
        soil_score = 95 if (soil_match or "loam" in user_soil) else 75

        if crop.ideal_ph_min <= user_ph <= crop.ideal_ph_max:
            ph_score = 95
        else:
            ph_score = max(50, int(95 - abs(user_ph - (crop.ideal_ph_min + crop.ideal_ph_max)/2) * 15))

        soil_ph_factor = (soil_score * 0.6 + ph_score * 0.4)
        climate_score = int(climate_score * 0.7 + soil_ph_factor * 0.3)
        climate_score = max(10, min(99, climate_score))

        # -------------------------------------------------------------
        # D. Season Alignment (0 - 100)
        # -------------------------------------------------------------
        c_season = crop.season.lower()
        if 6 <= current_month <= 10: # Kharif (Monsoon)
            if "kharif" in c_season or "monsoon" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season or "seasonal" in c_season:
                season_score = 90
            elif "summer" in c_season:
                season_score = 72
            else: # Rabi (Winter)
                season_score = 55
        elif 11 <= current_month or current_month <= 3: # Rabi (Winter)
            if "rabi" in c_season or "winter" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season or "seasonal" in c_season:
                season_score = 90
            elif "temperate" in c_season:
                season_score = 95
            else: # Kharif
                season_score = 58
        else: # Zaid (Summer: April-May)
            if "summer" in c_season or "zaid" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season:
                season_score = 90
            else:
                season_score = 65

        # -------------------------------------------------------------
        # E. Forecast & Weather Risk Suitability (0 - 100)
        # -------------------------------------------------------------
        if "snow" in w_cond_lower or user_temp <= 3.0:
            if "temperate" in c_season or crop.min_temp <= 5.0:
                forecast_score = 88
            else:
                forecast_score = 10 # Frost danger
        elif user_rain_prob > 75 or user_rain_mm > 50:
            forecast_score = 65
        elif 25 <= user_rain_prob <= 70:
            forecast_score = 94
        else:
            forecast_score = 82

        # -------------------------------------------------------------
        # F. Overall Weighted Score Calculation
        # -------------------------------------------------------------
        match_score = int(
            0.35 * current_score +
            0.25 * climate_score +
            0.25 * season_score +
            0.15 * forecast_score
        )

        # Disqualification cap if temp or climate is severely unsuitable
        if temp_score < 20:
            match_score = min(match_score, temp_score + 10)
        if climate_score < 30:
            match_score = min(match_score, climate_score + 15)

        match_score = max(5, min(98, match_score))

        if match_score >= 82:
            rating = "Highly Suitable"
        elif match_score >= 65:
            rating = "Suitable"
        elif match_score >= 45:
            rating = "Moderate"
        else:
            rating = "Low Suitability"

        # Risk breakdown & warnings
        risk_warnings = []
        if "snow" in w_cond_lower or user_temp <= 3.0:
            if crop.min_temp > 5.0:
                risk_warnings.append(f"Freezing temperature ({user_temp}°C). Frost risk for {crop.name}.")
                sowing_status = "WAIT"
                sowing_win = f"Delay sowing until temperature rises above minimum threshold ({crop.min_temp}°C)."
            else:
                sowing_status = "GOOD"
                sowing_win = f"Cold-hardy crop! Suitable for current mountain climate ({user_temp}°C)."
        elif user_rain_prob > 70 or user_rain_mm > 50:
            risk_warnings.append(f"Heavy rainfall risk expected in forecast ({user_rain_prob}% rain chance)")
            sowing_status = "WAIT"
            sowing_win = f"Consider delaying sowing by 3–5 days due to heavy rain probability ({user_rain_prob}%)."
        elif user_temp > crop.max_temp - 2:
            risk_warnings.append(f"High temperature warning ({user_temp}°C near crop limit of {crop.max_temp}°C)")
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

        # Reasons tailored to real weather values
        reasons = [
            f"Temperature ({user_temp}°C) is {'optimal' if crop.min_temp <= user_temp <= crop.max_temp else 'suboptimal'} for {crop.name} ({crop.min_temp}°C - {crop.max_temp}°C)",
            f"Humidity ({user_humidity}%) aligns with {crop.name}'s {crop.water_req.lower()} water requirement",
            f"Soil fit for {req.soil_type or 'Fertile loam'} with pH {user_ph} (Ideal: {crop.ideal_ph_min}-{crop.ideal_ph_max})"
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
                f"Conditions in {weather['location']} ({user_temp}°C, {user_humidity}% humidity) favor sowing {top_crop.crop_name} "
                f"with top suitability ({top_crop.match_score}%). "
                f"Upcoming forecast indicates suitable moisture and temperature levels."
            )
        elif top_crop.sowing_status == "WAIT":
            advisory = (
                f"Weather alert for {weather['location']}: current conditions ({user_temp}°C, {user_rain_prob}% rain/frost risk) "
                f"require caution. Consider delaying sowing {top_crop.crop_name} until climate stabilizes."
            )
        else:
            advisory = (
                f"High temperature ({user_temp}°C) in {weather['location']} requires heat management. "
                f"Wait for slightly cooler moisture window before sowing {top_crop.crop_name}."
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
        top_recommendations=results[:12],
        sowing_advisory=advisory,
        is_demo=is_demo
    )
