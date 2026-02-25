from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

from app.models.schemas import (
    LocationResolveRequest,
    LocationResolveResponse
)

router = APIRouter()

# ============================
# Load Risk Dataset
# ============================

BASE_DIR = Path(__file__).resolve().parents[3]
RISK_FILE = BASE_DIR / "DataPipeline" / "data" / "processed" / "risk_africa.parquet"

if not RISK_FILE.exists():
    raise RuntimeError("Risk dataset not found. Ensure parquet file is generated.")

risk_df = pd.read_parquet(RISK_FILE)

# ============================
# Full ISO-3 Country Mapping
# ============================

COUNTRY_MAP = {
    "AGO": "Angola",
    "BDI": "Burundi",
    "BEN": "Benin",
    "BFA": "Burkina Faso",
    "BWA": "Botswana",
    "CAF": "Central African Republic",
    "CIV": "Côte d'Ivoire",
    "CMR": "Cameroon",
    "COD": "Democratic Republic of the Congo",
    "COG": "Republic of the Congo",
    "COM": "Comoros",
    "CPV": "Cape Verde",
    "DJI": "Djibouti",
    "DZA": "Algeria",
    "EGY": "Egypt",
    "ERI": "Eritrea",
    "ETH": "Ethiopia",
    "GAB": "Gabon",
    "GHA": "Ghana",
    "GIN": "Guinea",
    "GMB": "Gambia",
    "GNB": "Guinea-Bissau",
    "GNQ": "Equatorial Guinea",
    "KEN": "Kenya",
    "LBR": "Liberia",
    "LBY": "Libya",
    "LSO": "Lesotho",
    "MAR": "Morocco",
    "MDG": "Madagascar",
    "MLI": "Mali",
    "MOZ": "Mozambique",
    "MRT": "Mauritania",
    "MUS": "Mauritius",
    "MWI": "Malawi",
    "NAM": "Namibia",
    "NER": "Niger",
    "NGA": "Nigeria",
    "RWA": "Rwanda",
    "SDN": "Sudan",
    "SEN": "Senegal",
    "SLE": "Sierra Leone",
    "SOM": "Somalia",
    "SSD": "South Sudan",
    "SWZ": "Eswatini",
    "TCD": "Chad",
    "TGO": "Togo",
    "TUN": "Tunisia",
    "TZA": "Tanzania",
    "UGA": "Uganda",
    "ZAF": "South Africa",
    "ZMB": "Zambia",
    "ZWE": "Zimbabwe"
}

# ============================
# Location Resolve
# ============================

@router.post("/location/resolve", response_model=LocationResolveResponse)
def resolve_location(data: LocationResolveRequest):
    return {
        "region_id": "NG-LA-IKJ",
        "region_name": "Ikeja",
        "country": "Nigeria"
    }

# ============================
# Countries Endpoint
# ============================

@router.get("/countries")
def get_countries():
    codes = risk_df["country_code"].dropna().unique().tolist()
    codes.sort()

    return {
        "countries": [
            {
                "code": code,
                "name": COUNTRY_MAP.get(code, code)
            }
            for code in codes
        ]
    }

# ============================
# Regions by Country
# ============================

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