# 🌿 Growva — Smart Agriculture & Weather-Aware Farm Planner

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB.svg?style=flat&logo=react)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Growva** is an intelligent, full-stack digital workspace designed for modern agriculture. It provides weather-aware crop suitability analysis, location-based sowing recommendations, dynamic crop growth stage planning, market price comparison, and multilingual support for 22 scheduled Indian languages.

---

## ✨ Features

- 🌾 **Weather-Aware Crop Recommendations**: Hybrid recommendation engine evaluating climate fit, real-time forecast risks, and agronomic requirements.
- 📅 **Dynamic Farm Planner**: Interactive sowing-to-harvest lifecycle timeline with milestone date tracking customized to your location.
- ⛅ **Real-Time Weather Intelligence**: Location-based weather forecasting via Open-Meteo with fallback support for offline/demo scenarios.
- 📚 **Comprehensive Produce Library**: Curated guidance on 120+ Indian crops, vegetables, fruits, pulses, and spices.
- 🏛️ **Government Schemes & Subsidies**: Direct discovery for PM-KISAN, PMFBY, PM-KUSUM, and Soil Health Card initiatives.
- 🌐 **Multilingual Platform**: Built-in support for 22 scheduled Indian languages (English, Hindi, Gujarati, Marathi, Punjabi, Tamil, etc.).

---

## 📁 Project Architecture

```
growva/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoints
│   │   ├── config.py        # Environment & CORS configuration
│   │   ├── database/        # SQLite / SQLAlchemy models & seeder script
│   │   ├── schemas/         # Pydantic schemas for data validation
│   │   └── services/        # Recommendation engine & Open-Meteo weather service
│   ├── run.py               # Uvicorn server entrypoint
│   └── requirements.txt     # Python backend dependencies
│
└── frontend/
    ├── public/              # High-resolution produce assets & icons
    ├── src/
    │   ├── assets/          # 3D visuals & reference guides
    │   ├── services/        # API client for backend communication
    │   ├── main.jsx         # App entrypoint & PlannerSection component
    │   └── styles.css       # Custom design system with dark green aesthetic
    ├── index.html
    └── package.json         # Vite + React configuration
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

---

### 2. Backend Setup & Startup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python run.py
```

- **Interactive API Documentation (Swagger)**: `http://localhost:8000/api/v1/docs`

---

### 3. Frontend Setup & Startup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the Vite development server
npm run dev
```

- **Web Application URL**: `http://localhost:5173` (or `http://localhost:5178`)

---

## 🛠️ API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status check |
| `POST` | `/api/v1/recommendations` | Location & weather-aware crop suitability analysis |
| `GET` | `/api/v1/crops` | List all database crops with growth stages |
| `GET` | `/api/v1/weather` | Fetch weather forecast for specified location |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
