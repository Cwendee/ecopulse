from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os

from app.routes import location, risk, chat
from app.services.supabase_client import supabase

load_dotenv()

app = FastAPI()

# Register routers
app.include_router(location.router)
app.include_router(risk.router)
app.include_router(chat.router)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict later to Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
# Endpoints
# ============================

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/subscribe")
def subscribe(data: SubscriptionRequest):
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
        "alert_enabled": True
    }

    response = (
        supabase.table("subscribers")
        .upsert(subscription_data, on_conflict="email")
        .execute()
    )

    return {
        "message": "Subscription saved successfully",
        "data": response.data
    }


@app.delete("/unsubscribe")
def unsubscribe(data: UnsubscribeRequest):
    response = (
        supabase.table("subscribers")
        .update({"alert_enabled": False})
        .eq("email", data.email)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "You have successfully unsubscribed"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

from DataPipeline.gpt_oss_client import generate
from app.routes import location, risk, chat
from app.services.supabase_client import supabase

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
# Health Endpoint
# ============================

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ============================
# Subscription Endpoints
# ============================

@app.post("/subscribe")
def subscribe(data: SubscriptionRequest):

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
# Risk Explanation Integration
# ============================

BASE_DIR = Path(__file__).resolve().parents[2]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

# Load once at startup (much faster)
risk_df = pd.read_parquet(RISK_FILE)


def build_prompt(row):
    return f"""
You are an expert climate risk analyst.

Region ID: {row['region_id']}

Recent rainfall mean: {row['rainfall_mean_recent']:.2f} mm
Baseline rainfall mean: {row['rainfall_mean_normal']:.2f} mm
Rainfall anomaly: {row['anomaly']:.2f} mm
Risk level: {row['risk_level']}

Explain this risk clearly in simple language and give one practical recommendation
for communities or local authorities. Keep it under 120 words.
"""


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

@app.get("/debug/regions")
def debug_regions():
    df = load_risk_data()
    return df["region_id"].head().tolist()

