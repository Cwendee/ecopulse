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
# SME Structured Messaging
# ============================

def build_structured_message(risk_level: str):

    risk = (risk_level or "").lower()

    if risk == "low":
        indicator = "🟢"
        title = "Low Risk"
        explanation = (
            "Rainfall is within normal range. "
            "Flooding is unlikely at this time. "
            "Continue normal activities and monitor updates."
        )

    elif risk == "moderate":
        indicator = "🟡"
        title = "Moderate Risk"
        explanation = (
            "Rainfall levels are above normal. "
            "Localized flooding may occur in low-lying areas. "
            "Prepare drainage systems and monitor closely."
        )

    elif risk == "high":
        indicator = "🔴"
        title = "High Risk"
        explanation = (
            "Rainfall significantly exceeds normal levels. "
            "Flooding is likely in vulnerable areas. "
            "Take precautionary measures immediately."
        )

    else:
        indicator = "⚪"
        title = "Risk Unavailable"
        explanation = (
            "Risk data is currently unavailable. "
            "Please check again later."
        )

    return {
        "indicator": indicator,
        "title": title,
        "explanation": explanation
    }

# ======================================================
# IMPORTANT: STATIC ROUTES MUST COME BEFORE DYNAMIC ONES
# ======================================================

# ============================
# Get All High Risk Regions
# ============================

@router.get("/risk/high")
def get_high_risk_regions():

    high_risk_df = risk_df[risk_df["risk_level"].str.lower() == "high"]

    if high_risk_df.empty:
        return {
            "count": 0,
            "regions": []
        }

    regions = high_risk_df[[
        "region_id",
        "region_name",
        "country_code",
        "risk_level",
        "valid_at"
    ]].to_dict(orient="records")

    return {
        "count": len(regions),
        "regions": regions
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
        "rainfall_percentile": data.get("rainfall_percentile"),
        "valid_at": data.get("valid_at"),
        "data_quality": data.get("data_quality"),
    }

# ============================
# Explain Risk (SME Friendly)
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
        "valid_at": data.get("valid_at"),
        **structured
    }