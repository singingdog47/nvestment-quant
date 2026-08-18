from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .config import SETTINGS
from .scoring import add_final_scores, add_technical_scores
from .tradingview import download_market_snapshot
from .universe import load_universe

LOG = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def _serializable(value):
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def quality_report(
    universe: pd.DataFrame,
    technical: pd.DataFrame,
    final: pd.DataFrame,
    run_status: str = "ok",
    failure_reason: str | None = None,
) -> dict:
    market_counts = universe.groupby("market")["ticker"].count().to_dict()
    price_ok = technical["price_status"].eq("ok")
    eligible = technical["eligible"].fillna(False)
    fundamental_status = final.get("fundamental_status", pd.Series(dtype=str)).value_counts(dropna=False).to_dict()
    retrieved = technical.loc[price_ok, "data_retrieved_at_utc"].dropna()
    return {
        "run_status": run_status,
        "failure_reason": failure_reason,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "MVP: official universe cross-check + full-universe TradingView snapshot",
        "universe_count": int(len(universe)),
        "universe_by_market": {str(k): int(v) for k, v in market_counts.items()},
        "universe_errors": universe.attrs.get("errors", []),
        "price_ok_count": int(price_ok.sum()),
        "price_missing_count": int((~price_ok).sum()),
        "price_missing_rate": float((~price_ok).mean()) if len(technical) else None,
        "eligible_count": int(eligible.sum()),
        "data_retrieved_at_utc": str(retrieved.max()) if not retrieved.empty else None,
        "price_timestamp_status": "unverified_exact_exchange_timestamp",
        "fundamental_status": {str(k): int(v) for k, v in fundamental_status.items()},
        "scored_count": int(final["total_score"].notna().sum()),
        "settings": {key: _serializable(value) for key, value in SETTINGS.__dict__.items()},
        "hard_warnings": [
            "Price and fundamentals are retrieved through an unofficial, undocumented TradingView scanner endpoint.",
            "The exact exchange timestamp of the close field is unavailable; verify executable prices separately.",
            "A high score is a relative comparison, not a buy signal.",
            "Missing values are not silently imputed; low-coverage rows are left unscored.",
        ],
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    DATA.mkdir(parents=True, exist_ok=True)
    LOG.info("loading universe")
    universe = load_universe()
    LOG.info("universe: %s", universe.groupby("market")["ticker"].count().to_dict())
    snapshot = download_market_snapshot(universe)
    technical = add_technical_scores(snapshot)
    missing_rate = float(technical["price_status"].ne("ok").mean()) if len(technical) else 1.0
    eligible_count = int(technical["eligible"].sum())
    if missing_rate > 0.30 or eligible_count == 0:
        reason = f"価格取得の品質ゲートで停止: missing_rate={missing_rate:.1%}, eligible={eligible_count}"
        failed = quality_report(
            universe,
            technical,
            pd.DataFrame(columns=["total_score", "fundamental_status"]),
            run_status="failed",
            failure_reason=reason,
        )
        (DATA / "quality_report.json").write_text(
            json.dumps(failed, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        raise RuntimeError(reason)
    final = add_final_scores(technical[technical["eligible"]].copy())

    full_path = DATA / "screening_full.csv.gz"
    latest_path = DATA / "screening_latest.csv"
    report_path = DATA / "quality_report.json"
    technical.to_csv(full_path, index=False, compression="gzip")
    market_count = max(1, final["market"].nunique())
    per_market = max(1, SETTINGS.output_top_n // market_count)
    selected = (
        final.sort_values(["market", "total_score"], ascending=[True, False])
        .groupby("market", group_keys=False)
        .head(per_market)
        .sort_values("total_score", ascending=False)
        .head(SETTINGS.output_top_n)
    )
    selected.to_csv(latest_path, index=False)
    report = quality_report(universe, technical, final)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.info("wrote %s, %s, %s", full_path, latest_path, report_path)


if __name__ == "__main__":
    main()
