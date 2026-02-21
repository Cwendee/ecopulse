import json
from typing import Optional, Tuple, List

import geopandas as gpd

from locations import load_adm2_boundaries
from gpt_oss_client import generate


def _country_column(gdf: gpd.GeoDataFrame) -> str:
    for c in ["NAME_0", "COUNTRY", "ADM0_NAME"]:
        if c in gdf.columns:
            return c
    raise ValueError("No country column found in ADM2 data")


def _adm_names(gdf: gpd.GeoDataFrame) -> Tuple[Optional[str], Optional[str]]:
    adm1 = None
    adm2 = None
    for c in ["NAME_1", "ADM1_NAME"]:
        if c in gdf.columns:
            adm1 = c
            break
    for c in ["NAME_2", "ADM2_NAME"]:
        if c in gdf.columns:
            adm2 = c
            break
    return adm1, adm2


def build_candidate_list_for_country(adm2_path: str, country: str) -> gpd.GeoDataFrame:
    gdf = load_adm2_boundaries(adm2_path)
    col_country = _country_column(gdf)
    mask = gdf[col_country].astype(str).str.lower() == country.strip().lower()
    subset = gdf.loc[mask].copy()
    if subset.empty:
        raise ValueError("No ADM2 regions found for country")
    return subset


def _prompt_for_resolution(country: str, user_location: str, candidates: gpd.GeoDataFrame) -> str:
    adm1_col, adm2_col = _adm_names(candidates)
    lines: List[str] = []
    for _, row in candidates.iterrows():
        rid = str(row["region_id"])
        adm1 = str(row[adm1_col]) if adm1_col else ""
        adm2 = str(row[adm2_col]) if adm2_col else ""
        lines.append(f"{rid}\t{adm1}\t{adm2}")
    regions_block = "\n".join(lines)
    prompt = (
        "You map messy user location descriptions to administrative level 2 regions.\n"
        f"Country: {country}\n"
        "You receive a user location description and a list of ADM2 regions for this country.\n"
        "Each line has region_id, ADM1 name and ADM2 name separated by tabs.\n"
        "Pick the single best matching region_id for the user location.\n"
        "If none is a reasonable match, pick the closest one.\n"
        "Respond only with a JSON object like {\"region_id\": \"...\"}.\n\n"
        f"User location: {user_location}\n\n"
        "ADM2 regions:\n"
        f"{regions_block}\n\n"
        "Answer:"
    )
    return prompt


def resolve_location_to_region_id(adm2_path: str, country: str, user_location: str) -> str:
    candidates = build_candidate_list_for_country(adm2_path, country)
    prompt = _prompt_for_resolution(country, user_location, candidates)
    raw = generate(prompt)
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not parse JSON from model output")
    obj = json.loads(raw[start : end + 1])
    region_id = str(obj.get("region_id", "")).strip()
    if region_id == "":
        raise ValueError("region_id missing in model output")
    if region_id not in set(candidates["region_id"].astype(str).tolist()):
        raise ValueError("region_id not found in ADM2 candidates")
    return region_id
