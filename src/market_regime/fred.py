from __future__ import annotations

import io
import time
import pandas as pd
import requests

from .common import now_iso

BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv"
UA = "investment-quant/1.6.1 (+research)"


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
                time.sleep(2 ** i)
    raise last_error if last_error else RuntimeError("FRED request failed")


def fetch_fred(series: dict):
    rows = []
    health = []
    fetched = now_iso()

    for name, sid in series.items():
        try:
            r = _get_with_retry(BASE, params={"id": sid}, attempts=3)
            df = pd.read_csv(io.StringIO(r.text))
            value_cols = [c for c in df.columns if c != "DATE"]
            if not value_cols:
                raise ValueError("no value column")
            valcol = value_cols[0]
            df[valcol] = pd.to_numeric(df[valcol], errors="coerce")
            x = df.dropna(subset=[valcol])
            if x.empty:
                raise ValueError("no observations")

            latest = x.iloc[-1]
            prev = x.iloc[-2] if len(x) > 1 else latest
            rows.append(
                {
                    "series": name,
                    "fred_id": sid,
                    "date": str(latest["DATE"]),
                    "value": float(latest[valcol]),
                    "previous": float(prev[valcol]),
                    "change": float(latest[valcol] - prev[valcol]),
                    "source": "FRED",
                    "source_url": r.url,
                    "fetched_at": fetched,
                    "data_status": "ok",
                }
            )
            health.append(
                {
                    "source": f"FRED:{sid}",
                    "status": "ok",
                    "records": len(x),
                    "fetched_at": fetched,
                    "error": "",
                    "source_tier": "primary",
                }
            )
        except Exception as e:
            health.append(
                {
                    "source": f"FRED:{sid}",
                    "status": "error",
                    "records": 0,
                    "fetched_at": fetched,
                    "error": f"{type(e).__name__}: {e}",
                    "source_tier": "primary",
                }
            )

    return pd.DataFrame(rows), health
