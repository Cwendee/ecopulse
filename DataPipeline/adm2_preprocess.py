import pandas as pd
from pathlib import Path
from typing import List, Optional

import geopandas as gpd


AFRICA_ISO3: List[str] = [
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV", "CAF", "TCD",
    "COM", "COG", "COD", "CIV", "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH",
    "GAB", "GMB", "GHA", "GIN", "GNB", "KEN", "LSO", "LBR", "LBY", "MDG",
    "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA",
    "STP", "SEN", "SYC", "SLE", "ZAF", "SSD", "SDN", "TZA", "TGO", "TUN",
    "UGA", "ZMB", "ZWE", "SOM",
]


def filter_global_adm2_to_africa(
    global_path: str, 
    output_path: str, 
    iso3_source_path: Optional[str] = None
) -> None:
    """
    Filters global ADM2 boundaries to African countries.
    If iso3_source_path is provided (Excel/CSV), it extracts unique ISO3 codes from it.
    Otherwise, it uses the hardcoded AFRICA_ISO3 list.
    """
    src = Path(global_path)
    dst = Path(output_path)
    
    # 1. Determine ISO3 codes to keep
    iso_list = AFRICA_ISO3
    if iso3_source_path:
        p = Path(iso3_source_path)
        if p.exists():
            if p.suffix == ".csv":
                df = pd.read_csv(p)
            else:
                df = pd.read_excel(p)
            
            # Use 'ISO3' column as seen in the screenshot
            if "ISO3" in df.columns:
                iso_list = df["ISO3"].dropna().unique().tolist()
                print(f"Using {len(iso_list)} ISO3 codes from {p.name}")

    # 2. Load and filter GeoJSON
    gdf = gpd.read_file(src)

    if "shapeGroup" not in gdf.columns:
        raise ValueError("Expected 'shapeGroup' column with ISO3 codes")

    mask = gdf["shapeGroup"].astype(str).isin(iso_list)
    subset = gdf.loc[mask].copy()

    dst.parent.mkdir(parents=True, exist_ok=True)
    subset.to_file(dst, driver="GeoJSON")
    print(f"✅ Filtered ADM2 saved to {dst}")
