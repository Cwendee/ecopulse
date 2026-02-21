import numpy as np
import pandas as pd
from typing import Tuple, Dict


def build_rainfall_features(recent_df: pd.DataFrame, normal_df: pd.DataFrame) -> pd.DataFrame:
    df = recent_df.merge(normal_df, on="region_id", suffixes=("_recent", "_normal"))
    df["data_missing"] = df["rainfall_mean_recent"].isna() | df["rainfall_mean_normal"].isna()
    df["rainfall_index"] = df["rainfall_mean_recent"] / (df["rainfall_mean_normal"] + 1e-6)
    df["rainfall_index"] = df["rainfall_index"].clip(0, 3)
    df["anomaly"] = df["rainfall_mean_recent"] - df["rainfall_mean_normal"]
    df.loc[df["data_missing"], ["rainfall_index", "anomaly"]] = np.nan
    df["rainfall_percentile"] = (df["rainfall_index"] / 3.0 * 100.0).clip(0, 100)
    return df


def classify_risk_row(rainfall_index: float, anomaly: float, data_missing: bool) -> Tuple[str, Dict[str, bool]]:
    if data_missing or np.isnan(rainfall_index) or np.isnan(anomaly):
        return "Unknown", {"rainfall_unusually_high": False, "anomaly_large": False}
    if rainfall_index < 1.2 and anomaly < 10:
        return "Low", {"rainfall_unusually_high": False, "anomaly_large": False}
    if rainfall_index < 1.6 and anomaly < 30:
        return "Moderate", {"rainfall_unusually_high": True, "anomaly_large": False}
    return "High", {"rainfall_unusually_high": True, "anomaly_large": True}


def classify_risk(df: pd.DataFrame, valid_at: str) -> pd.DataFrame:
    levels = []
    r1 = []
    r2 = []
    for _, row in df.iterrows():
        level, reason = classify_risk_row(
            float(row["rainfall_index"]) if not pd.isna(row["rainfall_index"]) else np.nan,
            float(row["anomaly"]) if not pd.isna(row["anomaly"]) else np.nan,
            bool(row.get("data_missing", False)),
        )
        levels.append(level)
        r1.append(reason["rainfall_unusually_high"])
        r2.append(reason["anomaly_large"])
    df["risk_level"] = levels
    df["valid_at"] = valid_at
    df["rainfall_unusually_high"] = r1
    df["anomaly_large"] = r2
    df["data_quality"] = np.where(df["data_missing"], "missing", "ok")
    return df
