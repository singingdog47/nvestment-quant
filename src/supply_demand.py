from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd


JST = timezone(timedelta(hours=9))
DEFAULT_CONFIG_PATH = "config/supply_demand_v1.json"

OUTPUT_COLUMNS = [
    "observed_date",
    "generated_at_utc",
    "market",
    "code",
    "ticker",
    "name",
    "target_source",
    "data_status",
    "confidence",
    "free_float_ratio",
    "free_float_shares",
    "shares_outstanding",
    "float_market_cap",
    "current_price",
    "avg_volume_30d",
    "current_volume",
    "avg_turnover_30d",
    "current_turnover",
    "one_day_capacity_at_participation_rate",
    "current_volume_ratio_30d",
    "avg_daily_float_turnover_ratio",
    "current_float_turnover_ratio",
    "short_percent_float",
    "shares_short",
    "shares_short_prior_month",
    "short_interest_change_ratio",
    "days_to_cover",
    "held_percent_insiders",
    "held_percent_institutions",
    "daily_change_pct",
    "free_float_source",
    "free_float_source_tier",
    "liquidity_source",
    "short_source",
    "source_url",
    "source_retrieved_at",
    "short_interest_as_of",
    "price_as_of",
    "context_flags",
    "data_quality_flags",
]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _text(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value).strip()


def _number(value: Any) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _positive(value: Any) -> float | None:
    number = _number(value)
    return number if number is not None and number > 0 else None


def _ratio(value: Any) -> float | None:
    """Normalize explicit ratio inputs while preserving missing values.

    Public feeds normally return ratios as decimals.  Manually supplied values
    sometimes use percentage points, so values in (1, 100] are converted.  No
    value is inferred from a peer, market-cap bucket, or previous observation.
    """

    number = _number(value)
    if number is None:
        return None
    if 1 < abs(number) <= 100:
        number /= 100.0
    return number


def _first_number(row: pd.Series | dict[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = _number(row.get(key))
        if value is not None:
            return value
    return None


def _first_text(row: pd.Series | dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = _text(row.get(key))
        if value:
            return value
    return ""


def _timestamp(value: Any) -> str:
    text = _text(value)
    if not text:
        return ""
    number = _number(value)
    if number is not None and number > 100_000_000:
        try:
            return datetime.fromtimestamp(number, timezone.utc).isoformat(timespec="seconds")
        except (ValueError, OSError, OverflowError):
            return ""
    try:
        return pd.Timestamp(text).isoformat()
    except (TypeError, ValueError):
        return text


def _normal_code(value: Any) -> str:
    text = _text(value).upper()
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    if text.endswith(".T") and text[:-2].isdigit():
        return text[:-2]
    return text


def _row_keys(row: pd.Series | dict[str, Any]) -> list[str]:
    market = _first_text(row, "market").upper()
    code = _normal_code(row.get("code"))
    ticker = _first_text(row, "ticker").upper()
    keys = []
    if code:
        keys.append(f"{market}|C|{code}")
    if ticker:
        keys.append(f"{market}|T|{ticker}")
    return keys


def _manual_lookup(manual: pd.DataFrame | None) -> dict[str, dict[str, Any]]:
    if manual is None or manual.empty:
        return {}
    result: dict[str, dict[str, Any]] = {}
    # Last row wins so a newer correction can supersede an earlier row in the
    # same explicitly managed file.
    for _, row in manual.iterrows():
        record = row.to_dict()
        for key in _row_keys(record):
            result[key] = record
    return result


def _manual_row(row: pd.Series, lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    for key in _row_keys(row):
        if key in lookup:
            return lookup[key]
    return {}


def _manual_number(manual: dict[str, Any], key: str) -> float | None:
    return _number(manual.get(key)) if manual else None


def _pick_number(manual: dict[str, Any], manual_key: str, row: pd.Series, *snapshot_keys: str) -> tuple[float | None, bool]:
    manual_value = _manual_number(manual, manual_key)
    if manual_value is not None:
        return manual_value, True
    return _first_number(row, *snapshot_keys), False


def _age_days(value: Any, reference: datetime) -> int | None:
    text = _text(value)
    if not text:
        return None
    try:
        stamp = pd.Timestamp(text)
        if stamp.tzinfo is None:
            stamp = stamp.tz_localize(JST)
        return (reference.astimezone(JST).date() - stamp.tz_convert(JST).date()).days
    except (TypeError, ValueError):
        return None


def _has_manual_values(row: dict[str, Any], keys: tuple[str, ...]) -> bool:
    return any(_number(row.get(key)) is not None for key in keys)


def _validated_positive(value: Any, flag: str, quality_flags: list[str]) -> float | None:
    number = _number(value)
    if number is None:
        return None
    if number <= 0:
        quality_flags.append(flag)
        return None
    return number


def _validated_nonnegative(value: Any, flag: str, quality_flags: list[str]) -> float | None:
    number = _number(value)
    if number is None:
        return None
    if number < 0:
        quality_flags.append(flag)
        return None
    return number


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_json_safe(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if not isinstance(value, (str, bytes)):
        try:
            if pd.isna(value):
                return None
        except (TypeError, ValueError):
            pass
    return value


def load_config(root: str | Path = ".", path: str = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    config_path = Path(root) / path
    return json.loads(config_path.read_text(encoding="utf-8"))


def compute_supply_demand(
    snapshot: pd.DataFrame,
    config: dict[str, Any],
    manual: pd.DataFrame | None = None,
    generated_at: datetime | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    generated_at = generated_at or _now_utc()
    if generated_at.tzinfo is None:
        generated_at = generated_at.replace(tzinfo=timezone.utc)
    generated_iso = generated_at.astimezone(timezone.utc).isoformat(timespec="seconds")
    observed_date = generated_at.astimezone(JST).date().isoformat()
    thresholds = config.get("thresholds") or {}
    freshness = config.get("freshness") or {}
    governance = config.get("governance") or {}
    lookup = _manual_lookup(manual)
    records: list[dict[str, Any]] = []

    for _, row in snapshot.iterrows():
        manual_row = _manual_row(row, lookup)
        manual_as_of = _first_text(manual_row, "as_of_date") if manual_row else ""
        manual_source = _first_text(manual_row, "source_name") if manual_row else ""
        manual_url = _first_text(manual_row, "source_url") if manual_row else ""
        manual_tier = (_first_text(manual_row, "source_tier") or "unverified").lower() if manual_row else ""
        quality_flags: list[str] = []
        manual_age = _age_days(manual_as_of, generated_at) if manual_row else None
        float_fields = (
            "shares_outstanding",
            "free_float_shares",
            "free_float_ratio",
            "held_percent_insiders",
            "held_percent_institutions",
        )
        short_fields = (
            "shares_short",
            "shares_short_prior_month",
            "short_percent_float",
            "days_to_cover",
        )
        market_fields = ("avg_volume_30d", "current_volume", "current_price", "daily_change_pct")
        has_manual_float = _has_manual_values(manual_row, float_fields)
        has_manual_short = _has_manual_values(manual_row, short_fields)
        has_manual_market = _has_manual_values(manual_row, market_fields)
        if manual_row and (has_manual_float or has_manual_short or has_manual_market) and manual_age is None:
            quality_flags.append("MANUAL_AS_OF_MISSING_OR_INVALID")
        if manual_age is not None and manual_age < -1:
            quality_flags.append("MANUAL_AS_OF_IN_FUTURE")

        def fresh_manual(group: str, has_values: bool) -> dict[str, Any]:
            if not has_values or manual_age is None or manual_age < -1:
                return {}
            default_max_age = {"float": 400, "short": 45, "market": 7}[group]
            max_age = int(freshness.get(f"manual_{group}_max_age_days", default_max_age))
            if manual_age > max_age:
                quality_flags.append(f"STALE_MANUAL_{group.upper()}_DATA")
                return {}
            return manual_row

        manual_float_row = fresh_manual("float", has_manual_float)
        manual_short_row = fresh_manual("short", has_manual_short)
        manual_market_row = fresh_manual("market", has_manual_market)

        shares_outstanding, shares_out_manual = _pick_number(
            manual_float_row, "shares_outstanding", row, "yf_shares_outstanding"
        )
        free_float_shares, float_shares_manual = _pick_number(
            manual_float_row, "free_float_shares", row, "yf_float_shares"
        )
        shares_outstanding = _validated_positive(
            shares_outstanding, "INVALID_SHARES_OUTSTANDING", quality_flags
        )
        free_float_shares = _validated_positive(
            free_float_shares, "INVALID_FREE_FLOAT_SHARES", quality_flags
        )
        direct_ratio = _ratio(manual_float_row.get("free_float_ratio")) if manual_float_row else None
        direct_ratio_manual = direct_ratio is not None
        calculated_ratio = None
        if _positive(free_float_shares) is not None and _positive(shares_outstanding) is not None:
            calculated_ratio = free_float_shares / shares_outstanding
        free_float_ratio = direct_ratio if direct_ratio is not None else calculated_ratio

        if free_float_ratio is not None and not 0 < free_float_ratio <= 1:
            quality_flags.append("INVALID_FREE_FLOAT_RATIO")
            free_float_ratio = None
        if direct_ratio is not None and calculated_ratio is not None and 0 < direct_ratio <= 1:
            if abs(direct_ratio - calculated_ratio) > max(0.02, calculated_ratio * 0.10):
                quality_flags.append("FREE_FLOAT_SOURCE_CONFLICT")

        # Deriving shares from two supplied values is deterministic; no peer or
        # historical imputation is used.
        if direct_ratio_manual and not float_shares_manual and _positive(shares_outstanding) is not None:
            free_float_shares = free_float_ratio * shares_outstanding if free_float_ratio is not None else None
        elif free_float_shares is None and free_float_ratio is not None and _positive(shares_outstanding) is not None:
            free_float_shares = free_float_ratio * shares_outstanding

        current_price, price_manual = _pick_number(
            manual_market_row, "current_price", row, "yf_price", "price"
        )
        market_cap = _first_number(row, "yf_market_cap", "market_cap")
        avg_volume, avg_volume_manual = _pick_number(
            manual_market_row, "avg_volume_30d", row, "yf_average_volume", "avg_volume_30d"
        )
        current_volume, current_volume_manual = _pick_number(
            manual_market_row, "current_volume", row, "yf_regular_market_volume", "volume"
        )
        current_price = _validated_positive(
            current_price, "INVALID_CURRENT_PRICE", quality_flags
        )
        market_cap = _validated_positive(
            market_cap, "INVALID_MARKET_CAP", quality_flags
        )
        avg_volume = _validated_positive(
            avg_volume, "INVALID_AVERAGE_VOLUME", quality_flags
        )
        current_volume = _validated_nonnegative(
            current_volume, "INVALID_CURRENT_VOLUME", quality_flags
        )
        avg_turnover = _first_number(row, "avg_turnover_30d")
        avg_turnover = _validated_positive(
            avg_turnover, "INVALID_AVERAGE_TURNOVER", quality_flags
        )
        if avg_turnover is None and _positive(avg_volume) is not None and _positive(current_price) is not None:
            avg_turnover = avg_volume * current_price
        current_turnover = (
            current_volume * current_price
            if _positive(current_volume) is not None and _positive(current_price) is not None
            else None
        )
        participation_rate = float(thresholds.get("execution_participation_rate", 0.10))
        one_day_capacity = avg_turnover * participation_rate if _positive(avg_turnover) is not None else None

        shares_short, shares_short_manual = _pick_number(
            manual_short_row, "shares_short", row, "yf_shares_short"
        )
        shares_short = _validated_nonnegative(
            shares_short, "INVALID_SHARES_SHORT", quality_flags
        )
        shares_short_prior, shares_short_prior_manual = _pick_number(
            manual_short_row,
            "shares_short_prior_month",
            row,
            "yf_shares_short_prior_month",
        )
        shares_short_prior = _validated_nonnegative(
            shares_short_prior, "INVALID_PRIOR_SHARES_SHORT", quality_flags
        )
        short_interest_change = (
            shares_short / shares_short_prior - 1.0
            if shares_short is not None and _positive(shares_short_prior) is not None
            else None
        )
        direct_short = _ratio(manual_short_row.get("short_percent_float")) if manual_short_row else None
        short_pct_manual = direct_short is not None
        if direct_short is None:
            direct_short = _ratio(row.get("yf_short_percent_float"))
        short_percent_float = direct_short
        if short_percent_float is None and _positive(shares_short) is not None and _positive(free_float_shares) is not None:
            short_percent_float = shares_short / free_float_shares
        if short_percent_float is not None and not 0 <= short_percent_float <= 1:
            quality_flags.append("INVALID_SHORT_PERCENT_FLOAT")
            short_percent_float = None

        days_to_cover, days_manual = _pick_number(
            manual_short_row, "days_to_cover", row, "yf_short_ratio_days"
        )
        if days_to_cover is None and _positive(shares_short) is not None and _positive(avg_volume) is not None:
            days_to_cover = shares_short / avg_volume
        if days_to_cover is not None and days_to_cover < 0:
            quality_flags.append("INVALID_DAYS_TO_COVER")
            days_to_cover = None

        insiders_raw, insiders_manual = _pick_number(
            manual_float_row, "held_percent_insiders", row, "yf_held_percent_insiders"
        )
        institutions_raw, institutions_manual = _pick_number(
            manual_float_row, "held_percent_institutions", row, "yf_held_percent_institutions"
        )
        held_percent_insiders = _ratio(insiders_raw)
        held_percent_institutions = _ratio(institutions_raw)
        if held_percent_insiders is not None and not 0 <= held_percent_insiders <= 1:
            quality_flags.append("INVALID_HELD_PERCENT_INSIDERS")
            held_percent_insiders = None
        if held_percent_institutions is not None and not 0 <= held_percent_institutions <= 1:
            quality_flags.append("INVALID_HELD_PERCENT_INSTITUTIONS")
            held_percent_institutions = None

        if manual_market_row and _number(manual_market_row.get("daily_change_pct")) is not None:
            daily_change_pct = _ratio(manual_market_row.get("daily_change_pct"))
            change_manual = True
        else:
            # Yahoo reports regularMarketChangePercent in percentage points.
            raw_change = _number(row.get("yf_regular_market_change_pct"))
            daily_change_pct = raw_change / 100.0 if raw_change is not None else None
            change_manual = False

        volume_ratio = None
        if _positive(current_volume) is not None and _positive(avg_volume) is not None:
            volume_ratio = current_volume / avg_volume
        avg_float_turnover = None
        current_float_turnover = None
        if _positive(free_float_shares) is not None:
            if _positive(avg_volume) is not None:
                avg_float_turnover = avg_volume / free_float_shares
            if _positive(current_volume) is not None:
                current_float_turnover = current_volume / free_float_shares
        float_market_cap = (
            market_cap * free_float_ratio
            if _positive(market_cap) is not None and free_float_ratio is not None
            else None
        )

        tight_threshold = float(thresholds.get("tight_free_float_ratio", 0.30))
        turnover_threshold = float(thresholds.get("high_average_float_turnover_ratio", 0.02))
        short_threshold = float(thresholds.get("crowded_short_percent_float", 0.10))
        cover_threshold = float(thresholds.get("high_days_to_cover", 5.0))
        short_change_threshold = float(
            thresholds.get("material_short_interest_change_ratio", 0.20)
        )
        volume_threshold = float(thresholds.get("volume_expansion_ratio", 1.50))
        move_threshold = float(thresholds.get("material_daily_move", 0.02))

        context_flags: list[str] = []
        if free_float_ratio is not None and free_float_ratio <= tight_threshold:
            context_flags.append("TIGHT_FLOAT")
        if avg_float_turnover is not None and avg_float_turnover >= turnover_threshold:
            context_flags.append("HIGH_FLOAT_TURNOVER")
        short_crowded = (
            (short_percent_float is not None and short_percent_float >= short_threshold)
            or (days_to_cover is not None and days_to_cover >= cover_threshold)
        )
        if short_crowded:
            context_flags.append("SHORT_CROWDING")
        if short_interest_change is not None and short_interest_change >= short_change_threshold:
            context_flags.append("SHORT_INTEREST_RISING")
        elif short_interest_change is not None and short_interest_change <= -short_change_threshold:
            context_flags.append("SHORT_INTEREST_FALLING")
        volume_expanded = volume_ratio is not None and volume_ratio >= volume_threshold
        if volume_expanded:
            context_flags.append("VOLUME_EXPANSION")
        if volume_expanded and daily_change_pct is not None and daily_change_pct >= move_threshold:
            context_flags.append("PRICE_UP_ON_VOLUME_EXPANSION")
            if short_crowded:
                context_flags.append("POTENTIAL_SHORT_SQUEEZE_CONTEXT")
        elif volume_expanded and daily_change_pct is not None and daily_change_pct <= -move_threshold:
            context_flags.append("PRICE_DOWN_ON_VOLUME_EXPANSION")
        if "TIGHT_FLOAT" in context_flags and "HIGH_FLOAT_TURNOVER" in context_flags:
            context_flags.append("TIGHT_FLOAT_HIGH_TURNOVER")
        if not context_flags:
            context_flags.append("NO_EXCEPTION")

        float_manual = shares_out_manual or float_shares_manual or direct_ratio_manual
        liquidity_manual = avg_volume_manual or current_volume_manual or price_manual or change_manual
        short_manual = (
            shares_short_manual
            or shares_short_prior_manual
            or short_pct_manual
            or days_manual
        )
        ownership_manual = insiders_manual or institutions_manual
        if (float_manual or liquidity_manual or short_manual or ownership_manual) and not manual_source:
            quality_flags.append("MANUAL_SOURCE_NAME_MISSING")
        yahoo_url = f"https://finance.yahoo.com/quote/{_first_text(row, 'ticker')}" if _first_text(row, "ticker") else ""
        float_source = manual_source if float_manual else ("Yahoo Finance via yfinance" if free_float_ratio is not None else "")
        float_tier = manual_tier if float_manual else ("secondary" if free_float_ratio is not None else "missing")
        liquidity_source = manual_source if liquidity_manual else (
            "Yahoo Finance via yfinance"
            if _first_number(row, "yf_average_volume", "yf_regular_market_volume") is not None
            else ("screening snapshot" if avg_volume is not None or current_volume is not None else "")
        )
        short_source = manual_source if short_manual else ("Yahoo Finance via yfinance" if short_percent_float is not None or days_to_cover is not None else "")
        source_url = manual_url if (float_manual or liquidity_manual or short_manual or ownership_manual) and manual_url else yahoo_url

        has_float = free_float_ratio is not None
        has_liquidity = avg_volume is not None or current_volume is not None
        has_short = (
            short_percent_float is not None
            or days_to_cover is not None
            or short_interest_change is not None
        )
        if has_float and _positive(avg_volume) is not None:
            data_status = "ok"
        elif has_float or has_liquidity or has_short:
            data_status = "partial"
        else:
            data_status = "missing"
        if any(flag.startswith("INVALID_") for flag in quality_flags) and data_status == "ok":
            data_status = "partial"

        if data_status == "missing":
            confidence = 0.0
        elif float_tier == "primary" and data_status == "ok":
            confidence = 0.90
        elif data_status == "ok":
            confidence = 0.70
        else:
            confidence = 0.40
        if any(flag.startswith("INVALID_") for flag in quality_flags):
            confidence = min(confidence, 0.35)
        elif "FREE_FLOAT_SOURCE_CONFLICT" in quality_flags:
            # A dated primary override still wins, but disagreement with the
            # secondary observation is visible and modestly reduces confidence.
            confidence = min(confidence, 0.80)

        source_retrieved_at = manual_as_of if float_manual else _first_text(row, "fetched_at", "data_retrieved_at_utc")
        short_interest_as_of = (
            _first_text(manual_short_row, "short_interest_date")
            if short_manual
            else _timestamp(row.get("yf_short_interest_date"))
        )
        price_as_of = (
            manual_as_of
            if price_manual or change_manual
            else (_timestamp(row.get("yf_regular_market_time")) or _first_text(row, "price_date"))
        )

        records.append(
            {
                "observed_date": observed_date,
                "generated_at_utc": generated_iso,
                "market": _first_text(row, "market").upper(),
                "code": _normal_code(row.get("code")),
                "ticker": _first_text(row, "ticker").upper(),
                "name": _first_text(row, "name", "name_screen"),
                "target_source": _first_text(row, "source"),
                "data_status": data_status,
                "confidence": confidence,
                "free_float_ratio": free_float_ratio,
                "free_float_shares": free_float_shares,
                "shares_outstanding": shares_outstanding,
                "float_market_cap": float_market_cap,
                "current_price": current_price,
                "avg_volume_30d": avg_volume,
                "current_volume": current_volume,
                "avg_turnover_30d": avg_turnover,
                "current_turnover": current_turnover,
                "one_day_capacity_at_participation_rate": one_day_capacity,
                "current_volume_ratio_30d": volume_ratio,
                "avg_daily_float_turnover_ratio": avg_float_turnover,
                "current_float_turnover_ratio": current_float_turnover,
                "short_percent_float": short_percent_float,
                "shares_short": shares_short,
                "shares_short_prior_month": shares_short_prior,
                "short_interest_change_ratio": short_interest_change,
                "days_to_cover": days_to_cover,
                "held_percent_insiders": held_percent_insiders,
                "held_percent_institutions": held_percent_institutions,
                "daily_change_pct": daily_change_pct,
                "free_float_source": float_source,
                "free_float_source_tier": float_tier,
                "liquidity_source": liquidity_source,
                "short_source": short_source,
                "source_url": source_url,
                "source_retrieved_at": source_retrieved_at,
                "short_interest_as_of": short_interest_as_of,
                "price_as_of": price_as_of,
                "context_flags": "|".join(context_flags),
                "data_quality_flags": "|".join(quality_flags),
            }
        )

    latest = pd.DataFrame(records, columns=OUTPUT_COLUMNS)
    total = len(latest)
    status_counts = latest["data_status"].value_counts().to_dict() if total else {}
    float_count = int(latest["free_float_ratio"].notna().sum()) if total else 0
    short_count = int(
        (
            latest["short_percent_float"].notna()
            | latest["days_to_cover"].notna()
            | latest["short_interest_change_ratio"].notna()
        ).sum()
    ) if total else 0
    volume_count = int(latest["current_volume_ratio_30d"].notna().sum()) if total else 0
    notable = latest[
        ~latest["context_flags"].isin(["NO_EXCEPTION", ""])
    ].copy() if total else latest.copy()
    if not notable.empty:
        notable["_priority"] = notable["context_flags"].map(
            lambda value: sum(
                flag in str(value)
                for flag in (
                    "POTENTIAL_SHORT_SQUEEZE_CONTEXT",
                    "PRICE_DOWN_ON_VOLUME_EXPANSION",
                    "TIGHT_FLOAT_HIGH_TURNOVER",
                    "SHORT_CROWDING",
                )
            )
        )
        notable = notable.sort_values(["_priority", "confidence"], ascending=False).head(10)

    if total == 0 or not status_counts:
        overall_status = "missing"
    elif status_counts.get("missing", 0) == 0 and status_counts.get("partial", 0) == 0:
        overall_status = "ok"
    else:
        overall_status = "partial"

    notable_fields = [
        "market",
        "code",
        "ticker",
        "name",
        "data_status",
        "confidence",
        "free_float_ratio",
        "avg_daily_float_turnover_ratio",
        "current_volume_ratio_30d",
        "short_percent_float",
        "short_interest_change_ratio",
        "days_to_cover",
        "context_flags",
    ]
    summary = {
        "version": config.get("version", "1.0.0"),
        "generated_at_utc": generated_iso,
        "observed_date_jst": observed_date,
        "data_status": overall_status,
        "target_scope": "public watchlist plus screening leaders; private portfolio excluded",
        "target_count": total,
        "status_counts": {
            "ok": int(status_counts.get("ok", 0)),
            "partial": int(status_counts.get("partial", 0)),
            "missing": int(status_counts.get("missing", 0)),
        },
        "coverage": {
            "free_float_ratio": float_count / total if total else 0.0,
            "short_interest": short_count / total if total else 0.0,
            "current_vs_average_volume": volume_count / total if total else 0.0,
        },
        "notable_contexts": [
            _json_safe(record)
            for record in notable[notable_fields].to_dict(orient="records")
        ] if not notable.empty else [],
        "thresholds": thresholds,
        "governance": governance,
        "interpretation": [
            "This layer is monitoring and execution context, not an alpha score or buy/sell signal.",
            "Free-float figures from Yahoo Finance are secondary-source observations unless a dated manual primary-source record overrides them.",
            "High volume plus a price move describes co-movement only; it does not identify accumulation, distribution, or causality.",
            "Missing free-float and short-interest values remain missing and are not carried forward.",
        ],
    }
    return latest, summary


def update_history(
    latest: pd.DataFrame,
    history_path: str | Path,
    retention_days: int = 400,
    observed_date: str | None = None,
) -> pd.DataFrame:
    history_path = Path(history_path)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    if history_path.exists():
        try:
            prior = pd.read_csv(history_path, dtype=str, low_memory=False)
        except Exception:
            prior = pd.DataFrame(columns=OUTPUT_COLUMNS)
    else:
        prior = pd.DataFrame(columns=OUTPUT_COLUMNS)
    if prior.empty:
        combined = latest.copy()
    elif latest.empty:
        combined = prior.copy()
    else:
        combined = pd.concat([prior, latest], ignore_index=True, sort=False)
    for column in OUTPUT_COLUMNS:
        if column not in combined:
            combined[column] = pd.NA
    if not combined.empty:
        combined = combined.drop_duplicates(
            ["observed_date", "market", "code", "ticker"], keep="last"
        )
        anchor = pd.Timestamp(observed_date or datetime.now(JST).date().isoformat())
        dates = pd.to_datetime(combined["observed_date"], errors="coerce")
        keep = dates.isna() | dates.ge(anchor - timedelta(days=int(retention_days)))
        combined = combined.loc[keep].sort_values(
            ["observed_date", "market", "code", "ticker"]
        )
    combined = combined[OUTPUT_COLUMNS]
    combined.to_csv(history_path, index=False, encoding="utf-8-sig")
    return combined


def _format_pct(value: Any) -> str:
    number = _number(value)
    return "missing" if number is None else f"{number * 100:.1f}%"


def _write_summary_markdown(summary: dict[str, Any], path: Path) -> None:
    coverage = summary.get("coverage") or {}
    counts = summary.get("status_counts") or {}
    input_health = summary.get("input_health") or {}
    lines = [
        "# Supply / Demand Context v1.0",
        "",
        f"Generated (UTC): {summary.get('generated_at_utc', 'unknown')}",
        f"Data status: **{summary.get('data_status', 'missing')}**",
        f"Scope: {summary.get('target_scope', 'unknown')}",
        "",
        "## Coverage",
        "",
        f"- Targets: {summary.get('target_count', 0)}",
        f"- Status: ok={counts.get('ok', 0)}, partial={counts.get('partial', 0)}, missing={counts.get('missing', 0)}",
        f"- Free-float ratio: {_format_pct(coverage.get('free_float_ratio'))}",
        f"- Short-interest context: {_format_pct(coverage.get('short_interest'))}",
        f"- Current/average volume: {_format_pct(coverage.get('current_vs_average_volume'))}",
        f"- Company snapshot input: {(input_health.get('company_snapshot') or {}).get('status', 'unknown')}",
        f"- Manual override input: {(input_health.get('manual_override') or {}).get('status', 'not_provided')}",
        "",
        "## Notable contexts",
        "",
    ]
    notable = summary.get("notable_contexts") or []
    if not notable:
        lines.append("- No exception context was detected, or the required data is missing.")
    else:
        for item in notable:
            label = item.get("name") or item.get("ticker") or item.get("code") or "unknown"
            lines.append(
                f"- [{item.get('market', '?')}] {label}: {item.get('context_flags', 'NO_EXCEPTION')} "
                f"(float={_format_pct(item.get('free_float_ratio'))}, "
                f"float turnover={_format_pct(item.get('avg_daily_float_turnover_ratio'))}, "
                f"volume ratio={item.get('current_volume_ratio_30d', 'missing')})"
            )
    lines += [
        "",
        "## Governance",
        "",
        "- This context does not change security ranking, fundamental score, or investment thesis.",
        "- It may be used only for monitoring, execution caution, and liquidity due diligence.",
        "- Missing values are not imputed or carried forward.",
        "- Volume/price co-movement is not labelled as accumulation or distribution.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _embed_decision_context(root: Path, summary: dict[str, Any]) -> None:
    for relative in (
        "data/decision_context_latest.json",
        "data/intelligence/decision_context_latest.json",
    ):
        path = root / relative
        if not path.exists():
            continue
        try:
            context = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(context, dict):
                continue
            context["supply_demand_context"] = _json_safe(summary)
            path.write_text(
                json.dumps(context, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception:
            # The standalone outputs remain authoritative.  A malformed
            # upstream context file must not erase or fabricate observations.
            continue


def run(root: str | Path = ".") -> tuple[Path, Path, Path]:
    root = Path(root)
    config = load_config(root)
    inputs = config.get("inputs") or {}
    outputs = config.get("outputs") or {}
    snapshot_path = root / inputs.get("company_snapshot", "data/intelligence/company_snapshot_latest.csv")
    manual_path = inputs.get("manual_override", "config/supply_demand_manual.csv")
    manual_path = root / manual_path
    snapshot_error = ""
    if not snapshot_path.exists():
        snapshot = pd.DataFrame(columns=["market", "code", "ticker", "name", "source"])
        snapshot_status = "missing"
    else:
        try:
            snapshot = pd.read_csv(snapshot_path, dtype=str, low_memory=False)
            snapshot_status = "ok"
        except Exception as exc:
            snapshot = pd.DataFrame(columns=["market", "code", "ticker", "name", "source"])
            snapshot_status = "error"
            snapshot_error = f"{type(exc).__name__}: {exc}"[:500]

    manual_error = ""
    if not manual_path.exists():
        manual = None
        manual_status = "not_provided"
    else:
        try:
            manual = pd.read_csv(manual_path, dtype=str, low_memory=False)
            manual_status = "ok" if not manual.empty else "empty"
        except Exception as exc:
            manual = None
            manual_status = "error"
            manual_error = f"{type(exc).__name__}: {exc}"[:500]

    latest, summary = compute_supply_demand(snapshot, config, manual)
    summary["input_health"] = {
        "company_snapshot": {
            "path": str(snapshot_path.relative_to(root)),
            "status": snapshot_status,
            "rows": len(snapshot),
            "error": snapshot_error,
        },
        "manual_override": {
            "path": str(manual_path.relative_to(root)),
            "status": manual_status,
            "rows": 0 if manual is None else len(manual),
            "error": manual_error,
        },
    }
    output_dir = root / outputs.get("directory", "data/supply_demand")
    output_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_dir / outputs.get("latest_csv", "supply_demand_latest.csv")
    summary_path = output_dir / outputs.get("summary_json", "supply_demand_summary_latest.json")
    markdown_path = output_dir / outputs.get("summary_markdown", "supply_demand_summary_latest.md")
    history_path = output_dir / outputs.get("history_csv", "supply_demand_history.csv")
    latest.to_csv(latest_path, index=False, encoding="utf-8-sig")
    summary_path.write_text(
        json.dumps(_json_safe(summary), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_summary_markdown(summary, markdown_path)
    _embed_decision_context(root, summary)
    update_history(
        latest,
        history_path,
        int(outputs.get("history_retention_days", 400)),
        summary.get("observed_date_jst"),
    )
    return latest_path, summary_path, markdown_path


def main() -> None:
    latest, summary, markdown = run(".")
    print(
        json.dumps(
            {
                "supply_demand_latest": str(latest),
                "supply_demand_summary": str(summary),
                "supply_demand_markdown": str(markdown),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
