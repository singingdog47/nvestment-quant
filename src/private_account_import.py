from __future__ import annotations

import csv
import io
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from portfolio_import import decode_rakuten_bytes


JST = timezone(timedelta(hours=9))


def _num(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "").replace("+", "")
    if text in {"", "-", "--"}:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def _norm(value: str) -> str:
    return re.sub(r"[\s（）()※＊*]", "", str(value))


def _timestamp_from_name(name: str | None, modified_time: str | None) -> tuple[str | None, str]:
    text = str(name or "")
    match = re.search(r"(20\d{6})[_-](\d{6})", text)
    if match:
        try:
            value = datetime.strptime("".join(match.groups()), "%Y%m%d%H%M%S").replace(tzinfo=JST)
            return value.isoformat(), "filename_embedded_export_time"
        except ValueError:
            pass
    match = re.search(r"(20\d{6})", text)
    if match:
        try:
            value = datetime.strptime(match.group(1), "%Y%m%d").replace(tzinfo=JST)
            return value.isoformat(), "filename_embedded_export_date"
        except ValueError:
            pass
    if modified_time:
        try:
            return datetime.fromisoformat(str(modified_time).replace("Z", "+00:00")).isoformat(), "drive_modified_time_fallback"
        except ValueError:
            pass
    return None, "missing"


def parse_account_summary_bytes(raw: bytes) -> dict:
    """Parse the account-level summary from a Rakuten holdings export."""
    text, encoding = decode_rakuten_bytes(raw)
    rows = list(csv.reader(io.StringIO(text)))
    wanted = {
        "資産合計": "total_assets_jpy",
        "保有商品の評価額合計": "invested_assets_jpy",
        "預り金合計": "deposits_total_jpy",
        "預り金": "cash_deposit_jpy",
        "外貨預り金": "foreign_cash_jpy",
        "信用保証金": "margin_collateral_jpy",
        "FX証拠金純資産": "fx_margin_net_assets_jpy",
    }
    values: dict[str, float] = {}
    daily_change_jpy: float | None = None
    daily_change_pct: float | None = None
    for row in rows:
        if not row:
            continue
        label = _norm(row[0])
        key = wanted.get(label)
        if not key:
            continue
        value = _num(row[1] if len(row) > 1 else None)
        if value is not None:
            values[key] = value
        if key == "total_assets_jpy":
            daily_change_jpy = _num(row[2] if len(row) > 2 else None)
            daily_change_pct = _num(row[3] if len(row) > 3 else None)
    if "total_assets_jpy" not in values or "invested_assets_jpy" not in values:
        raise ValueError("Rakuten account summary rows not found")
    return {
        "status": "ok",
        "source_encoding": encoding,
        **values,
        "daily_change_jpy": daily_change_jpy,
        "daily_change_pct": daily_change_pct,
    }


def parse_orders_bytes(raw: bytes) -> dict:
    """Parse only order-state metadata; this function never places orders."""
    text, encoding = decode_rakuten_bytes(raw)
    rows = list(csv.reader(io.StringIO(text)))
    if not rows or not any("注文番号" in _norm(x) for x in rows[0]):
        raise ValueError("Rakuten order header not found")
    headers = [_norm(x) for x in rows[0]]

    def idx(needle: str) -> int | None:
        return next((i for i, value in enumerate(headers) if needle in value), None)

    status_i = idx("状況")
    side_i = idx("売買")
    qty_i = idx("注文数量")
    filled_i = idx("約定数量")
    price_i = idx("注文単価")
    items = []
    for row in rows[1:]:
        if not row or not any(str(x).strip() for x in row):
            continue
        get = lambda i: "" if i is None or i >= len(row) else str(row[i]).strip()
        items.append({
            "status": get(status_i),
            "side": get(side_i),
            "quantity": _num(get(qty_i)),
            "filled_quantity": _num(get(filled_i)),
            "limit_price_jpy": _num(get(price_i)),
        })
    if not items:
        raise ValueError("No Rakuten order rows found")
    open_tokens = ("執行中", "待機中", "受付済", "未約定")
    return {
        "status": "ok",
        "source_encoding": encoding,
        "orders_count": len(items),
        "open_orders_count": sum(any(t in x["status"] for t in open_tokens) for x in items),
        "filled_orders_count": sum((x.get("filled_quantity") or 0) > 0 for x in items),
        "items": items,
    }


def parse_buying_power_pdf(path: str | Path) -> dict:
    """Extract Rakuten cash buying power from a text-bearing PDF."""
    from pypdf import PdfReader

    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)
    patterns = {
        "cash_buying_power_jpy": r"現物買付可能額[^\d]{0,80}([\d,]+)\s*円",
        "fund_buying_power_jpy": r"投資信託買付可能額[^\d]{0,80}([\d,]+)\s*円",
        "us_stock_buying_power_jpy": r"米国株式買付可能額（円貨）[^\d]{0,80}([\d,]+)\s*円",
        "margin_capacity_jpy": r"信用新規建余力[^\d]{0,80}([\d,]+)\s*円",
    }
    values: dict[str, float] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, flags=re.S)
        value = _num(match.group(1)) if match else None
        if value is not None:
            values[key] = value
    if "cash_buying_power_jpy" not in values:
        raise ValueError("Cash buying power not found in Rakuten PDF")
    timestamp = None
    match = re.search(r"(\d{2}/\d{2})\s+(\d{2}:\d{2})", text)
    if match:
        now = datetime.now(JST)
        timestamp = datetime.strptime(
            f"{now.year}/{match.group(1)} {match.group(2)}", "%Y/%m/%d %H:%M"
        ).replace(tzinfo=JST).isoformat()
    return {"status": "ok", "source_as_of": timestamp, **values}


def source_as_of(name: str | None, modified_time: str | None) -> tuple[str | None, str]:
    return _timestamp_from_name(name, modified_time)
