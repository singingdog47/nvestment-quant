from __future__ import annotations

import csv
import io
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from .portfolio_import import decode_rakuten_bytes
except ImportError:  # Legacy top-level test imports
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
        "楽天銀行普通預金残高": "rakuten_bank_jpy",
        "外貨預り金": "foreign_cash_jpy",
        "信用保証金": "margin_collateral_jpy",
        "国内株式信用保証金": "margin_collateral_jpy",
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



def reconcile_account_components(parsed: dict) -> dict:
    """Reconcile historical balances; never infer executable cash."""
    required = ("total_assets_jpy", "invested_assets_jpy",
                "deposits_total_jpy", "cash_deposit_jpy",
                "foreign_cash_jpy", "margin_collateral_jpy",
                "fx_margin_net_assets_jpy")
    missing = [key for key in required if key not in parsed]
    if missing:
        return {"status": "INCOMPLETE", "missing": missing,
                "deployable_cash_jpy": None, "execution_ready": False}
    asset_residual = parsed["total_assets_jpy"] - (
        parsed["invested_assets_jpy"] + parsed["deposits_total_jpy"]
        + parsed["fx_margin_net_assets_jpy"])
    deposit_residual = parsed["deposits_total_jpy"] - (
        parsed["cash_deposit_jpy"] + parsed["foreign_cash_jpy"]
        + parsed["margin_collateral_jpy"])
    return {"status": "RECONCILED_HISTORICAL"
            if asset_residual == 0 and deposit_residual == 0 else "MISMATCH",
            "asset_residual_jpy": asset_residual,
            "deposit_residual_jpy": deposit_residual,
            "deployable_cash_jpy": None, "execution_ready": False}


def summarize_open_orders(items: list[dict]) -> tuple[list[dict], int | None]:
    """Count open domestic cash orders only when every row can be classified."""
    open_statuses = {
        "執行待", "執行待ち", "執行中", "待機中", "受付済", "受付済み",
        "未約定", "出来有", "一部約定", "取消中", "訂正中", "市場執行中",
    }
    closed_statuses = {
        "約定", "約定済", "約定済み", "全部約定", "取消済", "取消済み",
        "取消済出来有", "取消済出来無", "出来ず", "出来ず出来有", "出来ず出来無", "失効",
    }
    open_items = []
    count_known = True
    for item in items:
        status = item.get("status") if isinstance(item, dict) else None
        label = _norm(status) if isinstance(status, str) else ""
        if label in open_statuses:
            open_items.append(item)
        elif label not in closed_statuses:
            count_known = False
    return open_items, len(open_items) if count_known else None


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
    _, open_count = summarize_open_orders(items)
    return {
        "status": "ok",
        "source_encoding": encoding,
        "orders_count": len(items),
        "open_orders_count": open_count,
        "filled_orders_count": sum((x.get("filled_quantity") or 0) > 0 for x in items),
        "items": items,
    }


def parse_buying_power_pdf(path: str | Path) -> dict:
    """Extract Rakuten cash buying power from a text-bearing PDF."""
    # Rakuten PDFs can contain CMaps that pypdf decodes as mojibake.
    # Prefer PyMuPDF Japanese extraction, retaining pypdf fallback.
    try:
        import fitz
        with fitz.open(str(path)) as doc:
            text = "\n".join(page.get_text() for page in doc)
    except ImportError:
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
    # A footer without an explicit year cannot establish an observation year.
    # Do not infer it from the runtime clock: historical PDFs may be replayed.
    timestamp = None
    match = re.search(r"(20\d{2})[/-](\d{2})[/-](\d{2})\s+(\d{2}:\d{2})", text)
    if match:
        timestamp = datetime.strptime(
            f"{match.group(1)}/{match.group(2)}/{match.group(3)} {match.group(4)}",
            "%Y/%m/%d %H:%M",
        ).replace(tzinfo=JST).isoformat()
    return {"status": "ok", "source_as_of": timestamp,
            "source_as_of_method": "pdf_footer_explicit_year" if timestamp else "missing",
            **values}


def source_as_of(name: str | None, modified_time: str | None) -> tuple[str | None, str]:
    return _timestamp_from_name(name, modified_time)


def parse_orders_document(path: str | Path) -> dict:
    """Date an order PDF without asserting complete rows or account coverage."""
    import fitz
    with fitz.open(str(path)) as doc:
        text = "\n".join(page.get_text() for page in doc)
        pages = len(doc)
    if "注文一覧" in text:
        scope = "orders_domestic_cash_document"
    elif "購入・売却履歴" in text:
        scope = "orders_mutual_funds_document"
    else:
        raise ValueError("Not a recognized order document")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    match = re.search(r"(20\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2})\s+\d+\s*/\s*(\d+)\s*ページ\s*$", "\n".join(lines[-8:]))
    if not match:
        raise ValueError("Order document requires a dated print footer")
    stamp = datetime.strptime(match.group(1), "%Y/%m/%d %H:%M").replace(tzinfo=JST)
    return {"status": "partial", "source_as_of": stamp.isoformat(),
            "source_as_of_method": "pdf_footer_explicit_year", "scope": scope,
            "document_verified": True, "pdf_pages": pages,
            "printed_page_count": int(match.group(2)), "orders_count": None,
            "items": None, "order_rows_verified": False,
            "account_wide_coverage_verified": False}


def parse_orders_file(path: str | Path) -> dict:
    p = Path(path)
    return parse_orders_document(p) if p.read_bytes()[:5] == b"%PDF-" else parse_orders_bytes(p.read_bytes())
