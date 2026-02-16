from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# Use a non-interactive backend (safe for headless runs)
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    fig_dir = root / "reports" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    out_dir = root / "data" / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)

    sns.set_style("whitegrid")

    df = pd.read_csv(root / "data" / "raw" / "brent_oil_prices.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Date", "Price"]).sort_values("Date").reset_index(drop=True)

    cutoff = df["Date"].max() - pd.DateOffset(years=10)
    df_10y = df.loc[df["Date"] >= cutoff].reset_index(drop=True)

    returns = np.log(df_10y["Price"]).diff().dropna()
    returns_df = pd.DataFrame(
        {
            "Date": df_10y["Date"].iloc[1:].reset_index(drop=True),
            "log_return": returns.reset_index(drop=True),
        }
    )

    # Full series price
    plt.figure(figsize=(12, 4))
    plt.plot(df["Date"], df["Price"], linewidth=1)
    plt.title("Brent Oil Price (USD/barrel) - Full series")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    plt.savefig(fig_dir / "price_series_full.png", dpi=160)
    plt.close()

    # Last decade price
    plt.figure(figsize=(12, 4))
    plt.plot(df_10y["Date"], df_10y["Price"], linewidth=1)
    plt.title("Brent Oil Price (USD/barrel) - Last 10 years")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    plt.savefig(fig_dir / "price_series_last_decade.png", dpi=160)
    plt.close()

    # Log returns last decade
    plt.figure(figsize=(12, 4))
    plt.plot(returns_df["Date"], returns_df["log_return"], linewidth=0.8)
    plt.title("Log returns - Last 10 years")
    plt.xlabel("Date")
    plt.ylabel("log return")
    plt.tight_layout()
    plt.savefig(fig_dir / "log_returns_last_decade.png", dpi=160)
    plt.close()

    # Rolling volatility
    window = 30
    returns_df["roll_vol_30d"] = returns_df["log_return"].rolling(window).std() * np.sqrt(252)
    plt.figure(figsize=(12, 4))
    plt.plot(returns_df["Date"], returns_df["roll_vol_30d"], linewidth=1)
    plt.title("Rolling volatility (30-day std of log returns, annualized) - Last 10 years")
    plt.xlabel("Date")
    plt.ylabel("Annualized volatility")
    plt.tight_layout()
    plt.savefig(fig_dir / "rolling_volatility_30d_last_decade.png", dpi=160)
    plt.close()

    def adf_row(series: pd.Series, name: str) -> dict:
        series = pd.Series(series).dropna().astype(float)
        stat, pvalue, _, _, crit, _ = adfuller(series, autolag="AIC")
        return {
            "series": name,
            "adf_stat": float(stat),
            "p_value": float(pvalue),
            "n": int(len(series)),
            "crit_1%": float(crit.get("1%")),
            "crit_5%": float(crit.get("5%")),
            "crit_10%": float(crit.get("10%")),
        }

    adf_table = pd.DataFrame(
        [
            adf_row(df["Price"], "Price level (full)"),
            adf_row(np.log(df["Price"]).diff().dropna(), "Log returns (full)"),
            adf_row(df_10y["Price"], "Price level (last 10y)"),
            adf_row(returns_df["log_return"], "Log returns (last 10y)"),
        ]
    )

    adf_table.to_csv(out_dir / "task1_adf_stationarity.csv", index=False)

    print("Wrote figures to", fig_dir)
    print("Wrote stationarity table to", out_dir / "task1_adf_stationarity.csv")


if __name__ == "__main__":
    main()
