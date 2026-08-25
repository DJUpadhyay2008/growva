import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Growva Smart Farming API"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./growva.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL: str = db_url
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "*"
    ]
    
    # Default Location for Weather & Agronomic Engine
    DEFAULT_LOCATION: str = "Ahmedabad, Gujarat"
    
    class Config:
        case_sensitive = True

settings = Settings()

