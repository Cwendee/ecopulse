from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
import os
import resend

from app.routes import location, risk, chat
from app.services.supabase_client import supabase

load_dotenv()

app = FastAPI()

# Register Routers
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

# ============================
# Health
# ============================

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ============================
# Email Confirmation
# ============================

def send_confirmation_email(to_email: str):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
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
    except Exception:
        pass

# ============================
# Subscription Models
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
# Subscribe
# ============================

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
            raise HTTPException(
                status_code=409,
                detail="Email already subscribed"
            )
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    if data.email_delivery:
        send_confirmation_email(data.email)

    return {
        "message": "Subscription saved successfully",
        "data": response.data,
    }

# ============================
# Unsubscribe
# ============================

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