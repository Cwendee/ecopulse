from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

from app.routes import location, risk, chat
from app.services.supabase_client import supabase
from app.services.gpt_oss_client import generate

load_dotenv()

app = FastAPI()

# ============================
# Register Routers
# ============================

app.include_router(location.router)
app.include_router(risk.router)
app.include_router(chat.router)

# ============================
# CORS
# ============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Load Risk Dataset
# ============================

BASE_DIR = Path(__file__).resolve().parents[2]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

risk_df = pd.read_parquet(RISK_FILE)

# ============================
# Utility Function
# ============================

def build_prompt(row):
    return f"""
You are an expert climate risk analyst.

Region ID: {row['region_id']}
Region Name: {row.get('shapeName', 'Unknown')}
Country: {row.get('shapeGroup', 'Unknown')}

Recent rainfall mean: {row['rainfall_mean_recent']:.2f} mm
Baseline rainfall mean: {row['rainfall_mean_normal']:.2f} mm
Rainfall anomaly: {row['anomaly']:.2f} mm
Risk level: {row['risk_level']}

Explain this risk clearly in simple language and give one practical recommendation
for communities or local authorities. Keep it under 120 words.
"""

# ============================
# Pydantic Models
# ============================

class SubscriptionRequest(BaseModel):
    email: EmailStr
    country: str
    region: str
    region_id: str
    severe_alerts: bool = False
    early_alerts: bool = False
    preparedness_reminders: bool = False
    email_delivery: bool = True
    in_app_delivery: bool = False
    browser_delivery: bool = False


class UnsubscribeRequest(BaseModel):
    email: EmailStr

# ============================
# Health
# ============================

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ============================
# Subscription Endpoints
# ============================

@app.post("/subscribe")
def subscribe(data: SubscriptionRequest):

    if supabase is None:
        raise HTTPException(status_code=500, detail="Database unavailable")

    subscription_data = {
        "email": data.email,
        "country": data.country,
        "region": data.region,
        "region_id": data.region_id,
        "severe_alerts": data.severe_alerts,
        "early_alerts": data.early_alerts,
        "preparedness_reminders": data.preparedness_reminders,
        "email_delivery": data.email_delivery,
        "in_app_delivery": data.in_app_delivery,
        "browser_delivery": data.browser_delivery,
        "alert_enabled": True,
    }

    response = (
        supabase.table("subscribers")
        .upsert(subscription_data, on_conflict="email")
        .execute()
    )

    return {
        "message": "Subscription saved successfully",
        "data": response.data,
    }


@app.delete("/unsubscribe")
def unsubscribe(data: UnsubscribeRequest):

    if supabase is None:
        raise HTTPException(status_code=500, detail="Database unavailable")

    response = (
        supabase.table("subscribers")
        .update({"alert_enabled": False})
        .eq("email", data.email)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "You have successfully unsubscribed"}

# ============================
# Countries Endpoint
# ============================

@app.get("/countries")
def get_countries():

    if "shapeGroup" not in risk_df.columns:
        raise HTTPException(status_code=500, detail="Country column not found")

    countries = (
        risk_df["shapeGroup"]
        .dropna()
        .unique()
        .tolist()
    )

    countries.sort()

    return {"countries": countries}

# ============================
# Regions by Country
# ============================

@app.get("/countries/{country}/regions")
def get_regions(country: str):

    if "shapeGroup" not in risk_df.columns:
        raise HTTPException(status_code=500, detail="Country column not found")

    filtered = risk_df[
        risk_df["shapeGroup"].str.lower() == country.lower()
    ]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="Country not found")

    regions = (
        filtered[["region_id", "shapeName"]]
        .dropna()
        .drop_duplicates()
    )

    return {
        "country": country,
        "regions": regions.to_dict(orient="records"),
    }

# ============================
# Risk Data Endpoint
# ============================

@app.get("/risk/{region_id}")
def get_risk(region_id: str):

    row = risk_df[risk_df["region_id"] == region_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    row_data = row.iloc[0]

    return {
        "region_id": row_data["region_id"],
        "region_name": row_data.get("shapeName"),
        "country": row_data.get("shapeGroup"),
        "risk_level": row_data["risk_level"],
        "rainfall_mean_recent": row_data["rainfall_mean_recent"],
        "rainfall_mean_normal": row_data["rainfall_mean_normal"],
        "anomaly": row_data["anomaly"],
        "valid_at": row_data["valid_at"],
    }

# ============================
# AI Risk Explanation
# ============================

@app.get("/risk/{region_id}/explain")
def explain_risk(region_id: str):

    row = risk_df[risk_df["region_id"] == region_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    row_data = row.iloc[0]
    prompt = build_prompt(row_data)

    explanation = generate(prompt)

    return {
        "region_id": region_id,
        "risk_level": row_data["risk_level"],
        "explanation": explanation,
    }

# ============================
# Debug Columns Endpoint
# ============================

@app.get("/debug/columns")
def debug_columns():
    return {"columns": risk_df.columns.tolist()}