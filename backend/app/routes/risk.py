from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.services.gpt_oss_client import generate

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
# AI Risk Explanation
# ============================

def build_prompt(row):
    return f"""
You are an expert climate risk analyst.

Region ID: {row['region_id']}
Region Name: {row.get('region_name', 'Unknown')}
Country Code: {row.get('country_code', 'Unknown')}

Recent rainfall mean: {row.get('rainfall_mean_recent', 0)} mm
Baseline rainfall mean: {row.get('rainfall_mean_normal', 0)} mm
Rainfall anomaly: {row.get('anomaly', 0)} mm
Risk level: {row.get('risk_level', 'Unknown')}

Explain this risk clearly in simple language and give one practical recommendation
for communities or local authorities. Keep it under 120 words.
"""


@router.get("/risk/{region_id}/explain")
def explain_risk(region_id: str):

    row = risk_df[risk_df["region_id"] == region_id]

    if row.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    data = row.iloc[0]
    prompt = build_prompt(data)

    try:
        explanation = generate(prompt)
    except Exception:
        explanation = "Unable to generate AI explanation at the moment."

    return {
        "region_id": region_id,
        "risk_level": data.get("risk_level"),
        "explanation": explanation,
    }