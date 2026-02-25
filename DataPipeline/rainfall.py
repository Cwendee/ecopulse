import glob
import re
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.mask import mask as rio_mask
import rioxarray
import xarray as xr


def list_geotiff_files(pattern: str) -> list[str]:
    return sorted(glob.glob(pattern))


def parse_date_from_name(path: str) -> datetime:
    name = Path(path).name
    m = re.search(r"(\d{4})\.(\d{2})\.(\d{2})", name)
    if not m:
        raise ValueError(f"Cannot parse date from filename {name}")
    year = int(m.group(1))
    month = int(m.group(2))
    day = int(m.group(3))
    return datetime(year, month, day)


def _mean_for_region(ds: rasterio.io.DatasetReader, geom) -> float:
    out_image, _ = rio_mask(ds, [geom.__geo_interface__], crop=False)
    data = out_image[0]

    if isinstance(data, np.ma.MaskedArray):
        values = data.compressed()
    else:
        values = data.ravel()

    if values.size == 0:
        return float("nan")

    return float(values.mean())


def aggregate_geotiff_period_mean(
    paths: list[str],
    adm2_gdf: gpd.GeoDataFrame,
    value_name: str
) -> pd.DataFrame:

    region_ids = adm2_gdf["region_id"].tolist()
    sums = {rid: 0.0 for rid in region_ids}
    counts = {rid: 0 for rid in region_ids}

    for path in paths:
        with rasterio.open(path) as ds:
            for _, row in adm2_gdf.iterrows():
                rid = row["region_id"]
                val = _mean_for_region(ds, row["geometry"])
                if not np.isnan(val):
                    sums[rid] += val
                    counts[rid] += 1

    records = []
    for rid in region_ids:
        c = counts[rid]
        mean_val = sums[rid] / c if c > 0 else float("nan")
        records.append({"region_id": rid, value_name: mean_val})

    return pd.DataFrame(records)


def aggregate_xarray_period_mean(
    da: xr.DataArray,
    adm2_gdf: gpd.GeoDataFrame,
    value_name: str
) -> pd.DataFrame:

    records = []

    # Ensure CRS is defined
    if not hasattr(da, "rio") or da.rio.crs is None:
        da = da.rio.write_crs("EPSG:4326", inplace=False)

    for _, row in adm2_gdf.iterrows():
        rid = row["region_id"]
        geom = [row["geometry"].__geo_interface__]

        try:
            clipped = da.rio.clip(geom, crs="EPSG:4326")
            values = clipped.values
            values = values[~np.isnan(values)]
            mean_val = float(values.mean()) if values.size > 0 else float("nan")
        except Exception:
            # Handles NoDataInBounds and any geometry mismatch
            mean_val = float("nan")

        records.append({
            "region_id": rid,
            value_name: mean_val
        })

    return pd.DataFrame(records)


def load_chirps_period(paths: list[str]) -> xr.DataArray:
    if not paths:
        raise ValueError("No CHIRPS files provided")

    dataarrays = []

    for path in paths:
        da = rioxarray.open_rasterio(path, masked=True).squeeze()
        date = parse_date_from_name(path)
        da = da.assign_coords(time=date)
        dataarrays.append(da)

    combined = xr.concat(dataarrays, dim="time")
    combined = combined.sortby("time")

    return combined