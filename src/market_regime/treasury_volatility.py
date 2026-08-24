from __future__ import annotations

import math
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from .common import clamp, load_json, now_iso


BASE = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml"
SOURCE_URL = "https://home.treasury.gov/treasury-daily-interest-rate-xml-feed"
UA = "investment-quant/1.6.2 (+research)"
TENOR_FIELDS = {
    "2Y": "BC_2YEAR",
    "5Y": "BC_5YEAR",
    "10Y": "BC_10YEAR",
    "30Y": "BC_30YEAR",
}


def _get_with_retry(year: int, attempts: int = 3):
    last_error = None
    for i, timeout in enumerate((12, 20, 30)[:attempts]):
        try:
            response = requests.get(
                BASE,
                params={
                    "data": "daily_treasury_yield_curve",
                    "field_tdr_date_value": str(year),
                },
                timeout=timeout,
                headers={"User-Agent": UA, "Accept": "application/xml,text/xml"},
            )
            response.raise_for_status()
            return response
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as exc:
            last_error = exc
            if i < attempts - 1:
                time.sleep(2**i)
    raise last_error if last_error else RuntimeError("U.S. Treasury request failed")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_treasury_xml(content: str | bytes) -> pd.DataFrame:
    """Parse the official Treasury Atom/XML feed without relying on prefix names."""
    root = ET.fromstring(content)
    rows = []
    for node in root.iter():
        if _local_name(node.tag) != "properties":
            continue
        values = {_local_name(child.tag): child.text for child in list(node)}
        date_raw = values.get("NEW_DATE") or values.get("Date")
        row = {"date": pd.to_datetime(date_raw, errors="coerce")}
        for tenor, field in TENOR_FIELDS.items():
            row[tenor] = pd.to_numeric(values.get(field), errors="coerce")
        rows.append(row)
    df = pd.DataFrame(rows, columns=["date", *TENOR_FIELDS])
    if df.empty:
        raise ValueError("no Treasury yield observations in XML payload")
    df = df.dropna(subset=["date"]).drop_duplicates("date", keep="last").sort_values("date")
    df = df.dropna(subset=list(TENOR_FIELDS), how="all")
    if df.empty:
        raise ValueError("Treasury XML has no usable yield values")
    return df.reset_index(drop=True)


def compute_treasury_volatility(
    yields: pd.DataFrame,
    *,
    window_days: int = 20,
    percentile_lookback_days: int = 252,
    minimum_observations: int = 60,
) -> tuple[dict, pd.DataFrame]:
    """Calculate a transparent realized-yield-volatility proxy.

    This is deliberately not an estimate of the proprietary ICE BofA MOVE Index.
    It uses the annualized standard deviation of daily yield changes across the
    2Y/5Y/10Y/30Y Treasury curve and is suitable only as market-state context.
    """
    required = ["date", *TENOR_FIELDS]
    missing = [c for c in required if c not in yields.columns]
    if missing:
        raise ValueError(f"missing Treasury columns: {missing}")
    df = yields[required].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for tenor in TENOR_FIELDS:
        df[tenor] = pd.to_numeric(df[tenor], errors="coerce")
    df = df.dropna(subset=["date"]).drop_duplicates("date", keep="last").sort_values("date")
    complete = df.dropna(subset=list(TENOR_FIELDS)).copy()
    if len(complete) < max(int(minimum_observations), int(window_days) + 1):
        raise ValueError(
            f"insufficient complete Treasury observations: {len(complete)}"
        )

    changes_bps = complete[list(TENOR_FIELDS)].diff() * 100.0
    rolling = changes_bps.rolling(int(window_days), min_periods=int(window_days)).std(ddof=1)
    rolling = rolling * math.sqrt(252.0)
    curve_proxy = (rolling.pow(2).mean(axis=1)).pow(0.5)
    latest_index = curve_proxy.last_valid_index()
    if latest_index is None:
        raise ValueError("Treasury volatility proxy could not be calculated")

    history = complete[["date"]].copy()
    for tenor in TENOR_FIELDS:
        history[f"{tenor.lower()}_realized_vol_20d_bps_ann"] = rolling[tenor]
    history["curve_realized_vol_20d_bps_ann"] = curve_proxy
    history = history.dropna(subset=["curve_realized_vol_20d_bps_ann"]).copy()
    lookback = history.tail(int(percentile_lookback_days))
    latest_curve = float(history.iloc[-1]["curve_realized_vol_20d_bps_ann"])
    percentile = float((lookback["curve_realized_vol_20d_bps_ann"] <= latest_curve).mean())
    latest_changes = changes_bps.loc[latest_index].dropna()
    latest_move_rms = float((latest_changes.pow(2).mean()) ** 0.5)

    latest = complete.loc[latest_index]
    five_back = complete.loc[:latest_index].tail(6).iloc[0]
    five_day_change = {
        tenor: round(float((latest[tenor] - five_back[tenor]) * 100.0), 3)
        for tenor in TENOR_FIELDS
    }
    tenor_vol = {
        tenor: round(float(rolling.loc[latest_index, tenor]), 3)
        for tenor in TENOR_FIELDS
    }
    stress_score = round(clamp(100.0 - 75.0 * percentile), 2)
    result = {
        "name": "UST_YIELD_VOLATILITY_PROXY",
        "label": "Treasury Volatility Proxy (not ICE MOVE)",
        "method_version": "1.0.0",
        "generated_at_utc": now_iso(),
        "as_of_date": str(pd.Timestamp(latest["date"]).date()),
        "data_status": "ok",
        "source": "U.S. Department of the Treasury",
        "source_url": SOURCE_URL,
        "is_ice_move": False,
        "method": "RMS of annualized 20-observation realized volatility of daily 2Y/5Y/10Y/30Y Treasury yield changes (basis points)",
        "window_observations": int(window_days),
        "percentile_lookback_observations": int(len(lookback)),
        "curve_realized_vol_20d_bps_ann": round(latest_curve, 3),
        "tenor_realized_vol_20d_bps_ann": tenor_vol,
        "latest_curve_move_bps_rms": round(latest_move_rms, 3),
        "five_observation_yield_change_bps": five_day_change,
        "percentile_rank": round(percentile, 4),
        "stress_score": stress_score,
        "interpretation": "Higher percentile means Treasury yields are moving more violently versus their own recent history; stress_score is calm=100, stressed=0.",
        "limitations": [
            "This is not ICE BofA MOVE and is not option-implied volatility.",
            "It does not include swaption prices, option skew, or tenor-specific option weights.",
            "Treasury observations are published with calendar and release-time lags.",
        ],
    }
    history["percentile_rank"] = history["curve_realized_vol_20d_bps_ann"].rolling(
        int(percentile_lookback_days), min_periods=1
    ).rank(pct=True)
    history["data_status"] = "ok"
    return result, history.tail(750).reset_index(drop=True)


def _load_cached_proxy(cache_path, max_cache_age_days: int):
    if not cache_path:
        return None
    cached = load_json(cache_path, {})
    if not cached or cached.get("data_status") not in {"ok", "stale"}:
        return None
    generated = pd.to_datetime(cached.get("generated_at_utc"), errors="coerce", utc=True)
    if pd.isna(generated):
        return None
    age_days = (pd.Timestamp.now(tz="UTC") - generated).total_seconds() / 86400.0
    if age_days > float(max_cache_age_days):
        return None
    return cached, age_days


def fetch_treasury_volatility(cfg: dict, cache_path=None):
    fetched = now_iso()
    current_year = datetime.now(timezone.utc).year
    frames = []
    urls = []
    try:
        for year in (current_year - 1, current_year):
            response = _get_with_retry(year)
            urls.append(getattr(response, "url", BASE))
            frames.append(parse_treasury_xml(response.content))
        yields = pd.concat(frames, ignore_index=True).drop_duplicates("date", keep="last")
        result, history = compute_treasury_volatility(
            yields,
            window_days=int(cfg.get("window_days", 20)),
            percentile_lookback_days=int(cfg.get("percentile_lookback_days", 252)),
            minimum_observations=int(cfg.get("minimum_observations", 60)),
        )
        health = [{
            "source": "USTreasury:daily_treasury_yield_curve",
            "status": "ok",
            "transport_status": "ok",
            "content_status": "valid",
            "records": len(yields),
            "as_of_date": result["as_of_date"],
            "fetched_at": fetched,
            "source_url": SOURCE_URL,
            "request_urls": urls,
            "error": "",
            "source_tier": "primary",
        }]
        return result, history, health
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        cached = _load_cached_proxy(
            cache_path, int(cfg.get("cache_max_age_days", 7))
        )
        if cached:
            result, age_days = cached
            result = dict(result)
            result.update({
                "data_status": "stale",
                "stale_reason": error,
                "cache_reused_at": fetched,
            })
            health = [{
                "source": "USTreasury:daily_treasury_yield_curve",
                "status": "stale",
                "transport_status": "error",
                "content_status": "cached_valid",
                "records": 1,
                "as_of_date": result.get("as_of_date", ""),
                "fetched_at": fetched,
                "cache_age_days": round(age_days, 3),
                "source_url": SOURCE_URL,
                "error": error,
                "source_tier": "primary",
            }]
            return result, pd.DataFrame(), health
        result = {
            "name": "UST_YIELD_VOLATILITY_PROXY",
            "label": "Treasury Volatility Proxy (not ICE MOVE)",
            "generated_at_utc": fetched,
            "data_status": "missing",
            "source": "U.S. Department of the Treasury",
            "source_url": SOURCE_URL,
            "is_ice_move": False,
            "error": error,
        }
        health = [{
            "source": "USTreasury:daily_treasury_yield_curve",
            "status": "missing",
            "transport_status": "error",
            "content_status": "not_checked",
            "records": 0,
            "as_of_date": "",
            "fetched_at": fetched,
            "source_url": SOURCE_URL,
            "error": error,
            "source_tier": "primary",
        }]
        return result, pd.DataFrame(), health
