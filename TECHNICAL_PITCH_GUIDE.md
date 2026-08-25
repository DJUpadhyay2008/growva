# 🌿 Growva — Technical Pitch & Judge Presentation Guide

Use this comprehensive guide when presenting to judges, pitching the product, or answering technical Q&A during evaluation sessions.

---

## 🎯 1. Executive Summary (30-Second Elevator Pitch)

> *"Growva is an intelligent, full-stack precision agriculture platform built to empower Indian smallholder farmers. Rather than providing static agricultural advice, Growva integrates **real-time weather telemetry**, a **hybrid agronomic suitability scoring engine**, **multi-LLM AI advisories with automatic server-side failover**, **crop residue circular economy monetization**, and **automated government scheme matching** across **22 scheduled Indian languages**."*

---

## 🏗️ 2. System Architecture & Technology Stack

```
                   ┌──────────────────────────────────────────────┐
                   │             React 18 + Vite SPA              │
                   │ (Framer Motion, Glassmorphism, 22 Languages) │
                   └──────────────────────┬───────────────────────┘
                                          │  REST APIs / JSON
                                          ▼
                   ┌──────────────────────────────────────────────┐
                   │             FastAPI Async Server             │
                   │    (Pydantic Validation, CORS, Uvicorn)      │
                   └──────┬───────────────┬───────────────┬───────┘
                          │               │               │
        ┌─────────────────┴─┐   ┌─────────┴─────────┐   ┌─┴────────────────┐
        ▼                   ▼   ▼                   ▼   ▼                  ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Hybrid Crop   │   │ Multi-Model   │   │ Residue &     │   │ Government    │
│ Suitability   │   │ AI Chatbot    │   │ Byproduct     │   │ Scheme        │
│ Scoring Engine│   │ (Gemini/GLM)  │   │ Calculator    │   │ Rules Engine  │
└───────┬───────┘   └───────────────┘   └───────────────┘   └───────────────┘
        │
        ├────────────────────────┬────────────────────────┐
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐        ┌───────────────┐
│  SQLite DB    │        │  Open-Meteo   │        │ Mandi Data    │
│ (Crop Knowledge)       │  Weather API  │        │ Prices Engine │
└───────────────┘        └───────────────┘        └───────────────┘
```

### Stack Breakdown:
* **Frontend**: React 18 Single Page Application (SPA) bundled via Vite. Modern UI built with dark-green glassmorphism aesthetics, dynamic Framer Motion micro-animations, and Lucide vector icons.
* **Backend**: FastAPI (Python 3.12) running asynchronously with Pydantic v2 data validation and auto-generated Swagger documentation (`/api/v1/docs`).
* **Database & Knowledge Base**: SQLite via SQLAlchemy ORM containing structured data for 120+ crops, growth stages, fertilizer formulas, and government schemes.
* **Weather Service**: Open-Meteo integration fetching hyper-local forecasts without third-party rate limits or key bottlenecks.

---

## ⚙️ 3. Core Technical Modules & Features

### 1. Hybrid Crop Suitability Scoring Engine (`RecommendationService`)
* **Climate Matching**: Evaluates target location parameters (temp bounds $T_{min}/T_{max}$, rainfall, soil pH) against crop agronomic requirements.
* **Forecast Risk Penalty (`RiskService`)**: Scans 7-to-14 day weather forecasts. If frost, heatwaves, or unexpected heavy rain fall within the critical sowing window, the crop score is penalized with a warning tag.
* **Dynamic Score Output**: Generates 0–100 suitability scores categorized into *Highly Suitable*, *Moderate*, or *High Risk*.

---

### 2. Multi-LLM AI Chatbot with Server-Side Failover (`chat.py`)
* **Primary LLM**: Google Gemini (`gemini-1.5-flash`, `gemini-1.5-pro`).
* **Secondary LLM**: OpenRouter (`z-ai/glm-5.2:free`).
* **Resilient Failover**: If the primary endpoint encounters rate limits (HTTP 429) or timeouts, backend requests automatically failover to secondary endpoints, ensuring zero live demo interruptions.

---

### 3. Circular Economy & Byproduct Monetization Engine (`ByproductService`)
* Addresses **stubble burning (Parali)** by converting agricultural waste into revenue.
* Calculates residue volume (tons/acre) for crops like wheat straw, paddy stubble, and sugarcane bagasse.
* Recommends monetization pathways: Bio-pellets, mushroom cultivation substrate, paper pulp, or organic compost.
* Displays estimated extra income (₹/acre).

---

### 4. Automated Government Scheme Eligibility Engine (`SchemeService`)
* Evaluates landholding size (small/marginal vs large), crop selection, state location, and social category.
* Returns tailored matches for PM-KISAN, PMFBY, PM-KUSUM, Soil Health Card, and state-specific schemes with direct application links.

---

### 5. Resilient Crop Disease Diagnosis
* High-resolution diagnostic assets hosted locally in `frontend/public/diseases/` for offline reliability.
* React visual fallbacks (`ImageOff`) preventing UI breaks during connectivity delays.

---

## 💡 4. Key Differentiators to Emphasize to Judges

1. **Weather-Aware Analysis vs. Static Lists**: Analyzes upcoming 14-day weather risks *before* sowing.
2. **Zero-Downtime AI Engine**: Multi-LLM fallback architecture guarantees robust demo performance.
3. **Environmental & Economic Impact**: Directly combats stubble burning through residue monetization.
4. **Inclusive Design**: Native multi-lingual interface support for **22 scheduled Indian languages**.

---

## 🏆 5. Q&A Cheatsheet for Judges

| Potential Question | Winning Technical Answer |
| :--- | :--- |
| **"Where do you get live weather data?"** | *"We pull hyper-local forecasts from the Open-Meteo API using latitude/longitude coordinates with server-side caching."* |
| **"How is crop suitability calculated?"** | *"Via a hybrid scoring algorithm combining static climate bounds with dynamic 14-day forecast risk penalty calculations."* |
| **"What if your AI API key rate limits during a pitch?"** | *"Our backend features multi-LLM automated failover; if Gemini rate limits, traffic routes instantaneously to OpenRouter."* |
| **"How does Growva address stubble burning?"** | *"Through our Byproduct Engine, which estimates residue tonnage per crop and connects farmers with bio-energy and composting revenue streams."* |
