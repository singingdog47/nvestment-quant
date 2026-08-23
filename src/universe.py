from __future__ import annotations

import io
import logging
import re
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .config import SETTINGS

LOG = logging.getLogger(__name__)
JPX_PAGE = "https://www.jpx.co.jp/english/markets/statistics-equities/misc/01.html"
NASDAQ_LISTED = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_LISTED = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
HEADERS = {"User-Agent": SETTINGS.http_user_agent}


def _get(url: str) -> requests.Response:
    response = requests.get(url, headers=HEADERS, timeout=SETTINGS.request_timeout)
    response.raise_for_status()
    return response


def _find_jpx_xlsx() -> str:
    html = _get(JPX_PAGE).text
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        label = anchor.get_text(" ", strip=True).lower()
        if href.lower().endswith((".xlsx", ".xls")):
            lower_href = href.lower()
            score = (
                int("listed" in label)
                + 10 * int(lower_href.endswith("data_e.xls"))
                - 5 * int("updated" in lower_href)
            )
            candidates.append((score, urljoin(JPX_PAGE, href)))
    if not candidates:
        raise RuntimeError("JPXの銘柄一覧Excelリンクを検出できませんでした")
    return sorted(candidates, reverse=True)[0][1]


def load_japan_universe() -> pd.DataFrame:
    url = _find_jpx_xlsx()
    LOG.info("JPX universe: %s", url)
    raw = pd.read_excel(io.BytesIO(_get(url).content), dtype=str)
    normalized = {str(c).strip().lower(): c for c in raw.columns}
    code_col = next((v for k, v in normalized.items() if "code" in k), None)
    name_col = next((v for k, v in normalized.items() if "company name" in k or k == "name" or k.startswith("name ")), None)
    market_col = next((v for k, v in normalized.items() if "market" in k or "section/products" in k), None)
    product_col = next((v for k, v in normalized.items() if "product" in k), None)
    if not code_col or not name_col:
        raise RuntimeError(f"JPX Excelの列を特定できません: {list(raw.columns)}")
    if product_col:
        product = raw[product_col].fillna("").str.lower()
        domestic = product.str.contains("domestic", regex=False)
        if domestic.any():
            raw = raw[domestic]
    codes = raw[code_col].astype(str).str.upper().str.extract(r"([0-9A-Z]{4})", expand=False)
    result = pd.DataFrame(
        {
            "ticker": codes + ".T",
            "code": codes,
            "name": raw[name_col].astype(str).str.strip(),
            "market": "JP",
            "exchange": raw[market_col].astype(str).str.strip() if market_col else "TSE",
            "universe_source": "JPX",
        }
    )
    return result.dropna(subset=["ticker"]).drop_duplicates("ticker").reset_index(drop=True)


def _read_pipe(url: str) -> pd.DataFrame:
    text = _get(url).text
    frame = pd.read_csv(io.StringIO(text), sep="|", dtype=str)
    frame = frame[~frame.iloc[:, 0].astype(str).str.startswith("File Creation Time")]
    return frame


def _allowed_us_name(name: str) -> bool:
    lowered = name.lower()
    blocked = ("warrant", " rights", " unit", "preferred", "acquisition corp", "acquisition inc")
    return not any(term in lowered for term in blocked)


def load_us_universe() -> pd.DataFrame:
    nasdaq = _read_pipe(NASDAQ_LISTED)
    nasdaq = nasdaq[(nasdaq["Test Issue"] == "N") & (nasdaq["ETF"] == "N")]
    nasdaq = pd.DataFrame(
        {
            "ticker": nasdaq["Symbol"],
            "name": nasdaq["Security Name"],
            "exchange": "NASDAQ",
        }
    )
    other = _read_pipe(OTHER_LISTED)
    other = other[(other["Test Issue"] == "N") & (other["ETF"] == "N")]
    exchange_map = {"N": "NYSE", "A": "NYSE American", "P": "NYSE Arca", "Z": "Cboe BZX", "V": "IEX"}
    other = pd.DataFrame(
        {
            "ticker": other["ACT Symbol"],
            "name": other["Security Name"],
            "exchange": other["Exchange"].map(exchange_map).fillna(other["Exchange"]),
        }
    )
    result = pd.concat([nasdaq, other], ignore_index=True)
    result["ticker"] = result["ticker"].astype(str).str.replace(".", "-", regex=False).str.strip()
    result = result[result["ticker"].str.match(r"^[A-Z][A-Z0-9.-]{0,9}$", na=False)]
    result = result[result["name"].astype(str).map(_allowed_us_name)]
    result["code"] = result["ticker"]
    result["market"] = "US"
    result["universe_source"] = "Nasdaq Trader"
    return result.drop_duplicates("ticker").reset_index(drop=True)


def load_universe() -> pd.DataFrame:
    frames = []
    errors = []
    for market, loader in (("JP", load_japan_universe), ("US", load_us_universe)):
        try:
            frames.append(loader())
        except Exception as exc:  # each market remains independently diagnosable
            LOG.exception("%s universe failed", market)
            errors.append(f"{market}: {exc}")
    if not frames:
        raise RuntimeError("全市場の銘柄一覧取得に失敗: " + " | ".join(errors))
    result = pd.concat(frames, ignore_index=True)
    if SETTINGS.max_tickers > 0:
        result = (
            result.groupby("market", group_keys=False)
            .head(SETTINGS.max_tickers)
            .reset_index(drop=True)
        )
    result.attrs["errors"] = errors
    return result
