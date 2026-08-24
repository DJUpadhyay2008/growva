# Growva Smart Farming Backend

Production-grade FastAPI backend for the **Growva** Smart Agriculture Platform.

## Architecture

- **Framework**: FastAPI (Python 3.10+)
- **ORM & DB**: SQLAlchemy with SQLite (`growva.db`)
- **Validation**: Pydantic v2 & Pydantic-Settings
- **API Version**: `v1` (`/api/v1`)

## Key Modules & Endpoints

| Router | Method | Path | Description |
|---|---|---|---|
| Health | `GET` | `/health` | Server health monitor |
| Crops | `GET` | `/api/v1/crops` | 120+ Produce catalog with group & name search filters |
| Crops | `GET` | `/api/v1/crops/{id}` | Detailed agronomic guide for specific crop |
| Weather | `GET` | `/api/v1/weather` | Current weather, 7-day forecast & rain window alerts |
| Recommendations | `POST` | `/api/v1/recommendations` | Hybrid suitability scoring engine |
| Planner | `GET` | `/api/v1/planner/tasks` | Active field stage tracking & recommendations |
| Planner | `POST` | `/api/v1/planner/tasks` | Create new farm field stage plan |
| Mandi Prices | `GET` | `/api/v1/mandi` | Live Mandi prices across commodities & states |
| Schemes | `GET` | `/api/v1/schemes` | Government scheme search (PM-KISAN, PMFBY, KUSUM) |
| Schemes | `POST` | `/api/v1/schemes/eligibility` | Automated farmer scheme eligibility checker |
| Disease | `POST` | `/api/v1/disease/diagnose` | AI pest & disease diagnostic engine |

## Running locally

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Run database seed (auto-runs on startup, or manually)
python app/database/seed.py

# 3. Start Uvicorn development server
python run.py
```

Swagger API Docs available at: `http://localhost:8000/api/v1/docs`
