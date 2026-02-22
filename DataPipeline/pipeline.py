from datetime import date, timedelta
from typing import Optional, Tuple

import pandas as pd

from DataPipeline.locations import load_adm2_boundaries
from DataPipeline.rainfall import (
    list_geotiff_files,
    parse_date_from_name,
    aggregate_xarray_period_mean,
    load_chirps_period,
)
from DataPipeline.risk import build_rainfall_features, classify_risk
from DataPipeline.chirps_stac_loader import load_chirps_daily_xarray


def _split_recent_normal(
    paths: list[str],
    recent_days: int,
    normal_days: int,
    valid_date: Optional[str],
) -> tuple[list[str], list[str], date]:

    dated = [(parse_date_from_name(p), p) for p in paths]
    dated.sort(key=lambda x: x[0])

    if not dated:
        raise ValueError("No rainfall files found")

    if valid_date is None:
        today = dated[-1][0].date()
    else:
        today = date.fromisoformat(valid_date)

    recent_start = today - timedelta(days=recent_days - 1)
    normal_start = recent_start - timedelta(days=normal_days)

    recent = [p for d, p in dated if recent_start <= d.date() <= today]
    normal = [p for d, p in dated if normal_start <= d.date() < recent_start]

    if not recent:
        raise ValueError("No recent rainfall files in requested window")

    if not normal:
        raise ValueError("No normal baseline rainfall files in requested window")

    return recent, normal, today


def run_daily_risk_pipeline(
    adm2_path: str,
    rainfall_glob: str,
    recent_days: int = 7,
    normal_days: int = 60,
    valid_date: Optional[str] = None,
    output_path: str = "DataPipeline/data/processed/risk_adm2.parquet",
) -> pd.DataFrame:

    # 🔁 Load ADM2 filtered to Africa
    adm2 = load_adm2_boundaries(adm2_path, region_scope="africa")

    # 🔁 Get rainfall file paths
    all_paths = list_geotiff_files(rainfall_glob)
    recent_paths, normal_paths, today = _split_recent_normal(
        all_paths, recent_days, normal_days, valid_date
    )

    # 🔁 Load full period as xarray
    da = load_chirps_period(recent_paths + normal_paths)
    da = da.sortby("time")

    recent_start = today - timedelta(days=recent_days - 1)
    normal_start = recent_start - timedelta(days=normal_days)

    recent_da = da.sel(time=slice(recent_start.isoformat(), today.isoformat()))
    normal_da = da.sel(
        time=slice(
            normal_start.isoformat(),
            (recent_start - timedelta(days=1)).isoformat(),
        )
    )

    recent_mean = recent_da.mean(dim="time", skipna=True)
    normal_mean = normal_da.mean(dim="time", skipna=True)

    # 🔁 Aggregate rainfall to ADM2
    recent_df = aggregate_xarray_period_mean(
        recent_mean, adm2, "rainfall_mean_recent"
    )
    normal_df = aggregate_xarray_period_mean(
        normal_mean, adm2, "rainfall_mean_normal"
    )

    # 🔁 Build features + classify risk
    feats = build_rainfall_features(recent_df, normal_df)
    result = classify_risk(feats, valid_at=today.isoformat())

    result.to_parquet(output_path, index=False)

    return result


def run_daily_risk_pipeline_stac(
    adm2_path: str,
    bbox: Tuple[float, float, float, float],
    recent_days: int = 7,
    normal_days: int = 60,
    valid_date: Optional[str] = None,
    output_path: str = "DataPipeline/data/processed/risk_adm2.parquet",
) -> pd.DataFrame:

    adm2 = load_adm2_boundaries(adm2_path, region_scope="africa")

    if valid_date is None:
        today = date.today()
    else:
        today = date.fromisoformat(valid_date)

    recent_start = today - timedelta(days=recent_days - 1)
    normal_start = recent_start - timedelta(days=normal_days)

    start_time = normal_start.isoformat()
    end_time = today.isoformat()

    da = load_chirps_daily_xarray(
        start_time=start_time,
        end_time=end_time,
        bbox=bbox,
        limit=500,
    )

    da = da.sortby("time")

    recent_da = da.sel(
        time=slice(recent_start.isoformat(), today.isoformat())
    )
    normal_da = da.sel(
        time=slice(
            normal_start.isoformat(),
            (recent_start - timedelta(days=1)).isoformat(),
        )
    )

    if recent_da.time.size == 0:
        raise ValueError("No recent CHIRPS data in requested window")

    if normal_da.time.size == 0:
        raise ValueError("No baseline CHIRPS data in requested window")

    recent_mean = recent_da.mean(dim="time", skipna=True)
    normal_mean = normal_da.mean(dim="time", skipna=True)

    recent_df = aggregate_xarray_period_mean(
        recent_mean, adm2, "rainfall_mean_recent"
    )
    normal_df = aggregate_xarray_period_mean(
        normal_mean, adm2, "rainfall_mean_normal"
    )

    feats = build_rainfall_features(recent_df, normal_df)
    result = classify_risk(feats, valid_at=today.isoformat())

    result.to_parquet(output_path, index=False)

    return result


if __name__ == "__main__":
    pass