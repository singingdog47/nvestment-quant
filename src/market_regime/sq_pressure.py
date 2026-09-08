from __future__ import annotations

import json
import math
from datetime import date, datetime
from pathlib import Path
from typing import Any


def _number(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _clip(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def second_friday(year: int, month: int) -> date:
    """Return the calendar date of the second Friday in a month."""
    first = date(year, month, 1)
    days_to_friday = (4 - first.weekday()) % 7
    return date(year, month, 1 + days_to_friday + 7)


def _parse_date(value: Any) -> date | None:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if value in (None, ""):
        return None
    text = str(value).strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text).date()
    except ValueError:
        try:
            return date.fromisoformat(text[:10])
        except ValueError:
            return None


def next_major_sq_date(
    as_of: date,
    major_months: list[int] | tuple[int, ...] = (3, 6, 9, 12),
    overrides: dict[str, str] | None = None,
) -> date:
    """Return the next quarterly SQ date.

    The default is the second Friday. Holiday adjustments can be supplied via
    overrides, keyed by YYYY-MM (for example {"2027-03": "2027-03-11"}).
    This keeps the calendar logic explicit instead of silently guessing a
    holiday convention.
    """
    months = sorted({int(m) for m in major_months if 1 <= int(m) <= 12}) or [3, 6, 9, 12]
    overrides = overrides or {}
    for year in (as_of.year, as_of.year + 1, as_of.year + 2):
        for month in months:
            if year == as_of.year and month < as_of.month:
                continue
            key = f"{year:04d}-{month:02d}"
            candidate = _parse_date(overrides.get(key)) or second_friday(year, month)
            if candidate >= as_of:
                return candidate
    raise RuntimeError("could not resolve next major SQ date")


def load_sq_manual_input(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _manual_freshness(manual: dict[str, Any], as_of: date, max_age_days: int) -> tuple[str, int | None]:
    input_date = _parse_date(manual.get("as_of_date") or manual.get("generated_at") or manual.get("timestamp"))
    if input_date is None:
        return ("undated", None) if manual else ("missing", None)
    age = (as_of - input_date).days
    if age < 0:
        return "future_dated", age
    if age > max_age_days:
        return "stale", age
    return "fresh", age


def build_sq_execution_overlay(
    as_of: date,
    spot: float | None,
    cfg: dict[str, Any] | None = None,
    manual_input: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a non-directional SQ execution overlay.

    This overlay is intentionally not an alpha factor. It may change order
    staging and limit-order patience, but never security ranking, fundamental
    score, or the investment thesis. Open-interest imbalance is used only as a
    measure of expiry sensitivity; it is not interpreted as dealer gamma sign
    or as a deterministic market direction.
    """
    cfg = cfg or {}
    enabled = bool(cfg.get("enabled", True))
    cap = max(0.0, float(cfg.get("caution_cap_points", 15)))
    activation_days = max(0, int(cfg.get("activation_calendar_days", 6)))
    major_months = cfg.get("major_months", [3, 6, 9, 12])
    overrides = cfg.get("date_overrides", {}) or {}
    manual = manual_input or {}

    if not enabled:
        return {
            "version": "1.0",
            "enabled": False,
            "active": False,
            "data_status": "not_implemented",
            "directional_bias": "UNDETERMINED",
            "execution_caution_points": 0.0,
            "caution_cap_points": cap,
            "rule": "SQ overlay disabled; no execution adjustment applied.",
        }

    sq_date = next_major_sq_date(as_of, major_months, overrides)
    days_to_sq = (sq_date - as_of).days
    active = 0 <= days_to_sq <= activation_days
    if active:
        event_score = 100.0 * (activation_days - days_to_sq + 1) / (activation_days + 1)
    else:
        event_score = 0.0

    max_input_age = max(0, int(cfg.get("max_input_age_days", 3)))
    freshness, input_age = _manual_freshness(manual, as_of, max_input_age)
    manual_usable = bool(manual) and freshness in {"fresh", "undated"}

    put_oi = _number(manual.get("option_put_oi")) if manual_usable else None
    call_oi = _number(manual.get("option_call_oi")) if manual_usable else None
    front_oi = _number(manual.get("front_futures_oi")) if manual_usable else None
    next_oi = _number(manual.get("next_futures_oi")) if manual_usable else None
    call_wall = _number(manual.get("call_wall")) if manual_usable else None
    put_wall = _number(manual.get("put_wall")) if manual_usable else None
    magnet = _number(manual.get("magnet_strike")) if manual_usable else None
    arb_z = _number(manual.get("arbitrage_balance_zscore")) if manual_usable else None
    vi_pct = _number(manual.get("nikkei_vi_percentile")) if manual_usable else None

    pcr = put_oi / call_oi if put_oi is not None and call_oi not in (None, 0) and put_oi >= 0 and call_oi > 0 else None
    pcr_imbalance = None
    if pcr is not None and pcr > 0:
        pcr_imbalance = _clip(abs(math.log(pcr)) / math.log(2) * 100.0)

    front_share = None
    roll_concentration = None
    if front_oi is not None and next_oi is not None and front_oi >= 0 and next_oi >= 0 and (front_oi + next_oi) > 0:
        front_share = front_oi / (front_oi + next_oi)
        roll_concentration = _clip((front_share - 0.50) / 0.50 * 100.0)

    spot_n = _number(spot)
    reference_levels = [x for x in (magnet, call_wall, put_wall) if x is not None and x > 0]
    nearest_distance_pct = None
    pin_proximity = None
    if spot_n is not None and spot_n > 0 and reference_levels:
        nearest_distance_pct = min(abs(x - spot_n) / spot_n for x in reference_levels)
        pin_window = max(0.001, float(cfg.get("pin_distance_window_pct", 0.03)))
        pin_proximity = _clip((1.0 - nearest_distance_pct / pin_window) * 100.0)

    arbitrage_extreme = _clip(abs(arb_z) / 2.5 * 100.0) if arb_z is not None else None
    vi_extreme = _clip(vi_pct * 100.0) if vi_pct is not None and 0 <= vi_pct <= 1 else None

    raw_components = {
        "event_proximity": event_score,
        "option_oi_imbalance": pcr_imbalance,
        "front_futures_concentration": roll_concentration,
        "strike_pin_proximity": pin_proximity,
        "arbitrage_balance_extreme": arbitrage_extreme,
        "nikkei_vi_percentile": vi_extreme,
    }
    base_weights = {
        "event_proximity": 0.35,
        "option_oi_imbalance": 0.20,
        "front_futures_concentration": 0.20,
        "strike_pin_proximity": 0.10,
        "arbitrage_balance_extreme": 0.10,
        "nikkei_vi_percentile": 0.05,
    }
    available = {k: v for k, v in raw_components.items() if v is not None}
    available_weight = sum(base_weights[k] for k in available)
    intensity = (
        sum(available[k] * base_weights[k] for k in available) / available_weight
        if available_weight > 0 and active
        else 0.0
    )

    confidence = 0.25 if active else 0.40
    if pcr_imbalance is not None:
        confidence += 0.20
    if roll_concentration is not None:
        confidence += 0.20
    if pin_proximity is not None:
        confidence += 0.15
    if arbitrage_extreme is not None:
        confidence += 0.10
    if vi_extreme is not None:
        confidence += 0.10
    if freshness == "undated" and manual:
        confidence *= 0.85
    confidence = min(1.0, confidence)

    caution = round(cap * intensity / 100.0 * confidence, 2) if active else 0.0
    if manual and freshness in {"stale", "future_dated"}:
        data_status = "stale"
    elif pcr_imbalance is not None and roll_concentration is not None:
        data_status = "ok"
    else:
        data_status = "partial"

    if caution >= 10:
        execution_stance = "HIGH_CAUTION"
        tactics = ["split_entries", "prefer_limit_orders", "avoid_chasing", "consider_waiting_for_post_sq_price_discovery"]
    elif caution >= 6:
        execution_stance = "MODERATE_CAUTION"
        tactics = ["split_entries", "prefer_limit_orders", "allow_deeper_entry_levels"]
    elif caution >= 3:
        execution_stance = "MILD_CAUTION"
        tactics = ["prefer_limit_orders", "avoid_unnecessary_market_orders"]
    else:
        execution_stance = "NORMAL"
        tactics = ["no_sq_specific_change"]

    return {
        "version": "1.0",
        "enabled": True,
        "active": active,
        "as_of_date": as_of.isoformat(),
        "next_major_sq_date": sq_date.isoformat(),
        "days_to_sq": days_to_sq,
        "event_proximity_score": round(event_score, 2),
        "pressure_intensity_score": round(intensity, 2),
        "confidence": round(confidence, 3),
        "data_status": data_status,
        "manual_input_freshness": freshness,
        "manual_input_age_days": input_age,
        "execution_caution_points": caution,
        "caution_cap_points": cap,
        "execution_stance": execution_stance,
        "directional_bias": "UNDETERMINED",
        "price_structure": {
            "spot": spot_n,
            "put_wall": put_wall,
            "call_wall": call_wall,
            "magnet_strike": magnet,
            "nearest_reference_distance_pct": nearest_distance_pct,
        },
        "evidence": {
            "put_call_oi_ratio": pcr,
            "front_futures_share": front_share,
            "arbitrage_balance_zscore": arb_z,
            "nikkei_vi_percentile": vi_pct,
            "component_scores": {k: (round(v, 2) if v is not None else None) for k, v in raw_components.items()},
            "source_notes": manual.get("source_notes") if manual else None,
        },
        "policy_effects": {
            "alter_security_ranking": False,
            "alter_fundamental_score": False,
            "alter_investment_thesis": False,
            "use_for_execution_timing_only": True,
        },
        "tactics": tactics,
        "rule": "SQ is a short-lived market-structure overlay. Use it for staging and limit-order timing only; do not infer direction from open interest alone.",
    }
