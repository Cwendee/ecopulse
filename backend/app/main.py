from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Load Risk Dataset
# ============================

BASE_DIR = Path(__file__).resolve().parents[2]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

if not RISK_FILE.exists():
    raise RuntimeError("Risk dataset not found. Ensure parquet file is generated.")

risk_df = pd.read_parquet(RISK_FILE)

# ============================
# Utility Function
# ============================

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

# ============================
# Email Utility
# ============================

def send_confirmation_email(to_email: str):
    api_key = os.getenv("SENDGRID_API_KEY")

    if not api_key:
        print("SENDGRID_API_KEY not set. Skipping email send.")
        return

    message = Mail(
        from_email="no-reply@ecopulse.app",  # Must be verified in SendGrid
        to_emails=to_email,
        subject="Ecopulse Subscription Confirmed",
        html_content="""
        <strong>You're subscribed to Ecopulse!</strong><br><br>
        You will now receive rainfall risk alerts for your selected region.<br><br>
        Stay safe and prepared.
        """
    )

    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        print(f"Confirmation email sent to {to_email}")
    except Exception as e:
        print(f"SendGrid error: {e}")

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
# Countries Endpoint
# ============================

@app.get("/countries")
def get_countries():
    countries = (
        risk_df["country_code"]
        .dropna()
        .unique()
        .tolist()
    )
    countries.sort()
    return {"countries": countries}

# ============================
# Regions by Country Code
# ============================

@app.get("/countries/{country_code}/regions")
def get_regions(country_code: str):

    filtered = risk_df[
        risk_df["country_code"].str.upper() == country_code.upper()
    ]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="Country not found")

    regions = (
        filtered[["region_id", "region_name"]]
        .drop_duplicates()
        .to_dict(orient="records")
    )

    return {
        "country_code": country_code.upper(),
        "regions": regions,
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
        "region_name": row_data.get("region_name"),
        "country_code": row_data.get("country_code"),
        "risk_level": row_data["risk_level"],
        "rainfall_mean_recent": row_data["rainfall_mean_recent"],
        "rainfall_mean_normal": row_data["rainfall_mean_normal"],
        "anomaly": row_data["anomaly"],
        "valid_at": row_data["valid_at"],
        "rainfall_percentile": row_data["rainfall_percentile"],
        "data_quality": row_data["data_quality"],
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

    try:
        explanation = generate(prompt)
    except Exception:
        explanation = "Unable to generate AI explanation at the moment."

    return {
        "region_id": region_id,
        "risk_level": row_data["risk_level"],
        "explanation": explanation,
    }

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

    try:
        response = (
            supabase.table("subscribers")
            .upsert(subscription_data, on_conflict="email")
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Send confirmation email (non-blocking failure)
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
        .eq("email", data.email)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Email not found")

    return {"message": "You have successfully unsubscribed"}