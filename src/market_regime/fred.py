from __future__ import annotations

import io
import os
import re
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .common import now_iso

BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
API_BASE = "https://api.stlouisfed.org/fred/series/observations"
SERIES_PAGE = "https://fred.stlouisfed.org/series/{sid}"
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


class FredOfficialFetchError(RuntimeError):
    def __init__(self, message, *, transport_ok=False):
        super().__init__(message)
        self.transport_ok = transport_ok


def _get_with_retry(url, *, params=None, attempts=3, accept="text/csv,*/*;q=0.8"):
    """Retry transient FRED/network failures without fabricating data."""
    last_error = None
    timeouts = (12, 20, 30)
    for i in range(attempts):
        try:
            r = requests.get(
                url,
                params=params,
                timeout=timeouts[min(i, len(timeouts) - 1)],
                headers={"User-Agent": UA, "Accept": accept},
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
    date_col = next(
        (c for c in ("DATE", "observation_date", "date") if c in df.columns),
        None,
    )
    if date_col is None:
        raise ValueError("DATE column missing")
    value_cols = [c for c in df.columns if c != date_col]
    if not value_cols:
        raise ValueError("no value column")
    valcol = value_cols[0]
    df["DATE"] = pd.to_datetime(df[date_col], errors="coerce")
    df[valcol] = pd.to_numeric(df[valcol], errors="coerce")
    x = df.dropna(subset=["DATE", valcol])
    if x.empty:
        raise ValueError("no valid observations")
    return x, valcol


def _parse_api_response(payload, sid):
    observations = payload.get("observations") if isinstance(payload, dict) else None
    if not isinstance(observations, list):
        raise ValueError("FRED API observations missing")
    frame = pd.DataFrame(observations)
    if frame.empty or "date" not in frame or "value" not in frame:
        raise ValueError("FRED API observation columns missing")
    frame["DATE"] = pd.to_datetime(frame["date"], errors="coerce")
    frame[sid] = pd.to_numeric(frame["value"], errors="coerce")
    valid = frame[["DATE", sid]].dropna().sort_values("DATE")
    if valid.empty:
        raise ValueError("FRED API has no valid observations")
    return valid, sid


def _parse_series_page(text, sid):
    """Parse explicit recent observations from an official FRED series page."""
    plain = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
    matches = re.findall(
        r"\b(\d{4}-\d{2}-\d{2})\s*:\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\b",
        plain,
    )
    if not matches:
        raise ValueError("official FRED series page has no date/value observations")
    frame = pd.DataFrame(matches, columns=["DATE", sid])
    frame["DATE"] = pd.to_datetime(frame["DATE"], errors="coerce")
    frame[sid] = pd.to_numeric(frame[sid], errors="coerce")
    frame = frame.dropna().drop_duplicates("DATE").sort_values("DATE")
    if frame.empty:
        raise ValueError("official FRED series page observations invalid")
    return frame, sid


def _fetch_official_series(sid):
    """Try independent official FRED transports and record the winning route."""
    errors = []
    transport_ok = False
    api_key = os.getenv("FRED_API_KEY", "").strip()
    if api_key:
        try:
            response = _get_with_retry(
                API_BASE,
                params={"series_id": sid, "api_key": api_key, "file_type": "json"},
                attempts=2,
                accept="application/json",
            )
            transport_ok = True
            x, valcol = _parse_api_response(response.json(), sid)
            return x, valcol, response.url, "fred_api"
        except Exception as exc:
            errors.append(f"api={type(exc).__name__}: {exc}")
    try:
        url = SERIES_PAGE.format(sid=sid)
        response = _get_with_retry(url, attempts=2, accept="text/html")
        transport_ok = True
        x, valcol = _parse_series_page(response.text, sid)
        return x, valcol, response.url, "official_series_page"
    except Exception as exc:
        errors.append(f"page={type(exc).__name__}: {exc}")
    try:
        response = _get_with_retry(BASE, params={"id": sid}, attempts=1)
        transport_ok = True
        x, valcol = _parse_response(response.text)
        return x, valcol, response.url, "fredgraph_single"
    except Exception as exc:
        errors.append(f"graph={type(exc).__name__}: {exc}")
    raise FredOfficialFetchError(" | ".join(errors), transport_ok=transport_ok)


def _parse_batch_response(content, requested_ids):
    """Parse FRED's multi-series CSV/ZIP response into one frame per series.

    FRED returns a ZIP archive when requested series have different frequencies.
    One batched request is both faster and materially less prone to the repeated
    timeouts seen when every series is fetched serially.
    """
    payloads = []
    if content[:2] == b"PK":
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for member in archive.namelist():
                if member.lower().endswith(".csv"):
                    payloads.append(archive.read(member).decode("utf-8-sig"))
    else:
        payloads.append(content.decode("utf-8-sig"))

    parsed = {}
    for text in payloads:
        frame = pd.read_csv(io.StringIO(text))
        date_col = next(
            (c for c in ("observation_date", "DATE", "date") if c in frame.columns),
            None,
        )
        if date_col is None:
            continue
        frame[date_col] = pd.to_datetime(frame[date_col], errors="coerce")
        for sid in requested_ids:
            if sid not in frame.columns:
                continue
            values = pd.to_numeric(frame[sid], errors="coerce")
            valid = pd.DataFrame({"DATE": frame[date_col], sid: values}).dropna()
            if not valid.empty:
                parsed[sid] = valid
    return parsed


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

    batch = {}
    batch_error = None
    if series:
        try:
            response = _get_with_retry(
                BASE, params={"id": ",".join(dict.fromkeys(series.values()))}, attempts=2
            )
            batch = _parse_batch_response(response.content, set(series.values()))
        except Exception as exc:
            batch_error = exc

    for name, sid in series.items():
        transport_status = "error"
        content_status = "not_checked"
        retrieval_route = "none"
        source_url = f"{BASE}?id={sid}"
        try:
            if sid in batch:
                x, valcol = batch[sid], sid
                transport_status = "ok"
                source_url = f"{BASE}?id={','.join(dict.fromkeys(series.values()))}"
                retrieval_route = "fredgraph_batch"
            else:
                x, valcol, source_url, retrieval_route = _fetch_official_series(sid)
                transport_status = "ok"
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
                    "retrieval_route": retrieval_route,
                }
            )
        except Exception as exc:
            if getattr(exc, "transport_ok", False):
                transport_status = "ok"
            cached, cache_age_days = _cached_observation(
                cache, name, sid, max_cache_age_days
            )
            errors = []
            if batch_error is not None:
                errors.append(f"batch={type(batch_error).__name__}: {batch_error}")
            errors.append(f"series={type(exc).__name__}: {exc}")
            error = " | ".join(errors)
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
                        "retrieval_route": retrieval_route,
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
                        "retrieval_route": retrieval_route,
                    }
                )

    return pd.DataFrame(rows, columns=FRED_COLUMNS), health
