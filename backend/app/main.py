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