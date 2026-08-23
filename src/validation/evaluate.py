from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


HORIZONS = {
    "1w": 7,
    "1m": 30,
    "3m": 90,
}


def _parse_dt(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _safe_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _market_symbol(item: dict[str, Any]) -> str | None:
    ticker = item.get("ticker")
    if ticker:
        return str(ticker)
    code = item.get("code")
    market = str(item.get("market") or "").upper()
    if code and market == "JP":
        return f"{code}.T"
    return str(code) if code else None


def _download_prices(symbol: str, start: datetime, end: datetime):
    try:
        import yfinance as yf
    except ImportError:
        return None
    try:
        df = yf.download(
            symbol,
            start=start.date().isoformat(),
            end=end.date().isoformat(),
            progress=False,
            auto_adjust=True,
            threads=False,
        )
    except Exception:
        return None
    if df is None or len(df) == 0:
        return None
    return df


def _close_series(df):
    if df is None:
        return None
    close = df.get("Close")
    if close is None:
        return None
    try:
        # yfinance may return a one-column DataFrame for recent versions.
        if getattr(close, "ndim", 1) == 2:
            close = close.iloc[:, 0]
        return close.dropna()
    except Exception:
        return None


def _outcome_for_symbol(symbol: str, captured_at: datetime, days: int) -> dict[str, Any] | None:
    target = captured_at + timedelta(days=days)
    # Calendar horizons need a small trading-day buffer around the target.
    df = _download_prices(symbol, captured_at - timedelta(days=3), target + timedelta(days=8))
    close = _close_series(df)
    if close is None or len(close) < 2:
        return None

    start_candidates = close[close.index >= captured_at.replace(tzinfo=None)]
    if len(start_candidates) == 0:
        start_candidates = close
    start_px = float(start_candidates.iloc[0])

    end_candidates = close[close.index >= target.replace(tzinfo=None)]
    if len(end_candidates) == 0:
        return None
    end_px = float(end_candidates.iloc[0])

    window = close[(close.index >= start_candidates.index[0]) & (close.index <= end_candidates.index[0])]
    if len(window) == 0:
        return None

    returns = (window.astype(float) / start_px) - 1.0
    return {
        "symbol": symbol,
        "start_price": start_px,
        "end_price": end_px,
        "return": end_px / start_px - 1.0,
        "max_up": float(returns.max()),
        "max_down": float(returns.min()),
        "evaluated_price_date": str(end_candidates.index[0].date()),
    }


def _append_summary(root: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    out = root / "data/validation/outcomes.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "decision_id",
        "captured_at",
        "market_regime",
        "recommended_action",
        "horizon",
        "symbol",
        "rank",
        "return",
        "max_up",
        "max_down",
        "evaluated_price_date",
        "model_version",
    ]
    existing_keys: set[tuple[str, str, str]] = set()
    if out.exists():
        with out.open("r", encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                existing_keys.add((row.get("decision_id", ""), row.get("horizon", ""), row.get("symbol", "")))
    new_rows = [
        r for r in rows
        if (str(r["decision_id"]), str(r["horizon"]), str(r["symbol"])) not in existing_keys
    ]
    if not new_rows:
        return
    write_header = not out.exists()
    with out.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerows(new_rows)


def evaluate_due_outcomes(root: str | Path = ".", now: datetime | None = None) -> int:
    root = Path(root)
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    decisions = sorted((root / "data/validation/decisions").glob("*/*.json"))
    summary_rows: list[dict[str, Any]] = []
    updated = 0

    for path in decisions:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        captured = _parse_dt(record["captured_at"])
        outcomes = record.setdefault("outcomes", {})
        changed = False

        for horizon, days in HORIZONS.items():
            if horizon in outcomes or now < captured + timedelta(days=days):
                continue
            per_symbol: list[dict[str, Any]] = []
            for item in record.get("top_screening", []):
                symbol = _market_symbol(item)
                if not symbol:
                    continue
                result = _outcome_for_symbol(symbol, captured, days)
                if not result:
                    continue
                result["rank"] = item.get("rank")
                per_symbol.append(result)
                summary_rows.append(
                    {
                        "decision_id": record.get("decision_id"),
                        "captured_at": record.get("captured_at"),
                        "market_regime": record.get("market_regime"),
                        "recommended_action": record.get("recommended_action"),
                        "horizon": horizon,
                        "symbol": symbol,
                        "rank": item.get("rank"),
                        "return": result["return"],
                        "max_up": result["max_up"],
                        "max_down": result["max_down"],
                        "evaluated_price_date": result["evaluated_price_date"],
                        "model_version": record.get("model_version"),
                    }
                )
            if per_symbol:
                avg_return = sum(r["return"] for r in per_symbol) / len(per_symbol)
                outcomes[horizon] = {
                    "evaluated_at": now.isoformat(timespec="seconds"),
                    "n": len(per_symbol),
                    "average_return": avg_return,
                    "symbols": per_symbol,
                }
                changed = True

        if changed:
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            updated += 1

    _append_summary(root, summary_rows)
    return updated
