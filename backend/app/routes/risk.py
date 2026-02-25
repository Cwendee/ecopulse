from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

router = APIRouter()

# ============================
# Load Risk Dataset (Parquet)
# ============================

BASE_DIR = Path(__file__).resolve().parents[3]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

if not RISK_FILE.exists():
    raise RuntimeError("Risk dataset not found. Ensure parquet file is generated.")

risk_df = pd.read_parquet(RISK_FILE)

# ============================
# Structured SME Messaging
# ============================

def build_structured_message(risk_level: str):

    risk = (risk_level or "").lower()

    if risk == "low":
        return {
            "indicator": "🟢",
            "title": "Low Risk",
            "line1": "Rainfall is within normal range.",
            "line2": "No immediate flood threat.",
            "recommendation": "Continue normal activities and monitor updates."
        }

    elif risk == "moderate":
        return {
            "indicator": "🟡",
            "title": "Moderate Risk",
            "line1": "Rainfall levels are above normal.",
            "line2": "Localized flooding may occur.",
            "recommendation": "Prepare drainage and monitor closely."
        }

    elif risk == "high":
        return {
            "indicator": "🔴",
            "title": "High Risk",
            "line1": "Rainfall significantly exceeds normal levels.",
            "line2": "Flooding is likely.",
            "recommendation": "Take precautionary measures immediately."
        }

    else:
        return {
            "indicator": "⚪",
            "title": "Risk Status Unavailable",
            "line1": "Risk data is currently unavailable.",
            "line2": "",
            "recommendation": "Please check again later."
        }

# ============================
# Get Risk by Region ID
# ============================

@router.get("/risk/{region_id}")
def get_risk(region_id: str):

    row = risk_df[risk_df["region_id"] == region_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    data = row.iloc[0]

    return {
        "region_id": data["region_id"],
        "region_name": data.get("region_name"),
        "country_code": data.get("country_code"),
        "risk_level": data.get("risk_level"),
        "rainfall_mean_recent": data.get("rainfall_mean_recent"),
        "rainfall_mean_normal": data.get("rainfall_mean_normal"),
        "anomaly": data.get("anomaly"),
        "valid_at": data.get("valid_at"),
        "rainfall_percentile": data.get("rainfall_percentile"),
        "data_quality": data.get("data_quality"),
    }

# ============================
# Explain Risk (Structured SME Format)
# ============================

@router.get("/risk/{region_id}/explain")
def explain_risk(region_id: str):

    row = risk_df[risk_df["region_id"] == region_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    data = row.iloc[0]
    structured = build_structured_message(data.get("risk_level"))

    return {
        "region_id": data["region_id"],
        "region_name": data.get("region_name"),
        "country_code": data.get("country_code"),
        "risk_level": data.get("risk_level"),
        **structured
    }