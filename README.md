## 🌊 Ecopulse

## Overview

Ecopulse is a web-based flood risk awareness and early warning platform designed for flood-prone communities across Africa.

The platform translates rainfall and climate data into simple, location-specific preparedness guidance that residents and small and medium-sized enterprises (SMEs) can use to take proactive action.

Rather than predicting floods in real time, Ecopulse converts existing rainfall indicators into understandable regional risk levels that support early awareness and preparedness.

## Problem Context

Flooding remains one of the most frequent and destructive climate-related hazards across many African regions. Although rainfall and climate datasets exist, communities often receive information that is:

* Late

* Too technical

* Not location specific

* Not actionable

This results in avoidable consequences such as:

* Property damage

* Business interruption

* Income loss

* Displacement

* Increased safety risks

Ecopulse bridges the gap between climate data availability and practical, community level action.


## Solution Summary

Ecopulse provides:

* Location-based flood risk summaries at the ADM2 (regional) level

* Deterministic rainfall-based flood risk classification

* Plain-language explanations via the ECO assistant

* Email subscription for early flood alerts

* A scalable backend API for risk processing and integration

The MVP focuses on accessibility, transparency, and explainability — not complex predictive modeling.


## 🌧 Deterministic Risk Engine (MVP Design)

Ecopulse uses a rainfall-based flood risk proxy powered by CHIRPS Daily rainfall data from Digital Earth Africa.

For the MVP:

* Risk Score = Recent Rainfall / Historical Mean Rainfall

* Risk classification is rule-based (no machine learning)

* Same input always produces the same output (deterministic logic)


Risk categories:

* Low

* Moderate

* High

* Unknown (if rainfall data is missing)


This approach ensures:

* Transparency

* Reproducibility

* Fast execution

* Clear interpretability


## 📊 Data Sources

* CHIRPS Daily Rainfall Dataset (Digital Earth Africa STAC API)

* geoBoundaries ADM2 Administrative Boundaries (Africa subset)

Ecopulse does not generate new climate predictions. It translates publicly available rainfall indicators into structured preparedness insights.


## ⚠ Disclaimer

Ecopulse does not predict floods in real time and does not coordinate emergency response.

The platform translates rainfall-based indicators into simplified regional preparedness guidance.

Risk levels are rainfall-based proxies and should not be interpreted as official emergency warnings.



## SDG Alignment

SDG 13: Climate Action

Ecopulse contributes by:

* Enhancing adaptive capacity to climate related hazards

* Supporting early preparedness and awareness

* Encouraging informed decision-making before disasters occur


## 🏗 Architecture Overview 

Ecopulse is structured into three main layers:

- **Frontend Layer** – User interface for location search, map visualization, alerts, and ECO assistant.
- **Backend API Layer** – FastAPI service responsible for location resolution, risk lookup, and AI explanations.
- **Data Intelligence Layer** – Deterministic rainfall-based flood risk engine powered by CHIRPS data.

The diagram below illustrates how these components interact:

```mermaid
flowchart TD

    %% =========================
    %% Frontend Layer
    %% =========================
    USER[User]
    FE[Frontend Web App]

    USER --> FE

    FE -->|GET /countries| API
    FE -->|GET /countries/:code/regions| API
    FE -->|GET /risk/:region_id| API
    FE -->|GET /risk/:region_id/explain| API
    FE -->|POST /subscribe| API

    %% =========================
    %% Backend Layer
    %% =========================
    API[FastAPI Backend]

    API --> PARQUET[(risk_africa.parquet)]
    API --> SUPA[(Supabase - Subscribers)]
    API --> OPENROUTER[OpenRouter API]

    OPENROUTER --> GPT[openai/gpt-4o-mini]

    %% =========================
    %% Data Science Processing
    %% =========================
    CHIRPS[CHIRPS Daily Rainfall]
    ADM2[geoBoundaries ADM2]
    RAIN[rainfall.py]
    RISK[risk.py]
    PIPE[pipeline.py]

    CHIRPS --> RAIN
    RAIN --> PIPE
    ADM2 --> PIPE
    RISK --> PIPE

    PIPE --> PARQUET

    %% =========================
    %% Scheduler
    %% =========================
    SCHED[Scheduled Job<br/>Cron / GitHub Action]
    SCHED --> PIPE
```

### 🔄 End-to-End Flow

1. Scheduled job (Cron / GitHub Action) triggers the daily rainfall pipeline.
2. Pipeline processes CHIRPS rainfall data and aggregates it by ADM2 region.
3. Deterministic risk classification logic is applied.
4. Regional metadata from geoBoundaries ADM2 is merged.
5. risk_africa.parquet is generated/updated as the serving dataset.
6. FastAPI backend exposes structured endpoints for countries, regions, and risk data.
7. On explanation requests, the backend sends risk metrics to OpenRouter (gpt-4o-mini) for natural-language summaries.
8. Subscription requests are stored in Supabase.
9. Frontend consumes the API and renders the dropdown-based location and risk flow.


## Live Backend URL
https://ecopulse-ndki.onrender.com/

Swagger Documentation:
https://ecopulse-ndki.onrender.com/docs


## Backend API Endpoints

# GET /health

- Checks whether the backend service is running.

Example response:

```bash
{
  "status": "ok"
}
```

# GET /countries

Returns list of supported countries.

Example response:

```bash
{
  "countries": [
    { "code": "NGA", "name": "Nigeria" }
  ]
}
```

# GET /countries/{country_code}/regions

Returns ADM2 regions for a selected country.

Example:

```bash
GET /countries/NGA/regions
```

# GET /risk/{region_id}

Returns latest deterministic rainfall-based risk data for a region.

Example:

```bash
GET /risk/NG-LA-IKJ
```

# GET /risk/{region_id}/explain

Generates a plain-language risk explanation.

POST /subscribe

Registers a user for flood alert notifications.

DELETE /unsubscribe

Disables alert notifications for a subscribed email.

## Database Schema

# Table: risk_adm2_daily

* region_id (primary key)

* country

* adm2_name

* valid_at

* rainfall_index

* anomaly

* rainfall_percentile

* risk_level

* data_quality


# Table: subscribers

* id (UUID)

* email (unique)

* country

* region

* region_id

* alert_enabled

* severe_alerts

* early_alerts

* preparedness_reminders

* email_delivery

* in_app_delivery

* browser_delivery

* created_at



## Local Development (Backend)

1. Clone the repository

2. Navigate to backend directory

3. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Create a .env file with:

```bash

SUPABASE_URL=your_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

GPT_OSS_BASE_URL=your_llm_gateway_url
GPT_OSS_API_KEY=your_api_key
GPT_OSS_MODEL=gpt-oss-120gb

RESEND_API_KEY=your_resend_api_key

```

6. Run the server

```bash
uvicorn app.main:app --reload
```

7. Open

http://127.0.0.1:8000/docs


## Project Status

* Backend API deployed and operational

* Supabase integration complete

* Deterministic rainfall-based risk engine integrated

* Location resolution via ADM2 mapping

* ECO assistant integration in progress

* Daily automated risk pipeline pending final integration






