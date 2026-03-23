import geopandas as gpd
from typing import Optional


AFRICAN_ISO3 = [
    "DZA","AGO","BEN","BWA","BFA","BDI","CMR","CPV","CAF","TCD",
    "COM","COD","COG","CIV","DJI","EGY","GNQ","ERI","SWZ","ETH",
    "GAB","GMB","GHA","GIN","GNB","KEN","LSO","LBR","LBY","MDG",
    "MWI","MLI","MRT","MUS","MAR","MOZ","NAM","NER","NGA","RWA",
    "STP","SEN","SYC","SLE","SOM","ZAF","SSD","SDN","TZA","TGO",
    "TUN","UGA","ZMB","ZWE"
]


def load_adm2_boundaries(
    path: str,
    region_scope: Optional[str] = None
) -> gpd.GeoDataFrame:
    """
    Load ADM2 boundaries and optionally filter by region scope.

    region_scope:
        None        -> load all regions
        "africa"    -> filter to African countries (ISO3 via shapeGroup)
    """

    gdf = gpd.read_file(path)
    gdf = gdf.to_crs(epsg=4326)

    cols = gdf.columns
    out = gdf.copy()

    # --- Normalize region_id ---
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
        name0_col = next((c for c in cols if c in ["NAME_0", "COUNTRY", "ADM0_NAME"]), None)
        name1_col = next((c for c in cols if c in ["NAME_1", "ADM1_NAME"]), None)
        name2_col = next((c for c in cols if c in ["NAME_2", "ADM2_NAME"]), None)

        if name0_col is None:
            raise ValueError("Cannot determine country column for region_id construction")

        name0 = out[name0_col].astype(str).str.strip()
        name1 = out[name1_col].astype(str).str.strip() if name1_col else ""
        name2 = out[name2_col].astype(str).str.strip() if name2_col else ""

        out["region_id"] = (name0 + "|" + name1 + "|" + name2).str.lower()

    # --- Optional Africa filtering ---
    if region_scope == "africa" and "shapeGroup" in out.columns:
        out = out[out["shapeGroup"].isin(AFRICAN_ISO3)]

    # --- Keep only relevant columns ---
    keep = ["region_id"]

    for k in [
        "NAME_0", "NAME_1", "NAME_2",
        "COUNTRY", "ADM0_NAME", "ADM1_NAME", "ADM2_NAME",
        "shapeGroup"
    ]:
        if k in out.columns:
            keep.append(k)

    keep.append("geometry")

    return out[keep]


def normalize_location(country: str, adm2_name: str, adm2_gdf: gpd.GeoDataFrame) -> str:
    cn = country.strip().lower()
    rn = adm2_name.strip().lower()

    name0_col = next(c for c in adm2_gdf.columns if c in ["NAME_0", "COUNTRY", "ADM0_NAME"])
    name2_col = next(c for c in adm2_gdf.columns if c in ["NAME_2", "ADM2_NAME"])

    match = adm2_gdf[
        (adm2_gdf[name0_col].astype(str).str.lower() == cn) &
        (adm2_gdf[name2_col].astype(str).str.lower() == rn)
    ]

    if len(match) == 0:
        raise ValueError("Region not found")

    return str(match.iloc[0]["region_id"])


def get_region_polygon(region_id: str, adm2_gdf: gpd.GeoDataFrame):
    row = adm2_gdf[adm2_gdf["region_id"] == region_id]

    if len(row) == 0:
        raise ValueError("Region not found")

    return row.iloc[0]["geometry"]