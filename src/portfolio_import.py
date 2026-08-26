from __future__ import annotations

import csv
import hashlib
import io
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

PORTFOLIO_COLUMNS = [
    "holding_id", "asset_type", "code", "ticker", "name", "account", "quantity",
    "avg_cost", "current_price", "market_value", "currency", "fx_exposure_type",
    "fx_beta_usdjpy", "classification_status", "weight"
]

@dataclass
class ParseResult:
    portfolio: pd.DataFrame
    source_encoding: str
    rows_seen: int
    rows_kept: int

def decode_rakuten_bytes(raw: bytes) -> tuple[str, str]:
    for enc in ("utf-8-sig", "cp932", "shift_jis"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise ValueError("Unsupported Rakuten CSV encoding")

def _num(v: str | None) -> float | None:
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("+", "")
    if s in {"", "-", "--"}:
        return None
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return float(s) if s else None
    except ValueError:
        return None

def _norm(s: str) -> str:
    return re.sub(r"[\s\[\]（）()・･]", "", str(s)).lower()

def _find_header(rows: list[list[str]]) -> tuple[int, list[str]]:
    for i, row in enumerate(rows):
        n = [_norm(x) for x in row]
        if any("銘柄コード" in x or "ティッカー" in x for x in n) and any("保有数量" in x for x in n) and any("時価評価額" in x for x in n):
            return i, row
    raise ValueError("Rakuten holdings detail header not found")

def _idx(headers: list[str], *needles: str) -> int | None:
    nh = [_norm(x) for x in headers]
    # Exact match first so "銘柄" does not accidentally resolve to
    # "銘柄コード・ティッカー".
    for needle in needles:
        nn = _norm(needle)
        for i, h in enumerate(nh):
            if h == nn:
                return i
    for needle in needles:
        nn = _norm(needle)
        for i, h in enumerate(nh):
            if nn in h:
                return i
    return None

def _get(row: list[str], i: int | None) -> str:
    return "" if i is None or i >= len(row) else str(row[i]).strip()

def classify_fx_exposure(asset_type: str, code: str, name: str) -> dict[str, object]:
    """Conservatively classify FX exposure; never treat every foreign fund as USD.

    `fx_beta_usdjpy` is populated only for direct/unhedged USD assets.  Basket
    funds remain unmodelled until a look-through holding file or an explicitly
    reviewed private override supplies a beta.
    """
    text = _norm(f"{asset_type} {code} {name}")
    domestic = "国内株" in asset_type or bool(re.fullmatch(r"\d{4}", code))
    if domestic or any(k in text for k in ("topix", "日経225", "国内株式")):
        return {"currency": "JPY", "fx_exposure_type": "domestic", "fx_beta_usdjpy": 0.0,
                "classification_status": "rule_confirmed"}
    if "為替ヘッジあり" in text or "currencyhedged" in text:
        return {"currency": "HEDGED", "fx_exposure_type": "hedged", "fx_beta_usdjpy": 0.0,
                "classification_status": "rule_confirmed"}
    if "外貨預り金" in asset_type and any(k in text for k in ("米ドル", "usd", "usドル")):
        return {"currency": "USD", "fx_exposure_type": "direct_cash", "fx_beta_usdjpy": 1.0,
                "classification_status": "rule_confirmed"}
    if any(k in text for k in ("新興国", "emerging", "インド", "中国", "台湾")):
        return {"currency": "EM_BASKET", "fx_exposure_type": "currency_basket", "fx_beta_usdjpy": None,
                "classification_status": "lookthrough_required"}
    if "米国株" in asset_type:
        return {"currency": "USD", "fx_exposure_type": "direct", "fx_beta_usdjpy": 1.0,
                "classification_status": "rule_confirmed"}
    if any(k in text for k in ("全米株式", "s&p500", "nasdaq", "vti")):
        return {"currency": "USD", "fx_exposure_type": "direct", "fx_beta_usdjpy": 1.0,
                "classification_status": "name_rule_inferred"}
    return {"currency": "UNKNOWN", "fx_exposure_type": "unknown", "fx_beta_usdjpy": None,
            "classification_status": "manual_review_required"}

def parse_rakuten_csv_bytes(raw: bytes) -> ParseResult:
    text, enc = decode_rakuten_bytes(raw)
    rows = list(csv.reader(io.StringIO(text)))
    hi, headers = _find_header(rows)
    ix = {
        "asset_type": _idx(headers, "種別"),
        "code": _idx(headers, "銘柄コード・ティッカー", "銘柄コード", "ティッカー"),
        "name": _idx(headers, "銘柄"),
        "account": _idx(headers, "口座"),
        "quantity": _idx(headers, "保有数量"),
        "avg_cost": _idx(headers, "平均取得価額"),
        "current_price": _idx(headers, "現在値"),
        "market_value": _idx(headers, "時価評価額[円]", "時価評価額"),
    }
    out = []
    seen = 0
    for row in rows[hi + 1:]:
        if not any(str(x).strip() for x in row):
            continue
        seen += 1
        code = _get(row, ix["code"])
        name = _get(row, ix["name"])
        mv = _num(_get(row, ix["market_value"]))
        if not (code or name) or mv is None or mv <= 0:
            continue
        asset_type = _get(row, ix["asset_type"])
        domestic = "国内株" in asset_type or bool(re.fullmatch(r"\d{4}", code))
        ticker = f"{code}.T" if domestic and re.fullmatch(r"\d{4}", code) else code
        account = _get(row, ix["account"])
        fx = classify_fx_exposure(asset_type, code, name)
        holding_id = hashlib.sha256(f"{asset_type}|{code}|{name}|{account}".encode("utf-8")).hexdigest()[:16]
        out.append({
            "holding_id": holding_id,
            "asset_type": asset_type,
            "code": code,
            "ticker": ticker,
            "name": name,
            "account": account,
            "quantity": _num(_get(row, ix["quantity"])),
            "avg_cost": _num(_get(row, ix["avg_cost"])),
            "current_price": _num(_get(row, ix["current_price"])),
            "market_value": mv,
            **fx,
        })
    df = pd.DataFrame(out)
    if df.empty:
        raise ValueError("No holdings rows parsed from Rakuten CSV")
    total = float(df["market_value"].sum())
    if total <= 0:
        raise ValueError("Portfolio market value is zero")
    df["weight"] = df["market_value"] / total
    return ParseResult(df[PORTFOLIO_COLUMNS], enc, seen, len(df))

def convert_file(source: str | Path, destination: str | Path) -> ParseResult:
    result = parse_rakuten_csv_bytes(Path(source).read_bytes())
    dst = Path(destination)
    dst.parent.mkdir(parents=True, exist_ok=True)
    result.portfolio.to_csv(dst, index=False, encoding="utf-8")
    return result


def infer_portfolio_source_as_of(file_name: str | None, modified_time: str | None) -> tuple[str | None, str]:
    """Prefer the embedded Rakuten export timestamp over a re-upload timestamp."""
    embedded: datetime | None = None
    match = re.search(r"(20\d{6})[_-](\d{6})", str(file_name or ""))
    if match:
        try:
            jst = timezone(timedelta(hours=9))
            embedded = datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").replace(tzinfo=jst)
        except ValueError:
            embedded = None
    modified: datetime | None = None
    if modified_time:
        try:
            modified = datetime.fromisoformat(str(modified_time).replace("Z", "+00:00"))
        except ValueError:
            modified = None
    if embedded is not None:
        return embedded.isoformat(), "filename_embedded_export_time"
    if modified is not None:
        return modified.isoformat(), "drive_modified_time_fallback"
    return None, "missing"
