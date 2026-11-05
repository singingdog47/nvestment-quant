"""PTS observer entry point.

Input is deliberately provider-neutral. A collector should write
 data/pts_observer/latest.csv with:
 code,name,regular_close,pts_price,volume,turnover_jpy

This keeps scraping/API credentials outside the scoring layer and prevents
an unstable public HTML endpoint from becoming a trading dependency.
"""
from pathlib import Path
import pandas as pd

from pts_observer import PTSObservation, append_observations, evaluate, load_config


def main() -> None:
    cfg = load_config()
    src = Path("data/pts_observer/latest.csv")
    if not src.exists():
        print("PTS input unavailable; observe-only run skipped safely.")
        return
    raw = pd.read_csv(src, dtype={"code": str})
    obs = [
        PTSObservation(
            code=str(r.code), name=str(r.name), regular_close=float(r.regular_close),
            pts_price=float(r.pts_price), volume=int(r.volume),
            turnover_jpy=float(r.turnover_jpy),
        )
        for r in raw.itertuples(index=False)
    ]
    result = evaluate(obs, cfg)
    append_observations(result, "data/pts_observer/history.csv")
    Path("data/pts_observer").mkdir(parents=True, exist_ok=True)
    result.to_csv("data/pts_observer/latest_scored.csv", index=False)
    alerts = result[result["alert"]] if not result.empty else result
    print(alerts.to_string(index=False) if not alerts.empty else "No material PTS alerts.")


if __name__ == "__main__":
    main()
