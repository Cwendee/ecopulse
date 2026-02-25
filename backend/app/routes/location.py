from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.models.schemas import (
    LocationResolveRequest,
    LocationResolveResponse
)

router = APIRouter()

# Load dataset
BASE_DIR = Path(__file__).resolve().parents[3]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"
risk_df = pd.read_parquet(RISK_FILE)

COUNTRY_MAP = {
    "NGA": "Nigeria",
    "GHA": "Ghana",
    "KEN": "Kenya",
    "ZAF": "South Africa",
    # Expand later if needed
}


@router.post("/location/resolve", response_model=LocationResolveResponse)
def resolve_location(data: LocationResolveRequest):
    return {
        "region_id": "NG-LA-IKJ",
        "region_name": "Ikeja",
        "country": "Nigeria"
    }


@router.get("/countries")
def get_countries():
    codes = risk_df["country_code"].dropna().unique().tolist()
    codes.sort()

    return {
        "countries": [
            {"code": code, "name": COUNTRY_MAP.get(code, code)}
            for code in codes
        ]
    }


@router.get("/countries/{country_code}/regions")
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