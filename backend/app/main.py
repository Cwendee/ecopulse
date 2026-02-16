from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Enable CORS (required for React + Vite frontend on Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP. Restrict later to your Vercel domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/subscribe")
def subscribe(email: str, location: str):
    data = {
        "email": email,
        "location": location
    }

    response = supabase.table("subscribers").insert(data).execute()

    return {
        "message": "Subscription successful",
        "data": response.data
    }


@app.get("/risk")
def get_risk(location: str):
    return {
        "location": location,
        "risk_level": "Moderate",
        "message": f"Flood risk in {location} is moderate."
    }
