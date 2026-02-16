from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_prices() -> list[dict]:
    import pandas as pd

    csv_path = project_root() / "data" / "raw" / "brent_oil_prices.csv"
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Price"])

    out = df.rename(columns={"Date": "date", "Price": "price"})
    out["date"] = out["date"].dt.date.astype(str)
    return out.to_dict(orient="records")


def load_events() -> list[dict]:
    import pandas as pd

    csv_path = project_root() / "data" / "raw" / "oil_market_events.csv"
    df = pd.read_csv(csv_path)
    df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")
    df = df.dropna(subset=["event_date"]).sort_values("event_date")
    df["event_date"] = df["event_date"].dt.date.astype(str)
    return df.to_dict(orient="records")


def load_changepoint_summary() -> dict:
    path = project_root() / "models" / "changepoint_summary.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/prices")
def prices():
    """Historical price data.

    Optional query params:
      - start=YYYY-MM-DD
      - end=YYYY-MM-DD
    """
    data = load_prices()
    start = request.args.get("start")
    end = request.args.get("end")

    if start or end:
        from datetime import date

        def to_date(s: str) -> date:
            return date.fromisoformat(s)

        if start:
            start_d = to_date(start)
            data = [r for r in data if to_date(r["date"]) >= start_d]
        if end:
            end_d = to_date(end)
            data = [r for r in data if to_date(r["date"]) <= end_d]

    return jsonify(data)


@app.get("/api/events")
def events():
    return jsonify(load_events())


@app.get("/api/changepoint")
def changepoint():
    return jsonify(load_changepoint_summary())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
