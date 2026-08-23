from __future__ import annotations

import logging
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import requests

from .config import SETTINGS

LOG = logging.getLogger(__name__)

TV_COLUMNS = [
    "name",
    "description",
    "close",
    "volume",
    "average_volume_30d_calc",
    "market_cap_basic",
    "price_earnings_ttm",
    "price_book_fq",
    "dividends_yield_current",
    "return_on_equity_fq",
    "debt_to_equity_fq",
    "gross_margin_ttm",
    "operating_margin_ttm",
    "net_margin_ttm",
    "total_revenue_yoy_growth_ttm",
    "earnings_per_share_diluted_yoy_growth_ttm",
    "Perf.1M",
    "Perf.3M",
    "Perf.6M",
    "Perf.Y",
    "Volatility.M",
    "beta_1_year",
]

OUTPUT_COLUMNS = [
    "source_code",
    "source_name",
    "source_description",
    "price",
    "volume",
    "avg_volume_30d",
    "market_cap",
    "pe",
    "pb",
    "dividend_yield",
    "roe",
    "debt_to_equity",
    "gross_margin",
    "operating_margin",
    "profit_margin",
    "revenue_growth",
    "earnings_growth",
    "return_1m",
    "return_3m",
    "return_6m",
    "return_12m",
    "volatility_1m",
    "beta_1y",
]


def _scan(market: str) -> pd.DataFrame:
    url = f"https://scanner.tradingview.com/{market}/scan"
    payload = {
        "filter": [{"left": "type", "operation": "equal", "right": "stock"}],
        "options": {"lang": "en"},
        "markets": [market],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": TV_COLUMNS,
        "range": [0, 50000],
    }
    response = requests.post(
        url,
        json=payload,
        headers={"User-Agent": SETTINGS.http_user_agent},
        timeout=max(SETTINGS.request_timeout, 60),
    )
    response.raise_for_status()
    body = response.json()
    rows = []
    for item in body.get("data", []):
        values = item.get("d", [])
        if len(values) != len(TV_COLUMNS):
            continue
        row = dict(zip(OUTPUT_COLUMNS[1:], values))
        row["source_code"] = str(values[0]).upper().replace(".", "-")
        row["source_symbol"] = item.get("s")
        row["source_exchange"] = str(item.get("s") or "").split(":", 1)[0].upper()
        rows.append(row)
    frame = pd.DataFrame(rows)
    frame.attrs["reported_total_count"] = body.get("totalCount")
    return frame


def download_market_snapshot(universe: pd.DataFrame) -> pd.DataFrame:
    retrieved = datetime.now(timezone.utc).isoformat()
    snapshots = []
    errors = []
    for universe_market, scanner_market in (("JP", "japan"), ("US", "america")):
        try:
            snapshot = _scan(scanner_market)
            snapshot["market"] = universe_market
            snapshots.append(snapshot)
            LOG.info(
                "TradingView %s: %s rows (reported %s)",
                universe_market,
                len(snapshot),
                snapshot.attrs.get("reported_total_count"),
            )
        except Exception as exc:
            LOG.exception("TradingView %s scan failed", universe_market)
            errors.append(f"{universe_market}: {exc}")
    if not snapshots:
        raise RuntimeError("全市場のスナップショット取得に失敗: " + " | ".join(errors))
    snapshot = pd.concat(snapshots, ignore_index=True)
    base = universe.copy()
    base["merge_code"] = base["code"].astype(str).str.upper().str.replace(".", "-", regex=False)
    exchange_map = {
        "NYSE AMERICAN": "AMEX",
        "NYSE ARCA": "AMEX",
        "CBOE BZX": "CBOE",
        "STANDARD MARKET (DOMESTIC)": "TSE",
        "STANDARD MARKET(DOMESTIC)": "TSE",
        "PRIME MARKET (DOMESTIC)": "TSE",
        "PRIME MARKET(DOMESTIC)": "TSE",
        "GROWTH MARKET (DOMESTIC)": "TSE",
        "GROWTH MARKET(DOMESTIC)": "TSE",
    }
    base["merge_exchange"] = base["exchange"].astype(str).str.upper().replace(exchange_map)
    snapshot["merge_code"] = snapshot["source_code"]
    snapshot["merge_exchange"] = snapshot["source_exchange"]
    snapshot = snapshot.drop_duplicates(["market", "merge_exchange", "merge_code"])
    result = base.merge(
        snapshot,
        on=["market", "merge_exchange", "merge_code"],
        how="left",
        suffixes=("", "_snapshot"),
        validate="one_to_one",
    )
    numeric = [column for column in OUTPUT_COLUMNS if column not in {"source_code", "source_name", "source_description"}]
    for column in numeric:
        if column in result:
            result[column] = pd.to_numeric(result[column], errors="coerce")
    result["avg_turnover_30d"] = result["price"] * result["avg_volume_30d"]
    result["price_status"] = np.where(result["price"].notna(), "ok", "missing")
    fundamental_fields = ["pe", "pb", "roe", "profit_margin", "revenue_growth", "earnings_growth", "market_cap"]
    present = result[fundamental_fields].notna().sum(axis=1)
    result["fundamental_fields_present"] = present
    result["fundamental_status"] = np.select(
        [present >= 5, present >= 2], ["ok", "partial"], default="missing"
    )
    result["data_retrieved_at_utc"] = retrieved
    result["price_date"] = None
    result["price_basis"] = "TradingView scanner close; exact exchange timestamp unavailable"
    result["price_source"] = "TradingView scanner (unofficial/undocumented)"
    result["fundamental_source"] = "TradingView scanner (unofficial/undocumented)"
    result.attrs["errors"] = errors
    return result
