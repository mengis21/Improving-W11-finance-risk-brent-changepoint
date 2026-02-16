from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DatasetPaths:
    root: Path

    @property
    def raw_prices_csv(self) -> Path:
        return self.root / "data" / "raw" / "brent_oil_prices.csv"

    @property
    def raw_events_csv(self) -> Path:
        return self.root / "data" / "raw" / "oil_market_events.csv"


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_brent_prices(path: str | Path | None = None) -> pd.DataFrame:
    paths = DatasetPaths(root=project_root())
    csv_path = Path(path) if path is not None else paths.raw_prices_csv

    df = pd.read_csv(csv_path)
    # Expected columns: Date, Price
    # Primary format in the provided dataset: e.g. 20-May-87
    parsed = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    # Fallback for any non-conforming rows (keeps behavior robust if format changes)
    if parsed.isna().any():
        parsed_fallback = pd.to_datetime(df.loc[parsed.isna(), "Date"], errors="coerce", dayfirst=True)
        parsed.loc[parsed.isna()] = parsed_fallback
    df["Date"] = parsed
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"]).reset_index(drop=True)
    return df


def load_events(path: str | Path | None = None) -> pd.DataFrame:
    paths = DatasetPaths(root=project_root())
    csv_path = Path(path) if path is not None else paths.raw_events_csv

    df = pd.read_csv(csv_path)
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["event_date"]).sort_values("event_date").reset_index(drop=True)
    return df


def compute_log_returns(prices: pd.Series) -> pd.Series:
    prices = prices.astype(float)
    return (np.log(prices) - np.log(prices.shift(1))).dropna()
