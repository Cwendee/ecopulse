from fastapi import APIRouter, HTTPException
from app.models.schemas import RiskResponse
from app.services.supabase_client import supabase
from app.services.gpt_oss_client import generate

router = APIRouter()


@router.get("/risk", response_model=RiskResponse)
def get_risk_query(region_id: str):
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


@router.get("/risk/{region_id}")
def get_risk_path(region_id: str):
    response = (
        supabase.table("risk_adm2_daily")
        .select("*")
        .eq("region_id", region_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Region not found")

    return response.data[0]


@router.get("/risk/{region_id}/explain")
def explain_risk(region_id: str):
    response = (
        supabase.table("risk_adm2_daily")
        .select("*")
        .eq("region_id", region_id)
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=404, detail="Region not found")

    row = response.data[0]

    prompt = f"""
    You are an expert climate risk analyst.

    Region: {row.get('region_name')}
    Country: {row.get('country_code')}
    Risk level: {row.get('risk_level')}
    Rainfall anomaly: {row.get('anomaly')}

    Explain this clearly and give one recommendation.
    """

    try:
        explanation = generate(prompt)
    except Exception:
        explanation = "AI explanation unavailable."

    return {
        "region_id": region_id,
        "risk_level": row.get("risk_level"),
        "explanation": explanation,
    }