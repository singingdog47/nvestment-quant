from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

PORTFOLIO_COLUMNS = [
    "asset_type", "code", "ticker", "name", "account", "quantity",
    "avg_cost", "current_price", "market_value", "currency", "weight"
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
        mv = _num(_get(row, ix["market_value"]))
        if not code or mv is None or mv <= 0:
            continue
        asset_type = _get(row, ix["asset_type"])
        domestic = "国内株" in asset_type or bool(re.fullmatch(r"\d{4}", code))
        ticker = f"{code}.T" if domestic and re.fullmatch(r"\d{4}", code) else code
        out.append({
            "asset_type": asset_type,
            "code": code,
            "ticker": ticker,
            "name": _get(row, ix["name"]),
            "account": _get(row, ix["account"]),
            "quantity": _num(_get(row, ix["quantity"])),
            "avg_cost": _num(_get(row, ix["avg_cost"])),
            "current_price": _num(_get(row, ix["current_price"])),
            "market_value": mv,
            "currency": "JPY" if domestic else "USD",
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
