from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os
import resend

# Top-level package (sibling to backend)
from DataPipeline.openrouter_client import generate

# Backend package imports
from backend.app.routes import location, risk, chat
from backend.app.services.supabase_client import supabase

load_dotenv()

app = FastAPI()

# Register routers
app.include_router(location.router)
app.include_router(risk.router)
app.include_router(chat.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Dataset Configuration
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

if not RISK_FILE.exists():
    raise RuntimeError("Risk dataset not found. Ensure parquet file is generated.")

risk_df = pd.read_parquet(RISK_FILE)

COUNTRY_MAP = {
    "AGO": "Angola", "BDI": "Burundi", "BEN": "Benin",
    "BFA": "Burkina Faso", "BWA": "Botswana",
    "CAF": "Central African Republic", "CIV": "Côte d'Ivoire",
    "CMR": "Cameroon", "COD": "Democratic Republic of the Congo",
    "COG": "Republic of the Congo", "COM": "Comoros",
    "CPV": "Cape Verde", "DJI": "Djibouti", "DZA": "Algeria",
    "EGY": "Egypt", "ERI": "Eritrea", "ETH": "Ethiopia",
    "GAB": "Gabon", "GHA": "Ghana", "GIN": "Guinea",
    "GMB": "Gambia", "GNB": "Guinea-Bissau",
    "GNQ": "Equatorial Guinea", "KEN": "Kenya",
    "LBR": "Liberia", "LBY": "Libya", "LSO": "Lesotho",
    "MAR": "Morocco", "MDG": "Madagascar", "MLI": "Mali",
    "MOZ": "Mozambique", "MRT": "Mauritania",
    "MUS": "Mauritius", "MWI": "Malawi", "NAM": "Namibia",
    "NER": "Niger", "NGA": "Nigeria", "RWA": "Rwanda",
    "SDN": "Sudan", "SEN": "Senegal", "SLE": "Sierra Leone",
    "SOM": "Somalia", "SSD": "South Sudan",
    "SWZ": "Eswatini", "TCD": "Chad", "TGO": "Togo",
    "TUN": "Tunisia", "TZA": "Tanzania", "UGA": "Uganda",
    "ZAF": "South Africa", "ZMB": "Zambia", "ZWE": "Zimbabwe"
}

# =========================
# AI Prompt Builder
# =========================

def build_prompt(row):
    return f"""
You are an expert climate risk analyst.

Region ID: {row['region_id']}
Region Name: {row.get('region_name', 'Unknown')}
Country Code: {row.get('country_code', 'Unknown')}

Recent rainfall mean: {row['rainfall_mean_recent']:.2f} mm
Baseline rainfall mean: {row['rainfall_mean_normal']:.2f} mm
Rainfall anomaly: {row['anomaly']:.2f} mm
Risk level: {row['risk_level']}

Explain this risk clearly in simple language and give one practical recommendation
for communities or local authorities. Keep it under 120 words.
"""

# =========================
# Email Service
# =========================

def send_confirmation_email(to_email: str):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        print("RESEND_API_KEY not set.")
        return

    resend.api_key = api_key

    try:
        resend.Emails.send({
            "from": "Ecopulse <onboarding@resend.dev>",
            "to": to_email,
            "subject": "Ecopulse Subscription Confirmed",
            "html": """
                <strong>You're subscribed to Ecopulse!</strong><br><br>
                You will now receive rainfall risk alerts for your selected region.<br><br>
                Stay safe and prepared.
            """
        })
    except Exception as e:
        print(f"Resend error: {e}")

# =========================
# Schemas
# =========================

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

# =========================
# Health Check
# =========================

@app.get("/health")
def health_check():
    return {"status": "ok"}

# =========================
# Subscription Endpoints
# =========================

@app.post("/subscribe")
def subscribe(data: SubscriptionRequest):

    if supabase is None:
        raise HTTPException(status_code=500, detail="Database unavailable")

    subscription_data = {
        "email": data.email.strip().lower(),
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

    try:
        response = (
            supabase
            .table("subscribers")
            .insert(subscription_data)
            .execute()
        )
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=409, detail="Email already subscribed")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if data.email_delivery:
        send_confirmation_email(data.email)

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
        .eq("email", data.email.strip().lower())
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "You have successfully unsubscribed"}