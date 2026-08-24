from __future__ import annotations

import io
import time
from pathlib import Path

import pandas as pd
import requests

from .common import now_iso

BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
UA = "investment-quant/1.6.1 (+research)"
FRED_COLUMNS = [
    "series",
    "fred_id",
    "date",
    "value",
    "previous",
    "change",
    "source",
    "source_url",
    "fetched_at",
    "data_status",
    "stale_reason",
    "cache_reused_at",
]


def _get_with_retry(url, *, params=None, attempts=3):
    """Retry transient FRED/network failures without fabricating data."""
    last_error = None
    timeouts = (12, 20, 30)
    for i in range(attempts):
        try:
            r = requests.get(
                url,
                params=params,
                timeout=timeouts[min(i, len(timeouts) - 1)],
                headers={"User-Agent": UA, "Accept": "text/csv,*/*;q=0.8"},
            )
            r.raise_for_status()
            return r
        except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as exc:
            last_error = exc
            if i < attempts - 1:
                retry_after = getattr(getattr(exc, "response", None), "headers", {}).get(
                    "Retry-After"
                )
                try:
                    delay = min(float(retry_after), 10.0) if retry_after else 2 ** i
                except (TypeError, ValueError):
                    delay = 2 ** i
                time.sleep(delay)
    raise last_error if last_error else RuntimeError("FRED request failed")


def _load_cache(cache_path):
    if not cache_path:
        return pd.DataFrame(columns=FRED_COLUMNS)
    path = Path(cache_path)
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=FRED_COLUMNS)
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=FRED_COLUMNS)


def _cached_observation(cache, name, sid, max_cache_age_days):
    if cache is None or cache.empty or "series" not in cache.columns:
        return None, None
    x = cache[cache["series"].astype(str) == str(name)].copy()
    if "fred_id" in x.columns:
        exact = x[x["fred_id"].astype(str) == str(sid)]
        if not exact.empty:
            x = exact
    if x.empty or "value" not in x.columns:
        return None, None
    x["value"] = pd.to_numeric(x["value"], errors="coerce")
    x = x.dropna(subset=["value"])
    if x.empty:
        return None, None
    if "date" in x.columns:
        x["_sort_date"] = pd.to_datetime(x["date"], errors="coerce", utc=True)
        x = x.sort_values("_sort_date")
    row = x.iloc[-1].to_dict()

    age_days = None
    fetched_at = pd.to_datetime(row.get("fetched_at"), errors="coerce", utc=True)
    if pd.notna(fetched_at):
        age_days = (pd.Timestamp.now(tz="UTC") - fetched_at).total_seconds() / 86400
        if max_cache_age_days is not None and age_days > float(max_cache_age_days):
            return None, age_days
    elif max_cache_age_days is not None:
        # Unknown cache age cannot satisfy a bounded-freshness policy.
        return None, None
    return row, age_days


def _parse_response(text):
    df = pd.read_csv(io.StringIO(text))
    if "DATE" not in df.columns:
        raise ValueError("DATE column missing")
    value_cols = [c for c in df.columns if c != "DATE"]
    if not value_cols:
        raise ValueError("no value column")
    valcol = value_cols[0]
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df[valcol] = pd.to_numeric(df[valcol], errors="coerce")
    x = df.dropna(subset=["DATE", valcol])
    if x.empty:
        raise ValueError("no valid observations")
    return x, valcol


def fetch_fred(series: dict, cache_path=None, max_cache_age_days=14):
    """Fetch FRED series and expose cache fallback explicitly as stale.

    Cached observations are retained for audit/report continuity, but scoring ignores
    rows whose ``data_status`` is not ``ok``. Network success and payload validity are
    recorded separately in source health.
    """
    rows = []
    health = []
    fetched = now_iso()
    cache = _load_cache(cache_path)

    for name, sid in series.items():
        transport_status = "error"
        content_status = "not_checked"
        source_url = f"{BASE}?id={sid}"
        try:
            r = _get_with_retry(BASE, params={"id": sid}, attempts=3)
            transport_status = "ok"
            source_url = r.url
            x, valcol = _parse_response(r.text)
            content_status = "valid"
            latest = x.iloc[-1]
            prev = x.iloc[-2] if len(x) > 1 else latest
            rows.append(
                {
                    "series": name,
                    "fred_id": sid,
                    "date": str(latest["DATE"].date()),
                    "value": float(latest[valcol]),
                    "previous": float(prev[valcol]),
                    "change": float(latest[valcol] - prev[valcol]),
                    "source": "FRED",
                    "source_url": source_url,
                    "fetched_at": fetched,
                    "data_status": "ok",
                    "stale_reason": "",
                    "cache_reused_at": "",
                }
            )
            health.append(
                {
                    "source": f"FRED:{sid}",
                    "status": "ok",
                    "transport_status": transport_status,
                    "content_status": content_status,
                    "records": len(x),
                    "as_of_date": str(latest["DATE"].date()),
                    "fetched_at": fetched,
                    "error": "",
                    "source_tier": "primary",
                }
            )
        except Exception as exc:
            cached, cache_age_days = _cached_observation(
                cache, name, sid, max_cache_age_days
            )
            error = f"{type(exc).__name__}: {exc}"
            if cached is not None:
                cached_row = {c: cached.get(c, "") for c in FRED_COLUMNS}
                cached_row.update(
                    {
                        "series": name,
                        "fred_id": sid,
                        "source": "FRED",
                        "source_url": cached.get("source_url") or source_url,
                        "data_status": "stale",
                        "stale_reason": error,
                        "cache_reused_at": fetched,
                    }
                )
                rows.append(cached_row)
                health.append(
                    {
                        "source": f"FRED:{sid}",
                        "status": "stale",
                        "transport_status": transport_status,
                        "content_status": "cached_valid"
                        if transport_status == "error"
                        else "invalid_current_cached_valid",
                        "records": 1,
                        "as_of_date": str(cached.get("date", "")),
                        "fetched_at": fetched,
                        "cache_age_days": round(cache_age_days, 3)
                        if cache_age_days is not None
                        else None,
                        "error": error,
                        "source_tier": "primary",
                    }
                )
            else:
                overall = "partial" if transport_status == "ok" else "missing"
                health.append(
                    {
                        "source": f"FRED:{sid}",
                        "status": overall,
                        "transport_status": transport_status,
                        "content_status": "invalid"
                        if transport_status == "ok"
                        else content_status,
                        "records": 0,
                        "as_of_date": "",
                        "fetched_at": fetched,
                        "cache_age_days": round(cache_age_days, 3)
                        if cache_age_days is not None
                        else None,
                        "error": error,
                        "source_tier": "primary",
                    }
                )

    return pd.DataFrame(rows, columns=FRED_COLUMNS), health
