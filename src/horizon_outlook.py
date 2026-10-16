"""Prospective multi-horizon market/flow outlook (public, research-only).

This module never places orders, changes screening ranks, reads private portfolio
data, or interprets missing supply/demand observations as institutional flows.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

JST = timezone(timedelta(hours=9))
VERSION = "1.0.0"
DEFAULT_CONFIG = {
    "short": {"sessions": "5-10", "label": "1-2 weeks", "validation_horizon": "1w"},
    "medium": {"sessions": "20-60", "label": "1-3 months", "validation_horizon": "1m"},
    "long": {"sessions": "250-750", "label": "1-3 years", "validation_horizon": None},
}
BENCHMARK = {"JP": "1306.T", "US": "SPY"}


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def _rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as source:
            return list(csv.DictReader(source))
    except (OSError, UnicodeError):
        return []


def _float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
        return parsed if math.isfinite(parsed) else None
    except (ValueError, TypeError):
        return None


def _date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        value = value.replace("Z", "+00:00")
        instant = datetime.fromisoformat(value)
        return instant.replace(tzinfo=timezone.utc) if instant.tzinfo is None else instant
    except (ValueError, TypeError):
        return None


def _symbol(row: dict[str, Any]) -> str | None:
    market = str(row.get("market") or "").upper()
    code = str(row.get("code") or "").strip()
    ticker = str(row.get("ticker") or "").strip()
    if market == "JP" and code.isdigit() and len(code) == 4:
        return code + ".T"
    if market == "US" and ticker:
        return ticker
    return None


def _eligible_signals(
    screening: list[dict[str, str]],
    supply: list[dict[str, str]],
    day: str,
    issued_at: str,
    cap: int = 3,
) -> list[dict[str, Any]]:
    """Only forecast on *fresh*, explicit volume/price evidence, not inferred buyers."""
    by_key = {(r.get("market", "").upper(), r.get("code", "")): r for r in supply}
    valid_screen = [r for r in screening if r.get("research_status", "research_candidate") == "research_candidate"]
    # Align with the existing validation system's top-10 screen: it sorts
    # market_rank first, and otherwise pre_score/total_score descending.
    rank_key = next((k for k in ("market_rank", "rank", "pre_score", "total_score", "score") if valid_screen and k in valid_screen[0]), None)
    if rank_key:
        descending = rank_key in {"pre_score", "total_score", "score"}
        valid_screen.sort(key=lambda x: _float(x.get(rank_key)) if _float(x.get(rank_key)) is not None else (float("-inf") if descending else float("inf")), reverse=descending)
    result = []
    for item in valid_screen[:10]:
        market, code = item.get("market", "").upper(), item.get("code", "")
        obs = by_key.get((market, code))
        if obs is None or obs.get("observed_date") != day or obs.get("data_status") != "ok":
            continue
        if (_float(obs.get("confidence")) or 0) < 0.6:
            continue
        price_stamp = _date(obs.get("price_as_of"))
        if price_stamp is None or price_stamp.astimezone(JST).date().isoformat() != day:
            continue  # price must be dated; a fresh processing timestamp is not enough
        flags = set(str(obs.get("context_flags") or "").split("|"))
        volume = _float(obs.get("current_volume_ratio_30d"))
        if volume is None or volume < 1.5 or "VOLUME_EXPANSION" not in flags:
            continue
        if "PRICE_UP_ON_VOLUME_EXPANSION" in flags:
            direction = "positive"
        elif "PRICE_DOWN_ON_VOLUME_EXPANSION" in flags:
            direction = "negative"
        else:
            continue
        symbol = _symbol(item)
        if not symbol or market not in BENCHMARK:
            continue
        key = f"{day}|{symbol}|1w|{direction}|v1"
        result.append({
            "id": hashlib.sha256(key.encode("utf-8")).hexdigest()[:16],
            "market": market, "symbol": symbol,
            "name": item.get("name") or symbol,
            "benchmark_symbol": BENCHMARK[market],
            "horizon": "short", "validation_horizon": "1w",
            "metric": "total_return_excess_over_benchmark",
            "threshold": 0.0, "expected_sign": direction,
            "probability": 0.55,
            "probability_label": "uncalibrated_research_prior_not_estimated_accuracy",
            "issued_at_utc": issued_at, "as_of_jst": day,
            "evidence": {
                "volume_ratio_30d": volume,
                "context_flags": sorted(flags),
                "data_status": obs.get("data_status"),
                "confidence": _float(obs.get("confidence")),
                "source_retrieved_at": obs.get("source_retrieved_at"),
                "price_as_of": obs.get("price_as_of"),
            },
            "rationale": "Volume expansion and same-direction price movement: continuation hypothesis, not verified net buying/selling.",
            "falsification": f"Relative total return at the existing 1w validation endpoint is {'<= 0' if direction == 'positive' else '>= 0'}.",
            "execution": "RESEARCH_ONLY_NO_AUTO_TRADE",
        })
        if len(result) >= cap:
            break
    return result


def build_outlook(
    regime: dict[str, Any],
    supply_summary: dict[str, Any],
    supply_rows: list[dict[str, str]],
    screening_rows: list[dict[str, str]],
    now: datetime,
) -> dict[str, Any]:
    now = now.astimezone(timezone.utc)
    day = now.astimezone(JST).date().isoformat()
    issued_at = now.isoformat(timespec="seconds")
    regime_fresh = regime.get("date_jst") == day and regime.get("data_status") == "ok" and bool(regime.get("actionable"))
    supply_fresh = supply_summary.get("observed_date_jst") == day and supply_summary.get("data_status") in {"ok", "partial"}
    shock = bool(regime.get("treasury_volatility_shock_flag")) if regime_fresh else None
    label = str(regime.get("regime_label") or "UNKNOWN") if regime_fresh else "UNKNOWN"
    score = _float(regime.get("regime_score")) if regime_fresh else None
    supply_coverage = supply_summary.get("coverage") if supply_fresh else {}
    hypotheses = (_eligible_signals(screening_rows, supply_rows, day, issued_at)
                  if regime_fresh and supply_fresh else [])
    signal_count = len(hypotheses)
    if not regime_fresh:
        short_view = "INSUFFICIENT_DATA"
        medium_view = "INSUFFICIENT_DATA"
    elif shock:
        short_view = "TWO_WAY_WITH_RATES_VOLATILITY_RISK"
        medium_view = "CONDITIONAL_RISK_REVIEW"
    elif label in {"CONSTRUCTIVE", "RISK_ON"}:
        short_view = "CONDITIONAL_RISK_ON"
        medium_view = "CONDITIONAL_CONSTRUCTIVE"
    elif label in {"RISK_OFF", "STRESS"}:
        short_view = "DEFENSIVE_CONTEXT"
        medium_view = "CONDITIONAL_RISK_REVIEW"
    else:
        short_view = "RANGE_OR_UNDECIDED"
        medium_view = "CONDITIONAL_UNDECIDED"
    horizons = [
        {
            "name": "short", **DEFAULT_CONFIG["short"], "view": short_view,
            "hypothesis": "Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.",
            "confirmation": "Validate each logged signal against 1306.T or SPY after the 1w horizon; inspect price breadth and volatility jointly.",
            "invalidation": "A contrary relative return at the predetermined endpoint or worsening rates/credit stress.",
            "trade_policy": "Existing orders unchanged. New purchase only after liquidity, risk and human review.",
        },
        {
            "name": "medium", **DEFAULT_CONFIG["medium"], "view": medium_view,
            "hypothesis": "Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.",
            "confirmation": "Observe relative sector returns and dated positioning/credit data for 20-60 sessions.",
            "invalidation": "Rotation reverses for several weeks or earnings/credit assumptions change materially.",
            "trade_policy": "Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.",
        },
        {
            "name": "long", **DEFAULT_CONFIG["long"], "view": "FUNDAMENTALS_NOT_ESTABLISHED",
            "hypothesis": "Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.",
            "confirmation": "Require multi-year primary fundamentals, valuation ranges, and thesis-specific catalysts.",
            "invalidation": "Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.",
            "trade_policy": "Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.",
        },
    ]
    return {
        "version": VERSION, "generated_at_utc": issued_at, "as_of_jst": day,
        "mode": "RESEARCH_ONLY",
        "source_status": {
            "regime_fresh": regime_fresh, "supply_fresh": supply_fresh,
            "regime": label, "regime_score": score,
            "treasury_volatility_shock": shock,
            "supply_coverage": supply_coverage or {},
            "public_watchlist_only": True,
            "private_portfolio_included": False,
        },
        "horizons": horizons, "prospective_hypotheses": hypotheses,
        "hypothesis_candidates_detected": signal_count,
        "limits": [
            "Regime confidence describes source coverage, not prediction accuracy.",
            "0.55 is a declared research prior, not a calibrated model probability.",
            "Volume/price co-movement is not proof of institutional buying or distribution.",
            "Delayed position/short interest releases must be evaluated by their as-of date, never publication day alone.",
            "This module does not place orders, alter ranking, or override existing risk and data-quality gates.",
        ],
    }


def grade_hypotheses(history: list[dict[str, Any]], outcomes: list[dict[str, str]]) -> dict[str, Any]:
    """Use existing validation results; never query future prices at issuance."""
    lookup: dict[tuple[str, str, str], tuple[datetime, float]] = {}
    for row in outcomes:
        timestamp = _date(row.get("captured_at"))
        excess = _float(row.get("excess_return"))
        if timestamp is None or excess is None:
            continue
        key = (row.get("symbol", ""), row.get("horizon", ""), timestamp.astimezone(JST).date().isoformat())
        old = lookup.get(key)
        if old is None or timestamp < old[0]:
            lookup[key] = (timestamp, excess)
    graded = []
    pending = 0
    for forecast in history:
        issued = _date(forecast.get("issued_at_utc"))
        if not issued:
            continue
        key = (forecast.get("symbol", ""), forecast.get("validation_horizon", ""), forecast.get("as_of_jst", ""))
        record = lookup.get(key)
        # Reject same-day outcomes from a *different* earlier decision snapshot.
        if record is None or record[0] < issued:
            pending += 1
            continue
        excess = record[1]
        success = (excess > 0 if forecast.get("expected_sign") == "positive" else excess < 0)
        probability = _float(forecast.get("probability"))
        if probability is None or not 0 <= probability <= 1:
            continue
        graded.append({
            "id": forecast.get("id"), "symbol": forecast.get("symbol"),
            "as_of_jst": forecast.get("as_of_jst"), "outcome_excess": excess,
            "correct": success, "brier": (probability - float(success)) ** 2,
        })
    return {
        "version": VERSION, "graded_n": len(graded), "pending_n": pending,
        "accuracy": sum(x["correct"] for x in graded) / len(graded) if graded else None,
        "mean_brier": sum(x["brier"] for x in graded) / len(graded) if graded else None,
        "calibrated": False, "observations": graded,
        "interpretation": "Research-prior scoring only. Compare to base rates and baselines before claiming forecasting skill.",
    }


def _render(outlook: dict[str, Any], graded: dict[str, Any]) -> str:
    lines = [
        "# Multi-horizon research outlook",
        f"Generated (UTC): {outlook['generated_at_utc']}",
        "Public watchlist only; no private holdings or automatic trades.",
        "",
        "## 短期・中期・長期の仮説と売買方針",
        "",
        "| 期間 | 市場仮説の状態 | 監視・執行方針 |",
        "|---|---|---|",
    ]
    for h in outlook["horizons"]:
        lines.append(f"| {h['name']} ({h['label']}) | {h['view']} | {h['trade_policy']} |")
    lines += ["", "## Prospective, testable demand hypotheses"]
    for h in outlook["prospective_hypotheses"]:
        lines.append(f"- [{h['horizon']}] {h['symbol']} excess vs {h['benchmark_symbol']}: {h['expected_sign']} (> or < 0). p={h['probability']:.2f} (uncalibrated). ID={h['id']}")
    if not outlook["prospective_hypotheses"]:
        lines.append("- No eligible fresh signal; do not manufacture a directional forecast.")
    lines += ["", "## 検証", f"- Scored: {graded['graded_n']}, pending: {graded['pending_n']}, mean Brier: {graded['mean_brier']}", ""]
    lines.extend(["- " + x for x in outlook["limits"]])
    return "\n".join(lines) + "\n"


def run(root: str | Path = ".", now: datetime | None = None) -> dict[str, Path]:
    root = Path(root)
    now = now or datetime.now(timezone.utc)
    day = now.astimezone(JST).date().isoformat()
    regime = _load(root / "data/regime/market_regime_latest.json")
    supply_summary = _load(root / "data/supply_demand/supply_demand_summary_latest.json")
    supply_rows = _rows(root / "data/supply_demand/supply_demand_latest.csv")
    screening = _rows(root / "data/screening_latest.csv")
    outlook = build_outlook(regime, supply_summary, supply_rows, screening, now)
    out = root / "data/horizon_outlook"
    archive = out / "history" / day[:4] / f"{day}.json"
    archive.parent.mkdir(parents=True, exist_ok=True)
    if not archive.exists():
        archive.write_text(json.dumps(outlook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Existing archives are immutable: intraday reruns cannot rewrite predictions.
    all_predictions = []
    for path in sorted((out / "history").glob("*/*.json")):
        all_predictions.extend(_load(path).get("prospective_hypotheses") or [])
    graded = grade_hypotheses(all_predictions, _rows(root / "data/validation/outcomes.csv"))
    latest = out / "horizon_latest.json"
    md = out / "horizon_latest.md"
    results = out / "learning_latest.json"
    latest.write_text(json.dumps(outlook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    results.write_text(json.dumps(graded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md.write_text(_render(outlook, graded), encoding="utf-8")
    return {"latest": latest, "markdown": md, "learning": results, "archive": archive}
