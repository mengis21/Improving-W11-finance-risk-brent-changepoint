# Brent Oil Regime Shift Risk Analytics (Week 12 Capstone Improvement)

![CI](https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint/actions/workflows/ci.yml/badge.svg)

Production-grade Bayesian change-point analytics for Brent oil prices with event attribution, tested APIs, and an interactive dashboard for finance risk decision support.

## Business Problem

Risk teams and analysts need timely detection of market regime shifts to avoid delayed responses in hedging, forecasting, and exposure management. Brent oil prices react to geopolitical and policy shocks, but change points are often identified late or inconsistently. This project provides a transparent, repeatable workflow that detects likely structural breaks and links them to curated market events.

## Solution Overview

- Build cleaned daily Brent price and event datasets.
- Transform prices into log returns for stationarity-aware modeling.
- Fit a Bayesian single change-point model (mean and volatility shift).
- Expose results through API endpoints and an interactive dashboard.
- Add automated tests and CI checks for reliability.

## Key Results

- Detected posterior median change point near **2018-11-15** with event alignment to 2018 sanctions context.
- 90-day mean price window changed by approximately **-18.74%** around the inferred shift.
- Automated quality gates: **10 passing tests** with CI execution on push/PR.

## Quick Start

```bash
git clone https://github.com/mengis21/Improving-W11-finance-risk-brent-changepoint.git
cd Improving-W11-finance-risk-brent-changepoint
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python dashboard/backend/app.py
```

In another terminal:

```bash
cd dashboard/frontend
npm install
npm run dev
```

## Project Structure

```
.
├─ data/
│  ├─ raw/
│  └─ processed/
├─ models/
├─ notebooks/
├─ src/
├─ tests/
├─ dashboard/
│  ├─ backend/
│  └─ frontend/
└─ .github/workflows/
```

## Demo

- Local dashboard: run Flask backend + Vite frontend and open the URL printed by Vite.
- Suggested screenshots for submission: dashboard overview, filtered view, event/changepoint context.

## Technical Details

- **Data:** Brent daily prices and curated geopolitical/policy event data.
- **Model:** Bayesian single change point on standardized log returns with pre/post mean and volatility parameters.
- **Evaluation:** posterior summaries, nearest-event mapping, and reproducible test/CI checks.

## Future Improvements

- Extend to multiple change points and robust/heavy-tailed likelihoods.
- Add uncertainty bands directly in dashboard views.
- Add performance profiling and endpoint latency benchmarks.
