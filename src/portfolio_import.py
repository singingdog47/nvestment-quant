from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

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
    """Decode Rakuten Securities CSV exports.

    Rakuten Japanese exports are commonly CP932/Shift-JIS. UTF-8 variants are
    also accepted. We never silently replace undecodable bytes because that can
    corrupt security codes/names and lead to a wrong portfolio.
    """
    for enc in ("utf-8-sig", "cp932", "shift_jis"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("rakuten_csv", raw, 0, min(len(raw), 1), "unsupported encoding")


def _num(v: str | None) -> float | None:
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("+", "")
    if s in {"", "-", "--"}:
        return None
    s = re.sub(r"[^0-9.\-]", "", s)
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _norm_header(s: str) -> str:
    return re.sub(r"[\s\[\]（）()・･]", "", str(s)).lower()


def _find_detail_header(rows: list[list[str]]) -> tuple[int, list[str]]:
    """Find the '保有商品詳細' table header instead of assuming a fixed row."""
    for i, row in enumerate(rows):
        norm = [_norm_header(x) for x in row]
        has_code = any(("銘柄コード" in x or "ティッカー" in x) for x in norm)
        has_qty = any("保有数量" in x for x in norm)
        has_value = any("時価評価額" in x for x in norm)
        if has_code and has_qty and has_value:
            return i, row
    raise ValueError("Rakuten holdings detail header not found")


def _idx(headers: list[str], *needles: str) -> int | None:
    normalized = [_norm_header(x) for x in headers]
    for needle in needles:
        n = _norm_header(needle)
        for i, h in enumerate(normalized):
            if n and n in h:
                return i
    return None


def _get(row: list[str], idx: int | None) -> str:
    if idx is None or idx >= len(row):
        return ""
    return str(row[idx]).strip()


def _ticker(asset_type: str, code: str) -> str:
    at = asset_type.strip()
    c = code.strip()
    if "国内株" in at and re.fullmatch(r"\d{4}", c):
        return f"{c}.T"
    return c


def parse_rakuten_csv_bytes(raw: bytes) -> ParseResult:
    text, enc = decode_rakuten_bytes(raw)
    rows = list(csv.reader(io.StringIO(text)))
    header_i, headers = _find_detail_header(rows)

    i_type = _idx(headers, "種別")
    i_code = _idx(headers, "銘柄コード・ティッカー", "銘柄コード", "ティッカー")
    i_name = _idx(headers, "銘柄")
    i_account = _idx(headers, "口座")
    i_qty = _idx(headers, "保有数量")
    i_avg = _idx(headers, "平均取得価額")
    i_price = _idx(headers, "現在値")
    i_value = _idx(headers, "時価評価額[円]", "時価評価額")

    out: list[dict] = []
    seen = 0
    for row in rows[header_i + 1:]:
        if not any(str(x).strip() for x in row):
            continue
        seen += 1
        asset_type = _get(row, i_type)
        code = _get(row, i_code)
        name = _get(row, i_name)
        qty = _num(_get(row, i_qty))
        mv = _num(_get(row, i_value))
        # Ignore totals, cash sections, and malformed rows. A security must have
        # an identifier plus a positive market value to enter risk calculations.
        if not code or mv is None or mv <= 0:
            continue
        currency = "JPY" if "国内" in asset_type or re.fullmatch(r"\d{4}", code) else "USD"
        out.append({
            "asset_type": asset_type,
            "code": code,
            "ticker": _ticker(asset_type, code),
            "name": name,
            "account": _get(row, i_account),
            "quantity": qty,
            "avg_cost": _num(_get(row, i_avg)),
            "current_price": _num(_get(row, i_price)),
            "market_value": mv,
            "currency": currency,
        })

    df = pd.DataFrame(out)
    if df.empty:
        raise ValueError("No holdings rows parsed from Rakuten CSV")
    total = float(df["market_value"].sum())
    if total <= 0:
        raise ValueError("Portfolio market value is zero")
    df["weight"] = df["market_value"] / total
    df = df[PORTFOLIO_COLUMNS]
    return ParseResult(df, enc, seen, len(df))


def convert_file(source: str | Path, destination: str | Path) -> ParseResult:
    src = Path(source)
    dst = Path(destination)
    result = parse_rakuten_csv_bytes(src.read_bytes())
    dst.parent.mkdir(parents=True, exist_ok=True)
    result.portfolio.to_csv(dst, index=False, encoding="utf-8")
    return result
