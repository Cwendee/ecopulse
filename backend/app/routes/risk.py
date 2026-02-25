from fastapi import APIRouter, HTTPException, Query
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
# Utility
# ============================

def normalize(text: str):
    return text.strip().lower()

# Country name → ISO3 mapping
COUNTRY_MAP = {
    "algeria": "DZA",
    "angola": "AGO",
    "benin": "BEN",
    "burkina faso": "BFA",
    "burundi": "BDI",
    "botswana": "BWA",
    "cameroon": "CMR",
    "cape verde": "CPV",
    "comoros": "COM",
    "congo": "COG",
    "democratic republic of the congo": "COD",
    "ghana": "GHA",
    "kenya": "KEN",
    "nigeria": "NGA",
    # Add more as needed
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
# Get Risk by Country + Region Name (SME-Friendly)
# ============================

@router.get("/risk/by-name")
def get_risk_by_name(
    country: str = Query(...),
    region: str = Query(...)
):

    country_key = normalize(country)

    if country_key not in COUNTRY_MAP:
        raise HTTPException(status_code=404, detail="Country not supported")

    country_code = COUNTRY_MAP[country_key]

    filtered = risk_df[
        (risk_df["country_code"] == country_code) &
        (risk_df["region_name"].str.lower().str.contains(normalize(region), na=False))
    ]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    # If multiple matches, take the first (safe for now)
    data = filtered.iloc[0]

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
# AI Explanation (by Region ID)
# ============================

def build_prompt(row):
    return f"""
You are an expert climate risk analyst.

Region: {row.get('region_name')}
Country Code: {row.get('country_code')}

Recent rainfall mean: {row.get('rainfall_mean_recent')} mm
Baseline rainfall mean: {row.get('rainfall_mean_normal')} mm
Rainfall anomaly: {row.get('anomaly')} mm
Risk level: {row.get('risk_level')}

Explain this risk clearly in simple language and give one practical recommendation.
Keep it under 120 words.
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

# ============================
# AI Explanation (by Name)
# ============================

@router.get("/risk/by-name/explain")
def explain_risk_by_name(
    country: str = Query(...),
    region: str = Query(...)
):

    country_key = normalize(country)

    if country_key not in COUNTRY_MAP:
        raise HTTPException(status_code=404, detail="Country not supported")

    country_code = COUNTRY_MAP[country_key]

    filtered = risk_df[
        (risk_df["country_code"] == country_code) &
        (risk_df["region_name"].str.lower().str.contains(normalize(region), na=False))
    ]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="Region not found")

    data = filtered.iloc[0]
    prompt = build_prompt(data)

    try:
        explanation = generate(prompt)
    except Exception:
        explanation = "Unable to generate AI explanation at the moment."

    return {
        "region_name": data.get("region_name"),
        "country_code": data.get("country_code"),
        "risk_level": data.get("risk_level"),
        "explanation": explanation,
    }