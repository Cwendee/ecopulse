import geopandas as gpd
import pandas as pd
from typing import Optional


def load_adm2_boundaries(path: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(path)
    gdf = gdf.to_crs(epsg=4326)
    cols = gdf.columns
    out = gdf.copy()
    if "region_id" in cols:
        out["region_id"] = out["region_id"].astype(str)
    elif "shapeID" in cols:
        out["region_id"] = out["shapeID"].astype(str)
        if "shapeGroup" in cols and "NAME_0" not in cols:
            out["NAME_0"] = out["shapeGroup"]
        if "shapeName" in cols and "NAME_2" not in cols:
            out["NAME_2"] = out["shapeName"]
    elif "GID_2" in cols:
        out["region_id"] = out["GID_2"].astype(str)
    else:
        name0 = out[cols.intersection(["NAME_0", "COUNTRY", "ADM0_NAME"]).tolist()[0]].astype(str)
        name1 = out[cols.intersection(["NAME_1", "ADM1_NAME"]).tolist()[0]].astype(str) if len(
            cols.intersection(["NAME_1", "ADM1_NAME"])) else ""
        name2 = out[cols.intersection(["NAME_2", "ADM2_NAME"]).tolist()[0]].astype(str) if len(
            cols.intersection(["NAME_2", "ADM2_NAME"])) else ""
        out["region_id"] = (name0.str.strip() + "|" + name1.str.strip() + "|" + name2.str.strip()).str.lower()
    keep = ["region_id"]
    for k in ["NAME_0", "NAME_1", "NAME_2", "COUNTRY", "ADM0_NAME", "ADM1_NAME", "ADM2_NAME", "shapeGroup"]:
        if k in out.columns:
            keep.append(k)
    keep.append("geometry")
    return out[keep]


def normalize_location(country: str, adm2_name: str, adm2_gdf: gpd.GeoDataFrame) -> str:
    cn = country.strip().lower()
    rn = adm2_name.strip().lower()
    name0_col = [c for c in adm2_gdf.columns if c in ["NAME_0", "COUNTRY", "ADM0_NAME"]][0]
    name2_col = [c for c in adm2_gdf.columns if c in ["NAME_2", "ADM2_NAME"]][0]
    match = adm2_gdf[
        (adm2_gdf[name0_col].astype(str).str.lower() == cn)
        & (adm2_gdf[name2_col].astype(str).str.lower() == rn)
    ]
    if len(match) == 0:
        raise ValueError("Region not found")
    return str(match.iloc[0]["region_id"])


def get_region_polygon(region_id: str, adm2_gdf: gpd.GeoDataFrame):
    row = adm2_gdf[adm2_gdf["region_id"] == region_id]
    if len(row) == 0:
        raise ValueError("Region not found")
    return row.iloc[0]["geometry"]
