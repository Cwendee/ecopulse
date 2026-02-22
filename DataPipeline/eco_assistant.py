import json
from pathlib import Path
from typing import Optional, List

import pandas as pd

from api_models import EcoChatRequest, EcoChatResponse, RiskRecord, UserProfile
from gpt_oss_client import generate
from locations import load_adm2_boundaries


def _find_latest_risk_file(processed_dir: str = "data/processed") -> Optional[Path]:
    base = Path(processed_dir)
    if not base.exists():
        return None
    candidates: List[Path] = sorted(base.glob("risk_adm2_*.parquet"))
    if candidates:
        return candidates[-1]
    default = base / "risk_adm2.parquet"
    if default.exists():
        return default
    return None


def load_risk_table(path: Optional[str] = None) -> pd.DataFrame:
    if path is None:
        f = _find_latest_risk_file()
        if f is None:
            raise FileNotFoundError("No risk_adm2 parquet file found in data/processed")
        path = str(f)
    return pd.read_parquet(path)


def get_risk_record_for_region(region_id: str, adm2_path: str, risk_path: Optional[str] = None) -> RiskRecord:
    risk_df = load_risk_table(risk_path)
    row_risk = risk_df[risk_df["region_id"].astype(str) == str(region_id)]
    if row_risk.empty:
        raise ValueError("Region not found in risk table")
    row_risk = row_risk.iloc[0]
    adm2 = load_adm2_boundaries(adm2_path)
    row_loc = adm2[adm2["region_id"].astype(str) == str(region_id)]
    country = None
    adm1 = None
    adm2_name = None
    if not row_loc.empty:
        r = row_loc.iloc[0]
        country = str(r.get("NAME_0") or r.get("shapeGroup") or "")
        adm1 = str(r.get("NAME_1") or "")
        adm2_name = str(r.get("NAME_2") or r.get("shapeName") or "")
    return RiskRecord(
        region_id=str(region_id),
        country=country or None,
        adm1_name=adm1 or None,
        adm2_name=adm2_name or None,
        risk_level=str(row_risk["risk_level"]),
        valid_at=str(row_risk["valid_at"]),
        rainfall_index=float(row_risk["rainfall_index"]) if pd.notna(row_risk["rainfall_index"]) else None,
        rainfall_percentile=float(row_risk["rainfall_percentile"]) if pd.notna(row_risk["rainfall_percentile"]) else None,
        anomaly_mm=float(row_risk["anomaly"]) if pd.notna(row_risk["anomaly"]) else None,
        data_quality=str(row_risk.get("data_quality", "ok")),
    )


def build_eco_prompt(req: EcoChatRequest) -> str:
    obj = {
        "location": {
            "region_id": req.location.region_id,
            "country": req.location.country,
            "adm1_name": req.location.adm1_name,
            "adm2_name": req.location.adm2_name,
        },
        "risk": {
            "risk_level": req.location.risk_level,
            "valid_at": req.location.valid_at,
            "rainfall_index": req.location.rainfall_index,
            "rainfall_percentile": req.location.rainfall_percentile,
            "anomaly_mm": req.location.anomaly_mm,
            "data_quality": req.location.data_quality,
        },
        "user_profile": {
            "audience": req.user_profile.audience,
            "language": req.user_profile.language,
        },
        "user_question": req.user_question,
    }
    payload = json.dumps(obj, ensure_ascii=False)
    prompt = (
        "You are Eco, a calm and practical flood preparedness assistant for African communities.\n"
        "You receive structured JSON with flood risk metrics and user context.\n"
        "Explain the current flood risk clearly and give concrete, local, actionable preparedness steps.\n"
        "Never guess the numeric risk; always respect the risk_level and data_quality fields.\n"
        "If risk_level is 'Unknown' or data_quality is 'missing', be honest about the uncertainty but still give general safety advice.\n"
        "Use simple language suitable for the specified audience. Answer in the specified language.\n\n"
        f"Input JSON:\n{payload}\n\n"
        "Now write a short answer for the user."
    )
    return prompt


def generate_eco_answer(req: EcoChatRequest) -> EcoChatResponse:
    prompt = build_eco_prompt(req)
    answer = generate(prompt)
    return EcoChatResponse(answer=answer)
