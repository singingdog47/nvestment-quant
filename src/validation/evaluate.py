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

BENCHMARKS = {
    "JP": "1306.T",  # TOPIX-linked ETF proxy
    "JAPAN": "1306.T",
    "TSE": "1306.T",
    "TOKYO": "1306.T",
    "US": "SPY",     # S&P 500 ETF proxy
    "NASDAQ": "SPY",
    "NYSE": "SPY",
    "AMEX": "SPY",
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
    code = item.get("code")
    market = str(item.get("market") or "").upper()
    if code and (market in {"JP", "JAPAN", "TSE", "TOKYO"} or (str(code).isdigit() and len(str(code)) == 4)):
        return f"{code}.T"
    if ticker:
        return str(ticker)
    return str(code) if code else None


def _benchmark_symbol(item: dict[str, Any], symbol: str | None = None) -> str | None:
    market = str(item.get("market") or "").upper()
    if market in BENCHMARKS:
        return BENCHMARKS[market]
    if symbol and symbol.endswith(".T"):
        return "1306.T"
    return None


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
        if getattr(close, "ndim", 1) == 2:
            close = close.iloc[:, 0]
        return close.dropna()
    except Exception:
        return None


def _outcome_for_symbol(symbol: str, captured_at: datetime, days: int) -> dict[str, Any] | None:
    target = captured_at + timedelta(days=days)
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


def _benchmark_result(item: dict[str, Any], symbol: str, captured_at: datetime, days: int) -> dict[str, Any]:
    benchmark_symbol = _benchmark_symbol(item, symbol)
    if not benchmark_symbol:
        return {"benchmark_symbol": None, "benchmark_return": None, "excess_return": None}
    result = _outcome_for_symbol(benchmark_symbol, captured_at, days)
    if not result:
        return {"benchmark_symbol": benchmark_symbol, "benchmark_return": None, "excess_return": None}
    return {"benchmark_symbol": benchmark_symbol, "benchmark_return": result["return"]}


def _summary_fields() -> list[str]:
    return [
        "decision_id",
        "captured_at",
        "market_regime",
        "recommended_action",
        "horizon",
        "symbol",
        "rank",
        "return",
        "benchmark_symbol",
        "benchmark_return",
        "excess_return",
        "max_up",
        "max_down",
        "evaluated_price_date",
        "model_version",
    ]


def _append_summary(root: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    out = root / "data/validation/outcomes.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = _summary_fields()
    existing: list[dict[str, Any]] = []
    existing_keys: set[tuple[str, str, str]] = set()
    if out.exists():
        with out.open("r", encoding="utf-8-sig", newline="") as f:
            existing = list(csv.DictReader(f))
        for row in existing:
            existing_keys.add((row.get("decision_id", ""), row.get("horizon", ""), row.get("symbol", "")))
    new_rows = [
        r for r in rows
        if (str(r["decision_id"]), str(r["horizon"]), str(r["symbol"])) not in existing_keys
    ]
    if not new_rows and out.exists() and all(x in (existing[0].keys() if existing else fields) for x in ("benchmark_symbol", "excess_return")):
        return

    # Rewrite the file using the new schema so pre-v2.1 rows remain readable with blank benchmark fields.
    merged = existing + new_rows
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)


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
                bench = _benchmark_result(item, symbol, captured, days)
                benchmark_return = _safe_float(bench.get("benchmark_return"))
                excess_return = result["return"] - benchmark_return if benchmark_return is not None else None
                result.update(bench)
                result["excess_return"] = excess_return
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
                        "benchmark_symbol": bench.get("benchmark_symbol"),
                        "benchmark_return": benchmark_return,
                        "excess_return": excess_return,
                        "max_up": result["max_up"],
                        "max_down": result["max_down"],
                        "evaluated_price_date": result["evaluated_price_date"],
                        "model_version": record.get("model_version"),
                    }
                )
            if per_symbol:
                avg_return = sum(r["return"] for r in per_symbol) / len(per_symbol)
                benchmark_values = [r.get("benchmark_return") for r in per_symbol if r.get("benchmark_return") is not None]
                excess_values = [r.get("excess_return") for r in per_symbol if r.get("excess_return") is not None]
                outcomes[horizon] = {
                    "evaluated_at": now.isoformat(timespec="seconds"),
                    "n": len(per_symbol),
                    "average_return": avg_return,
                    "benchmark_coverage_n": len(excess_values),
                    "average_benchmark_return": (sum(benchmark_values) / len(benchmark_values)) if benchmark_values else None,
                    "average_excess_return": (sum(excess_values) / len(excess_values)) if excess_values else None,
                    "symbols": per_symbol,
                }
                changed = True

        if changed:
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            updated += 1

    _append_summary(root, summary_rows)
    return updated
