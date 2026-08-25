from sqlalchemy.orm import Session
from app.database.models import CropModel
from app.schemas.recommendation import (
    RecommendationRequest, RecommendationResponse, CropRecommendationItem,
    ScoreBreakdown, RiskBreakdown, SowingWindowSchema, GrowthStageSchema
)
from app.services.weather_service import get_current_weather_and_forecast
from app.services.climate_service import calculate_lifecycle_climate_score
from typing import List
from datetime import datetime, timedelta

SCORING_WEIGHTS = {
    "lifecycle_climate": 0.40,
    "season": 0.25,
    "current_conditions": 0.20,
    "forecast": 0.15,
}

def determine_current_season(month: int) -> str:
    if 6 <= month <= 10:
        return "Kharif"
    elif month >= 11 or month <= 3:
        return "Rabi"
    else:
        return "Zaid"

def generate_crop_recommendations(db: Session, req: RecommendationRequest) -> RecommendationResponse:
    loc_str = req.location or "Vadodara, Gujarat"
    
    # 1. Weather Service Call (real Open-Meteo or regional deterministic fallback)
    weather = get_current_weather_and_forecast(loc_str)
    
    user_temp = weather.get("temp_c", 28.0)
    user_humidity = weather.get("humidity_pct", 68.0)
    user_rain_prob = weather.get("rain_chance_pct", 45.0)
    user_rain_mm = weather.get("rainfall_mm", 0.0)
    weather_cond = weather.get("condition", "Partly cloudy")
    forecast_days = weather.get("forecast", [])
    is_demo = weather.get("is_demo", True)
    
    now = datetime.now()
    current_month = now.month
    current_season = determine_current_season(current_month)

    # 2. Analyze Short-Term Forecast Array (7-14 days)
    heavy_rain_days = 0
    moderate_rain_days = 0
    total_7d_rain = 0.0
    max_forecast_prob = 0
    first_heavy_rain_day = None

    for idx, f in enumerate(forecast_days):
        r_mm = f.get("rainfall_mm", 0.0)
        r_prob = f.get("rain_chance_pct", 0)
        total_7d_rain += r_mm
        if r_prob > max_forecast_prob:
            max_forecast_prob = r_prob
        
        if r_mm >= 25.0 or r_prob >= 75:
            heavy_rain_days += 1
            if first_heavy_rain_day is None:
                first_heavy_rain_day = idx
        elif r_mm >= 8.0 or r_prob >= 50:
            moderate_rain_days += 1

    # 3. Query Crop Knowledge Base
    crops = db.query(CropModel).all()
    results = []

    for crop in crops:
        # -------------------------------------------------------------
        # A. Lifecycle Climate Suitability (40% Weight)
        # -------------------------------------------------------------
        lifecycle_score = calculate_lifecycle_climate_score(
            location=weather["location"],
            start_month=current_month,
            duration_days=crop.duration_days or 120,
            crop_min_temp=crop.min_temp,
            crop_max_temp=crop.max_temp,
            crop_min_rainfall=crop.min_rainfall,
            crop_max_rainfall=crop.max_rainfall,
            water_req_str=crop.water_req
        )

        # -------------------------------------------------------------
        # B. Season Alignment Score (25% Weight)
        # -------------------------------------------------------------
        c_season = crop.season.lower()
        if current_season == "Kharif":
            if "kharif" in c_season or "monsoon" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season or "seasonal" in c_season:
                season_score = 90
            elif "summer" in c_season:
                season_score = 70
            else:
                season_score = 45 # Rabi crop planted in Kharif
        elif current_season == "Rabi":
            if "rabi" in c_season or "winter" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season or "seasonal" in c_season:
                season_score = 90
            elif "temperate" in c_season:
                season_score = 95
            else:
                season_score = 48 # Kharif crop planted in Rabi
        else: # Zaid (Summer)
            if "summer" in c_season or "zaid" in c_season:
                season_score = 96
            elif "perennial" in c_season or "year-round" in c_season:
                season_score = 90
            else:
                season_score = 65

        # -------------------------------------------------------------
        # C. Current Conditions Score (20% Weight)
        # -------------------------------------------------------------
        if crop.min_temp <= user_temp <= crop.max_temp:
            temp_score = 98
        elif user_temp < crop.min_temp:
            diff = crop.min_temp - user_temp
            temp_score = max(5, int(85 - diff * 7.5))
        else:
            diff = user_temp - crop.max_temp
            temp_score = max(5, int(85 - diff * 7.5))

        w_req = crop.water_req.lower()
        if "very high" in w_req or "high" in w_req:
            humidity_score = 95 if user_humidity >= 60 else max(20, int(95 - (60 - user_humidity) * 2.2))
        elif "low" in w_req:
            humidity_score = 95 if user_humidity <= 65 else max(20, int(95 - (user_humidity - 65) * 2.2))
        else:
            humidity_score = 92 if 45 <= user_humidity <= 80 else max(30, int(92 - abs(user_humidity - 62) * 1.5))

        current_conditions_score = int(0.70 * temp_score + 0.30 * humidity_score)
        current_conditions_score = max(5, min(99, current_conditions_score))

        # -------------------------------------------------------------
        # D. Short-Term Forecast Score & Sowing Window (15% Weight)
        # -------------------------------------------------------------
        w_cond_lower = weather_cond.lower()
        
        # Determine exact sowing window start and end
        if "snow" in w_cond_lower or user_temp <= 3.0:
            if "temperate" in c_season or crop.min_temp <= 4.0:
                forecast_score = 88
                sowing_status = "GOOD"
                start_offset = 0
                window_length = 4
                sowing_reason = f"Cold-hardy crop! Temperature ({user_temp}°C) suitable for high altitude sowing."
            else:
                forecast_score = 15
                sowing_status = "WAIT"
                start_offset = 7
                window_length = 5
                sowing_reason = f"Freezing temperatures ({user_temp}°C) risk seedling damage. Delay sowing until temperature rises above {crop.min_temp}°C."
        elif heavy_rain_days > 0 or max_forecast_prob >= 75:
            forecast_score = max(20, 80 - heavy_rain_days * 20 - int(total_7d_rain * 0.5))
            sowing_status = "WAIT"
            start_offset = (first_heavy_rain_day + 3) if first_heavy_rain_day is not None else 4
            window_length = 4
            sowing_reason = f"Heavy rainfall forecast ({max_forecast_prob}% probability, ~{int(total_7d_rain)}mm total). Delay sowing to avoid seed washout."
        elif moderate_rain_days > 0 or max_forecast_prob >= 50:
            forecast_score = 75
            sowing_status = "CAUTION"
            start_offset = 2
            window_length = 5
            sowing_reason = f"Moderate rainfall expected ({max_forecast_prob}% chance). Ensure proper field drainage before sowing."
        elif user_temp >= crop.max_temp + 2.0:
            forecast_score = 45
            sowing_status = "WAIT"
            start_offset = 5
            window_length = 4
            sowing_reason = f"High temperature alert ({user_temp}°C near crop limit of {crop.max_temp}°C). Delay sowing for cooler soil temperatures."
        else:
            forecast_score = 94
            sowing_status = "GOOD"
            start_offset = 0
            window_length = 5
            sowing_reason = "Optimal weather window! Soil moisture and short-term forecast are favorable for sowing."

        rec_start_dt = now + timedelta(days=start_offset)
        rec_end_dt = rec_start_dt + timedelta(days=window_length)

        sowing_window_obj = SowingWindowSchema(
            status=sowing_status,
            recommended_start=rec_start_dt.strftime("%Y-%m-%d"),
            recommended_end=rec_end_dt.strftime("%Y-%m-%d"),
            reason=sowing_reason
        )

        formatted_sowing_win = f"{rec_start_dt.strftime('%b %d')} – {rec_end_dt.strftime('%b %d')}"

        # -------------------------------------------------------------
        # E. Final Weighted Recommendation Score Calculation
        # -------------------------------------------------------------
        final_score = int(
            SCORING_WEIGHTS["lifecycle_climate"] * lifecycle_score +
            SCORING_WEIGHTS["season"] * season_score +
            SCORING_WEIGHTS["current_conditions"] * current_conditions_score +
            SCORING_WEIGHTS["forecast"] * forecast_score
        )

        # Disqualification Cap for incompatible climate or season
        if temp_score < 20:
            final_score = min(final_score, temp_score + 10)
        if lifecycle_score < 25:
            final_score = min(final_score, lifecycle_score + 15)

        final_score = max(5, min(98, final_score))

        if final_score >= 82:
            rating = "Highly Suitable"
        elif final_score >= 65:
            rating = "Suitable"
        elif final_score >= 45:
            rating = "Moderate"
        else:
            rating = "Low Suitability"

        # Risk breakdown
        risk_warnings = []
        if sowing_status == "WAIT":
            risk_warnings.append(sowing_reason)
            risk_level = "HIGH" if heavy_rain_days > 1 or user_temp <= 3.0 else "MEDIUM"
            risk_score = 45 if risk_level == "HIGH" else 65
        elif sowing_status == "CAUTION":
            risk_warnings.append(sowing_reason)
            risk_level = "MEDIUM"
            risk_score = 72
        else:
            risk_level = "LOW"
            risk_score = 90
            risk_warnings.append("No major short-term weather risks detected.")

        reasons = [
            f"Historical lifecycle climate suitability is {lifecycle_score}% for {weather['location']}",
            f"Aligned with {crop.season} season ({season_score}% alignment score)",
            f"Current temperature ({user_temp}°C) & humidity ({user_humidity}%) fit {crop.name} requirements",
            f"Short-term forecast score is {forecast_score}%"
        ]

        # Growth Stages Calculation
        dur = crop.duration_days or 120
        s1 = max(4, int(dur * 0.08))
        s2 = s1 + max(10, int(dur * 0.20))
        s3 = s2 + max(15, int(dur * 0.30))
        s4 = s3 + max(15, int(dur * 0.25))

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
            match_score=final_score,
            suitability_rating=rating,
            scores=ScoreBreakdown(
                lifecycle_climate=lifecycle_score,
                season=season_score,
                current_conditions=current_conditions_score,
                forecast=forecast_score
            ),
            risk=RiskBreakdown(
                level=risk_level,
                score=risk_score,
                warnings=risk_warnings
            ),
            sowing_window=sowing_window_obj,
            duration_days=dur,
            growth_stages=growth_stages,
            reasons=reasons,
            risk_factors=risk_warnings,
            expected_yield=crop.expected_yield,
            suggested_sowing_window=formatted_sowing_win,
            sowing_status=sowing_status
        ))

    # Sort descending by match_score
    results.sort(key=lambda x: x.match_score, reverse=True)

    top_crop = results[0] if results else None
    if top_crop:
        if top_crop.sowing_window.status == "GOOD":
            advisory = (
                f"Conditions in {weather['location']} ({user_temp}°C, {user_humidity}% humidity) strongly favor sowing {top_crop.crop_name} "
                f"with top suitability rating ({top_crop.match_score}%). Recommended sowing window: {top_crop.suggested_sowing_window}."
            )
        elif top_crop.sowing_window.status == "CAUTION":
            advisory = (
                f"Weather alert for {weather['location']}: {top_crop.sowing_window.reason} "
                f"Recommended sowing window for {top_crop.crop_name}: {top_crop.suggested_sowing_window}."
            )
        else:
            advisory = (
                f"Weather risk alert in {weather['location']}: {top_crop.sowing_window.reason} "
                f"Delay sowing {top_crop.crop_name} until recommended window: {top_crop.suggested_sowing_window}."
            )
    else:
        advisory = "No recommendations generated."

    return RecommendationResponse(
        location=weather["location"],
        season=current_season,
        temperature=user_temp,
        humidity=user_humidity,
        rain_probability=user_rain_prob,
        rainfall_expected=user_rain_mm,
        condition=weather_cond,
        top_recommendations=results[:12],
        sowing_advisory=advisory,
        is_demo=is_demo
    )
