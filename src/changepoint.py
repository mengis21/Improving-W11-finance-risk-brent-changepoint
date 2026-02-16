from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ChangePointSummary:
    tau_index_median: int
    tau_index_hdi_94: tuple[int, int]
    tau_date_median: str
    tau_date_hdi_94: tuple[str, str]
    mu_before_mean: float
    mu_after_mean: float
    sigma_before_mean: float
    sigma_after_mean: float
    prob_mu_after_gt_before: float


def fit_single_changepoint_normal(
    y: np.ndarray,
    *,
    draws: int = 1500,
    tune: int = 1500,
    chains: int = 2,
    target_accept: float = 0.9,
    random_seed: int = 42,
) -> Any:
    """Single change point model with mean+sigma shift.

    Model:
      tau ~ DiscreteUniform(0, n-2)
      mu1, mu2 ~ Normal(0, 1)
      sigma1, sigma2 ~ HalfNormal(1)
      y[t] ~ Normal(mu = switch(t < tau, mu1, mu2), sigma = switch(t < tau, sigma1, sigma2))

    Notes:
      - `y` should be roughly standardized (e.g., returns or standardized log-price).
      - We allow sigma to shift because returns often show volatility regime changes.
    """

    import pymc as pm

    y = np.asarray(y, dtype=float)
    if y.ndim != 1:
        raise ValueError("y must be 1D")
    if len(y) < 10:
        raise ValueError("y is too short for changepoint modeling")

    n = len(y)
    idx = np.arange(n)

    with pm.Model() as model:
        tau = pm.DiscreteUniform("tau", lower=0, upper=n - 2)

        mu_before = pm.Normal("mu_before", mu=0.0, sigma=1.0)
        mu_after = pm.Normal("mu_after", mu=0.0, sigma=1.0)

        sigma_before = pm.HalfNormal("sigma_before", sigma=1.0)
        sigma_after = pm.HalfNormal("sigma_after", sigma=1.0)

        mu_t = pm.math.switch(idx <= tau, mu_before, mu_after)
        sigma_t = pm.math.switch(idx <= tau, sigma_before, sigma_after)

        pm.Normal("obs", mu=mu_t, sigma=sigma_t, observed=y)

        idata = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            random_seed=random_seed,
            return_inferencedata=True,
        )

    return idata


def summarize_tau(idata: Any) -> tuple[int, tuple[int, int]]:
    import arviz as az

    tau_samples = idata.posterior["tau"].values.reshape(-1)
    tau_median = int(np.median(tau_samples))
    hdi = az.hdi(tau_samples, hdi_prob=0.94)
    tau_hdi = (int(hdi[0]), int(hdi[1]))
    return tau_median, tau_hdi


def build_summary(
    idata: Any,
    *,
    dates: pd.Series | list[pd.Timestamp] | np.ndarray,
) -> ChangePointSummary:
    dates = pd.to_datetime(pd.Series(dates)).reset_index(drop=True)

    tau_median, tau_hdi = summarize_tau(idata)

    def idx_to_date(i: int) -> str:
        i = int(np.clip(i, 0, len(dates) - 1))
        d = dates.iloc[i].date() if hasattr(dates.iloc[i], "date") else dates.iloc[i]
        if isinstance(d, (pd.Timestamp,)):
            d = d.date()
        if isinstance(d, date):
            return d.isoformat()
        return str(d)

    mu_before = float(idata.posterior["mu_before"].values.mean())
    mu_after = float(idata.posterior["mu_after"].values.mean())
    sigma_before = float(idata.posterior["sigma_before"].values.mean())
    sigma_after = float(idata.posterior["sigma_after"].values.mean())

    prob_mu_after_gt_before = float(
        (idata.posterior["mu_after"] > idata.posterior["mu_before"]).values.mean()
    )

    return ChangePointSummary(
        tau_index_median=tau_median,
        tau_index_hdi_94=tau_hdi,
        tau_date_median=idx_to_date(tau_median),
        tau_date_hdi_94=(idx_to_date(tau_hdi[0]), idx_to_date(tau_hdi[1])),
        mu_before_mean=mu_before,
        mu_after_mean=mu_after,
        sigma_before_mean=sigma_before,
        sigma_after_mean=sigma_after,
        prob_mu_after_gt_before=prob_mu_after_gt_before,
    )


def summary_to_dict(summary: ChangePointSummary) -> dict[str, Any]:
    return {
        "tau_index_median": summary.tau_index_median,
        "tau_index_hdi_94": list(summary.tau_index_hdi_94),
        "tau_date_median": summary.tau_date_median,
        "tau_date_hdi_94": list(summary.tau_date_hdi_94),
        "mu_before_mean": summary.mu_before_mean,
        "mu_after_mean": summary.mu_after_mean,
        "sigma_before_mean": summary.sigma_before_mean,
        "sigma_after_mean": summary.sigma_after_mean,
        "prob_mu_after_gt_before": summary.prob_mu_after_gt_before,
    }


def nearest_event(
    *,
    target_date: str | pd.Timestamp,
    events: pd.DataFrame,
    max_days: int = 45,
) -> dict[str, Any] | None:
    if events.empty:
        return None

    target = pd.to_datetime(target_date)
    e = events.copy()
    e["event_date"] = pd.to_datetime(e["event_date"])
    e["abs_days"] = (e["event_date"] - target).abs().dt.days
    best = e.sort_values("abs_days").iloc[0]

    if int(best["abs_days"]) > max_days:
        return None

    return {
        "event_date": pd.to_datetime(best["event_date"]).date().isoformat(),
        "event_title": str(best.get("event_title", "")),
        "event_type": str(best.get("event_type", "")),
        "region": str(best.get("region", "")),
        "notes": str(best.get("notes", "")),
        "abs_days": int(best["abs_days"]),
    }
