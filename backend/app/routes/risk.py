from fastapi import APIRouter, HTTPException
from app.models.schemas import RiskResponse
from app.services.supabase_client import supabase  # adjust if your path differs

router = APIRouter()


@router.get("/risk", response_model=RiskResponse)
def get_risk(region_id: str):
    response = (
        supabase.table("risk_adm2_daily")
        .select("*")
        .eq("region_id", region_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Region not found")

    risk_data = response.data[0]

    if risk_data.get("data_quality") == "missing":
        raise HTTPException(
            status_code=503,
            detail="Risk data temporarily unavailable for this region"
        )

    return risk_data