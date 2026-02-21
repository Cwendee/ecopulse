import json
from typing import List, Tuple
from urllib.request import urlopen

import numpy as np
import rioxarray
import xarray as xr


def search_chirps_daily(start_time: str, end_time: str, bbox: Tuple[float, float, float, float], limit: int = 50) -> List[dict]:
    root_url = "https://explorer.digitalearth.africa/stac"
    bbox_str = f"[{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}]"
    url = f"{root_url}/search?collection=rainfall_chirps_daily&time={start_time}/{end_time}&bbox={bbox_str}&limit={limit}"
    with urlopen(url) as f:
        data = json.loads(f.read().decode())
    return data.get("features", [])


def load_chirps_daily_xarray(start_time: str, end_time: str, bbox: Tuple[float, float, float, float], limit: int = 50) -> xr.DataArray:
    items = search_chirps_daily(start_time, end_time, bbox, limit=limit)
    arrays: List[xr.DataArray] = []
    for feat in items:
        assets = feat.get("assets", {})
        asset = assets.get("rainfall") or next(iter(assets.values()))
        href = asset["href"]
        da = rioxarray.open_rasterio(href, masked=True)
        da = da.squeeze("band", drop=True)
        t = feat["properties"]["datetime"]
        da = da.assign_coords(time=np.datetime64(t))
        arrays.append(da)
    if not arrays:
        raise ValueError("No CHIRPS items found for given query")
    out = xr.concat(arrays, dim="time")
    out.name = "rainfall"
    return out
