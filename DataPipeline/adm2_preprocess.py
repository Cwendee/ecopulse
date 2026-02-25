from pathlib import Path
from typing import  List

import geopandas as gpd


AFRICA_ISO3: List[str] = [
    "DZA",
    "AGO",
    "BEN",
    "BWA",
    "BFA",
    "BDI",
    "CMR",
    "CPV",
    "CAF",
    "TCD",
    "COM",
    "COG",
    "COD",
    "CIV",
    "DJI",
    "EGY",
    "GNQ",
    "ERI",
    "SWZ",
    "ETH",
    "GAB",
    "GMB",
    "GHA",
    "GIN",
    "GNB",
    "KEN",
    "LSO",
    "LBR",
    "LBY",
    "MDG",
    "MWI",
    "MLI",
    "MRT",
    "MUS",
    "MAR",
    "MOZ",
    "NAM",
    "NER",
    "NGA",
    "RWA",
    "STP",
    "SEN",
    "SYC",
    "SLE",
    "ZAF",
    "SSD",
    "SDN",
    "TZA",
    "TGO",
    "TUN",
    "UGA",
    "ZMB",
    "ZWE",
    "SOM",
]


def filter_global_adm2_to_africa(global_path: str, output_path: str) -> None:
    src = Path(global_path)
    dst = Path(output_path)

    gdf = gpd.read_file(src)

    if "shapeGroup" not in gdf.columns:
        raise ValueError("Expected 'shapeGroup' column with ISO3 codes")

    mask = gdf["shapeGroup"].astype(str).isin(AFRICA_ISO3)
    subset = gdf.loc[mask].copy()

    dst.parent.mkdir(parents=True, exist_ok=True)
    subset.to_file(dst, driver="GeoJSON")


