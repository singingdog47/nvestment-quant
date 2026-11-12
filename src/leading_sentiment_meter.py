"""Experimental Japan equity sentiment meter. No trade execution.

Input: JSON object with as_of and signals (each signal has value 0..100,
observed_at ISO timestamp, and optional quality 'ok'/'missing').
Scores measure risk appetite, not expected index return.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
from pathlib import Path

WEIGHTS = {"volatility": .25, "breadth": .25, "trend": .15,
           "futures": .10, "credit": .15, "fx_global": .10}
MAX_AGE_DAYS = {"volatility": 2, "breadth": 2, "trend": 2,
                "futures": 1, "credit": 7, "fx_global": 2}

def _date(value):
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include timezone")
    return parsed.astimezone(dt.timezone.utc)

def calculate(payload):
    as_of = _date(payload["as_of"])
    valid = {}
    rejected = {}
    for key, weight in WEIGHTS.items():
        item = payload.get("signals", {}).get(key)
        if not isinstance(item, dict) or item.get("quality", "ok") != "ok":
            rejected[key] = "missing_or_bad_quality"
            continue
        try:
            value = float(item["value"])
            observed = _date(item["observed_at"])
        except (ValueError, KeyError, TypeError):
            rejected[key] = "invalid_value_or_timestamp"
            continue
        age = (as_of - observed).total_seconds() / 86400
        if not 0 <= value <= 100 or age < 0 or age > MAX_AGE_DAYS[key]:
            rejected[key] = "out_of_range_or_stale"
            continue
        valid[key] = value
    coverage = round(sum(WEIGHTS[k] for k in valid), 3)
    if coverage < .8 or "volatility" not in valid or "breadth" not in valid:
        status, score = "INSUFFICIENT_DATA", None
    else:
        status = "OBSERVED_ONLY"
        score = round(sum(WEIGHTS[k] * v for k, v in valid.items()) / coverage, 1)
    return {"as_of": payload["as_of"], "status": status,
            "current_sentiment": score, "coverage": coverage,
            "forecast_5d": None, "forecast_status": "NOT_CALIBRATED",
            "signals_used": sorted(valid), "signals_rejected": rejected,
            "action": "NO_AUTOMATIC_TRADE",
            "note": "Inputs are normalized signal scores; forecast withheld until walk-forward validation."}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = calculate(json.loads(args.input_json.read_text(encoding="utf-8")))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

if __name__ == "__main__":
    main()
