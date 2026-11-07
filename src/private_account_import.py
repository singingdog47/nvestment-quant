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
        "国内株式信用保証金": "margin_collateral_jpy",
        "FX証拠金純資産": "fx_margin_net_assets_jpy",
        "FX証拠金（純資産）": "fx_margin_net_assets_jpy",
        "楽天銀行普通預金残高": "rakuten_bank_balance_jpy",
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
    if values["total_assets_jpy"] < values["invested_assets_jpy"]:
        raise ValueError("Rakuten account totals inconsistent")
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

    order_id_i = idx("注文番号")
    code_i = idx("銘柄コード")
    name_i = idx("銘柄名")
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
            "order_id": get(order_id_i),
            "code": get(code_i),
            "name": get(name_i),
            "status": get(status_i),
            "side": get(side_i),
            "quantity": _num(get(qty_i)),
            "filled_quantity": _num(get(filled_i)),
            "limit_price_jpy": _num(get(price_i)),
        })
    if not items:
        raise ValueError("No Rakuten order rows found")
    open_tokens = ("執行中", "待機中", "受付済", "未約定", "一部約定", "一部出来")
    return {
        "status": "ok",
        "source_encoding": encoding,
        "orders_count": len(items),
        "open_orders_count": sum(any(t in x["status"] for t in open_tokens) for x in items),
        "filled_orders_count": sum((x.get("filled_quantity") or 0) > 0 for x in items),
        "items": items,
    }


def _pdf_text(path: str | Path) -> str:
    """Prefer readable Japanese text; reject a PDF that cannot be decoded."""
    from pypdf import PdfReader
    text = "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)
    if any(marker in text for marker in ("現物買付可能額", "注文一覧")):
        return text
    # Browser-printed Rakuten PDFs can contain fonts whose ToUnicode mapping
    # pypdf cannot decode. PyMuPDF correctly reads these real exports.
    import fitz

    with fitz.open(str(path)) as pdf:
        text = "\n".join(page.get_text() for page in pdf)
    if not any(marker in text for marker in ("現物買付可能額", "注文一覧")):
        raise ValueError("Rakuten PDF Japanese text could not be decoded")
    return text


def parse_buying_power_pdf(path: str | Path) -> dict:
    """Extract Rakuten cash buying power from a text-bearing PDF."""
    text = _pdf_text(path)
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
    footer = re.findall(r"(20[0-9]{2}/[0-9]{2}/[0-9]{2}) +([0-9]{2}:[0-9]{2})", text)
    if footer:
        if len(set(footer)) != 1:
            raise ValueError("Conflicting PDF footer timestamps")
        date_part, time_part = footer[0]
        timestamp = datetime.strptime(date_part + " " + time_part, "%Y/%m/%d %H:%M").replace(tzinfo=JST).isoformat()
    return {"status": "ok", "source_as_of": timestamp, "source_as_of_method": "pdf_footer_explicit_year" if footer else "pdf_embedded_timestamp_inferred_year", **values}



def parse_orders_pdf(path: str | Path) -> dict:
    """Parse Rakuten domestic cash-order inquiry PDF; fail closed on ambiguity."""
    text = _pdf_text(path)
    if "注文照会" not in text or "注文一覧" not in text:
        raise ValueError("Not a Rakuten order inquiry PDF")
    # Scope is explicit: this PDF covers domestic cash equity orders only.
    # Reject a narrowed status filter; never infer account-wide order absence.
    if not re.search(r"注文状況\s*すべての注文", text):
        raise ValueError("Order PDF status filter is not all orders")
    if not re.search(r"注文種類\s*現物のみ", text):
        raise ValueError("Order PDF trade type is not domestic cash only")
    count_match = re.search(r"(\d+)件中(\d+)～(\d+)件表示", text)
    if not count_match:
        raise ValueError("Order count or pagination not recognized")
    total, first, last = map(int, count_match.groups())
    # A filtered or partial page must never be mistaken for all account orders.
    if total > 0 and (first != 1 or last != total):
        raise ValueError("Order PDF pagination incomplete")
    if total == 0:
        items = []
    else:
        # PDFs may wrap a single order over multiple lines. We only accept
        # records whose order ID, status and security code are all present.
        rows = re.findall(
            r"(?m)^\s*(\d{3,})\s+(約定|取消済|失効|執行中|待機中|受付済|未約定|一部約定)\s+"
            r"(\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+([^\n]+)\n"
            r"\s*(\d{4})\s+",
            text,
        )
        if len(rows) != total:
            raise ValueError("Order PDF rows incomplete or ambiguous")
        items = [
            {"order_id": oid, "status": status, "ordered_at": ordered_at,
             "name": name.strip(), "code": code}
            for oid, status, ordered_at, name, code in rows
        ]
    # The printed document may have more pages than the supplied PDF file.\n    # Reject incomplete print exports instead of asserting all orders were observed.\n    printed_pages = re.findall(r"(?m)(\\d+)\\s*/\\s*(\\d+)\\s*ページ", text)\n    if printed_pages:\n        seen = {int(page) for page, _ in printed_pages}\n        totals = {int(total_pages) for _, total_pages in printed_pages}\n        if len(totals) != 1 or seen != set(range(1, next(iter(totals)) + 1)):\n            raise ValueError("Order PDF printed document pages incomplete")\n    # Require a full year from the printed PDF footer, not the upload time.
    stamps = re.findall(r"20\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2}", text)
    if not stamps:
        raise ValueError("Order PDF lacks explicit-year observation timestamp")
    observed = datetime.strptime(stamps[-1], "%Y/%m/%d %H:%M").replace(tzinfo=JST)
    return {
        "status": "ok", "source_as_of": observed.isoformat(),
        "source_as_of_method": "pdf_footer_explicit_year",
        "orders_count": total,
        "open_orders_count": sum(
            any(t in item["status"] for t in ("執行中", "待機中", "受付済", "未約定", "一部約定"))
            for item in items
        ),
        "items": items,
    }


def source_as_of(name: str | None, modified_time: str | None) -> tuple[str | None, str]:
    return _timestamp_from_name(name, modified_time)
