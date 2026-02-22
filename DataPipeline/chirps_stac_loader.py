import json
from typing import List, Tuple

import numpy as np
import rioxarray
import xarray as xr
import requests


def search_chirps_daily(
    start_time: str,
    end_time: str,
    bbox: Tuple[float, float, float, float],
    limit: int = 50,
) -> List[dict]:
    """
    Perform a POST-based STAC search against Digital Earth Africa
    for CHIRPS daily rainfall items.
    """

    url = "https://explorer.digitalearth.africa/stac/search"

    payload = {
        "collections": ["rainfall_chirps_daily"],
        "bbox": list(bbox),
        "datetime": f"{start_time}/{end_time}",
        "limit": limit,
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"STAC search failed: {response.status_code} {response.text}"
        )

    data = response.json()
    return data.get("features", [])


def load_chirps_daily_xarray(
    start_time: str,
    end_time: str,
    bbox: Tuple[float, float, float, float],
    limit: int = 50
) -> xr.DataArray:
    """
    Load CHIRPS daily rainfall rasters into an xarray DataArray
    with a time dimension.
    """

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