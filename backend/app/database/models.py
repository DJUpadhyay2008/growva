from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from datetime import datetime
from app.database.database import Base

class CropModel(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    hindi_name = Column(String(100), nullable=True)
    gujarati_name = Column(String(100), nullable=True)
    category = Column(String(50), index=True, nullable=False) # Crops, Pulses, Vegetables, Fruits, Spices
    season = Column(String(100), nullable=False)
    soil_type = Column(String(100), nullable=False)
    water_req = Column(String(50), nullable=False)
    duration_days = Column(Integer, default=90)
    min_temp = Column(Float, default=15.0)
    max_temp = Column(Float, default=38.0)
    min_rainfall = Column(Float, default=400.0) # mm
    max_rainfall = Column(Float, default=1500.0) # mm
    ideal_ph_min = Column(Float, default=6.0)
    ideal_ph_max = Column(Float, default=7.5)
    expected_yield = Column(String(100), default="Regional estimate")
    image_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    byproducts = Column(Text, nullable=True)
    common_pests = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class WeatherLogModel(Base):
    __tablename__ = "weather_logs"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), index=True, nullable=False)
    temp_c = Column(Float, nullable=False)
    humidity_pct = Column(Float, nullable=False)
    wind_kmh = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False)
    condition = Column(String(100), nullable=False)
    forecast_data = Column(Text, nullable=False) # JSON string of forecast
    created_at = Column(DateTime, default=datetime.utcnow)


class PlannerTaskModel(Base):
    __tablename__ = "planner_tasks"

    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String(100), nullable=False) # e.g. Field A
    crop_name = Column(String(100), nullable=False) # e.g. Wheat
    sowing_date = Column(String(50), nullable=False)
    expected_harvest = Column(String(50), nullable=False)
    stage_name = Column(String(100), nullable=False) # e.g. Soil prep, Sowing, First irrigation, Harvest
    progress_pct = Column(Integer, default=0)
    soil_moisture_pct = Column(Integer, default=35)
    weather_alert = Column(Text, nullable=True)
    daily_recommendation = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class MandiPriceModel(Base):
    __tablename__ = "mandi_prices"

    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), index=True, nullable=False)
    district = Column(String(100), nullable=False)
    market = Column(String(100), nullable=False)
    commodity = Column(String(100), index=True, nullable=False)
    variety = Column(String(100), nullable=True)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    arrival_date = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class GovernmentSchemeModel(Base):
    __tablename__ = "government_schemes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # e.g. PM-KISAN
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False) # Income Support, Insurance, Solar Irrigation, Soil Testing
    short_description = Column(Text, nullable=False)
    full_description = Column(Text, nullable=False)
    benefit_amount = Column(String(100), nullable=False)
    eligibility_criteria = Column(Text, nullable=False)
    required_documents = Column(Text, nullable=False)
    apply_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DiseaseRecordModel(Base):
    __tablename__ = "disease_records"

    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100), index=True, nullable=False)
    disease_name = Column(String(150), nullable=False)
    symptoms = Column(Text, nullable=False)
    cause = Column(String(200), nullable=True)
    organic_treatment = Column(Text, nullable=False)
    chemical_treatment = Column(Text, nullable=False)
    preventive_measures = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
