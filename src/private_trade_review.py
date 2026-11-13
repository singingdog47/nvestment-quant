"""Evidence-backed JP cash-equity order snapshots and sell/hold review, private only."""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import unicodedata
from zoneinfo import ZoneInfo

from .jpx_market_calendar import is_jpx_session
from .private_drive import download_named, upload_or_replace

JST = ZoneInfo("Asia/Tokyo")
LEDGER = "private_trade_ledger.jsonl"
REPORT = "private_trade_review_latest.json"
STATUSES = {"OPEN", "PARTIALLY_FILLED", "FILLED", "CANCELLED", "EXPIRED"}
TERMINAL = STATUSES - {"OPEN", "PARTIALLY_FILLED"}


def instant(value: str) -> datetime:
    result = datetime.fromisoformat(value)
    if result.utcoffset() is None:
        raise ValueError("timezone required")
    return result


def yen(value: str) -> Decimal:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]{1,12}(?:\.[0-9]{1,6})?", value):
        raise ValueError("invalid yen amount")
    return Decimal(value)


def order_key(row: dict) -> tuple:
    return (row["broker"], row["account_alias"], row["order_id"], instant(row["order_at"]))


def validate(row: dict) -> None:
    if row.get("schema_version") != 1 or row.get("asset") != "JP_CASH_EQUITY":
        raise ValueError("unsupported schema or asset")
    for key in ("broker", "account_alias", "account_type", "order_id", "evidence_ref"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            raise ValueError("missing identity or evidence")
    if not re.fullmatch(r"[0-9][0-9A-Z]{3}\.T", row["symbol"]):
        raise ValueError("invalid JP equity symbol")
    if row["side"] not in {"BUY", "SELL"} or row["status"] not in STATUSES:
        raise ValueError("unsupported order state")
    order_at, observed, recorded = (instant(row[k]) for k in ("order_at", "observed_at", "recorded_at"))
    if not order_at <= observed <= recorded:
        raise ValueError("inconsistent observation times")
    quantity, filled = row["quantity"], row["filled_quantity"]
    if type(quantity) is not int or type(filled) is not int or not 0 <= filled <= quantity or not quantity:
        raise ValueError("invalid order quantities")
    if ((row["status"] == "OPEN" and filled != 0)
        or (row["status"] == "PARTIALLY_FILLED" and not 0 < filled < quantity)
        or (row["status"] == "FILLED" and filled != quantity)
        or (row["status"] in {"CANCELLED", "EXPIRED"} and filled == quantity)):
        raise ValueError("quantity conflicts with status")
    if filled:
        if not yen(row["fill_price_jpy"]) or not yen(row["fill_value_jpy"]):
            raise ValueError("executed amount required")
        # A broker may display a rounded cumulative average; retain the reported amount.
        if abs(yen(row["fill_price_jpy"]) * filled - yen(row["fill_value_jpy"])) > Decimal("0.01") * filled:
            raise ValueError("executed amount conflicts with quantity and price")
        if row.get("execution_date"):
            d = date.fromisoformat(row["execution_date"])
            if not is_jpx_session(d) or not order_at.astimezone(JST).date() <= d <= observed.astimezone(JST).date():
                raise ValueError("execution date conflicts with evidence")
    elif any(row.get(k) is not None for k in ("fill_price_jpy", "fill_value_jpy", "execution_date")):
        raise ValueError("unfilled order cannot have execution values")
    if row.get("limit_price_jpy") is not None and not yen(row["limit_price_jpy"]):
        raise ValueError("zero limit price")
    if row.get("good_until") and date.fromisoformat(row["good_until"]) < order_at.astimezone(JST).date():
        raise ValueError("expiry predates order")
    if row.get("evidence_sha256") and not re.fullmatch(r"[0-9a-f]{64}", row["evidence_sha256"]):
        raise ValueError("invalid evidence digest")
    if mark := row.get("execution_day_close"):
        if (not row.get("execution_date") or not filled or not mark.get("evidence_ref")
            or not yen(mark["close_jpy"])):
            raise ValueError("unverified execution-day close")
        mark_at = instant(mark["observed_at"]).astimezone(JST)
        if (mark_at.date() < date.fromisoformat(row["execution_date"]) or mark_at > recorded
            or (mark_at.date().isoformat() == row["execution_date"] and (mark_at.hour, mark_at.minute) < (15, 30))):
            raise ValueError("close was not yet known")
    if row.get("decision") is not None:
        decision = row["decision"]
        if not isinstance(decision, dict) or any(not isinstance(decision.get(k), str) or not decision[k].strip()
                                                for k in ("reason", "evidence_ref", "timing_basis")):
            raise ValueError("unattributed decision")
        if decision.get("decided_at") and instant(decision["decided_at"]) > order_at:
            raise ValueError("decision occurred after order")


def read_rows(raw: bytes) -> list[dict]:
    rows, seen, latest = [], {}, {}
    for line in raw.decode("utf-8-sig").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        validate(row)
        key = order_key(row)
        stamp = instant(row["observed_at"])
        event = (key, stamp)
        if event in seen:
            raise ValueError("duplicate or conflicting order observation")
        prev = latest.get(key)
        if prev is not None:
            if (stamp <= instant(prev["observed_at"])
                or instant(row["recorded_at"]) < instant(prev["recorded_at"])
                or row["filled_quantity"] < prev["filled_quantity"]
                or (prev["status"] in TERMINAL and (row["status"], row["filled_quantity"], row.get("fill_value_jpy"))
                    != (prev["status"], prev["filled_quantity"], prev.get("fill_value_jpy")))
                or any(row[k] != prev[k] for k in ("symbol", "side", "account_type"))):
                raise ValueError("order history regressed or changed identity")
        seen[event] = row
        latest[key] = row
        rows.append(row)
    return rows


def append_rows(original: bytes, incoming: list[dict]) -> bytes:
    """Return the original byte prefix plus new rows, or reject the entire batch."""
    prior = {(order_key(r), instant(r["observed_at"])): r for r in read_rows(original)}
    extra = []
    for row in incoming:
        validate(row)
        key = (order_key(row), instant(row["observed_at"]))
        if key in prior:
            if {k: v for k, v in prior[key].items() if k != "recorded_at"} != {
                k: v for k, v in row.items() if k != "recorded_at"
            }:
                raise ValueError("conflicting observation")
            continue
        prior[key] = row
        extra.append(json.dumps(row, ensure_ascii=False, allow_nan=False).encode() + b"\n")
    result = original + (b"\n" if extra and original and not original.endswith(b"\n") else b"") + b"".join(extra)
    read_rows(result)
    return result


def rakuten_csv_rows(raw: bytes, *, observed_at: datetime, recorded_at: datetime,
                     account_alias: str, evidence_ref: str) -> list[dict]:
    """Import only rows with broker evidence. A CSV may cover a subset of the account."""
    try:
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        decoded = raw.decode("cp932")

    def norm(s):
        return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))

    def money(s):
        s = norm(s).replace(",", "").removesuffix("円")
        if s in {"", "-", "--", "成行"}:
            return None
        yen(s)
        return s

    def broker_time(s):
        s = unicodedata.normalize("NFKC", s.strip())
        m = re.fullmatch(r"(\d{4}/)?(\d{1,2})/(\d{1,2})\s+(\d{2}):(\d{2})(?::(\d{2}))?", s)
        if m:
            y, month, day, hour, minute, sec = m.groups()
            if not y and (int(month), int(day)) != (observed_at.astimezone(JST).month, observed_at.astimezone(JST).day):
                raise ValueError("historical order timestamp lacks a year")
            return datetime(int(y[:-1]) if y else observed_at.astimezone(JST).year,
                            int(month), int(day), int(hour), int(minute), int(sec or 0), tzinfo=JST)
        return instant(s)

    reader = csv.reader(io.StringIO(decoded))
    header = [norm(h).split("[", 1)[0] for h in next(reader)]
    digest = hashlib.sha256(raw).hexdigest()
    statuses = {label: status for status, labels in {
        "OPEN": ("執行中", "未約定", "受付済", "受付済み", "執行待", "執行待ち", "市場執行中"),
        "FILLED": ("約定", "約定済", "約定済み", "全部約定"),
        "PARTIALLY_FILLED": ("一部約定", "出来有"),
        "CANCELLED": ("取消済", "取消済み", "取消済出来有", "取消済出来無"),
        "EXPIRED": ("失効", "出来ず", "出来ず出来有", "出来ず出来無"),
    }.items() for label in labels}
    out = []
    for values in reader:
        if not any(v.strip() for v in values):
            continue
        if len(values) != len(header):
            raise ValueError("incomplete CSV row")
        data = dict(zip(header, values))
        if len(data) != len(header):
            raise ValueError("duplicate CSV columns")

        def get(*names, default=None):
            return next((data[n].strip() for n in names if data.get(n, "").strip()), default)

        market = norm(get("市場", default=""))
        trade = norm(get("取引", "取引区分", default=""))
        side = norm(get("売買", default=trade)).removeprefix("現物")
        if not trade.startswith("現物") or not market.startswith(("東証", "東京証券取引所")):
            raise ValueError("only verified JP cash orders are supported")
        code = norm(get("銘柄コード", default=""))
        executed = get("約定日")
        expires = get("注文期限", "有効期限")
        row = {"schema_version": 1, "asset": "JP_CASH_EQUITY", "broker": "RAKUTEN",
               "account_alias": account_alias, "account_type": get("口座", "口座区分"),
               "order_id": get("注文番号"), "order_at": broker_time(get("注文日時", "注文日/時刻")).isoformat(),
               "symbol": code + ".T", "side": {"買付": "BUY", "売付": "SELL"}[side],
               "status": statuses[norm(get("状況", "注文状況"))], "quantity": int(norm(get("注文数量")).replace(",", "")),
               "filled_quantity": int(norm(get("約定数量", default="0")).replace(",", "")),
               "limit_price_jpy": money(get("注文単価", default="")),
               "fill_price_jpy": money(get("約定単価", default="")),
               "fill_value_jpy": money(get("約定代金", default="")),
               "execution_date": executed.replace("/", "-") if executed and executed != "-" else None,
               "good_until": expires.replace("/", "-") if expires and expires != "-" else None,
               "observed_at": observed_at.isoformat(), "recorded_at": recorded_at.isoformat(),
               "evidence_ref": evidence_ref, "evidence_sha256": digest}
        if not row["filled_quantity"] and row["fill_value_jpy"] == "0":
            row["fill_value_jpy"] = None
        validate(row)
        out.append(row)
    if not out:
        raise ValueError("no order evidence; do not infer zero orders")
    return out


def session_after(day: date, n: int) -> date:
    for _ in range(n):
        day += timedelta(days=1)
        while not is_jpx_session(day):
            day += timedelta(days=1)
    return day


def yahoo_comparison(symbol: str, start: date, end: date) -> dict | None:
    """Require the specified daily bar and guard against an intervening split."""
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    p1 = int(datetime.combine(start, datetime.min.time(), JST).timestamp())
    p2 = int(datetime.combine(end + timedelta(days=1), datetime.min.time(), JST).timestamp())
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?" + urlencode(
        {"period1": p1, "period2": p2, "interval": "1d", "events": "splits"})
    try:
        with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=8) as reply:
            payload = json.load(reply)["chart"]["result"][0]
        if payload["meta"]["symbol"] != symbol:
            return None
        if payload.get("events", {}).get("splits"):
            return {"status": "CORPORATE_ACTION_REVIEW_REQUIRED"}
        close = next(value for stamp, value in zip(payload["timestamp"], payload["indicators"]["quote"][0]["close"])
                     if datetime.fromtimestamp(stamp, JST).date() == end)
        return {"status": "AVAILABLE", "close_jpy": str(Decimal(str(close)).quantize(Decimal("0.001"))),
                "evidence_ref": url}
    except (OSError, ValueError, TypeError, KeyError, IndexError, StopIteration, InvalidOperation):
        return None


def build_review(raw: bytes, as_of: datetime, quotes=None) -> dict:
    rows = read_rows(raw)
    latest, decisions, execution_closes = {}, {}, {}
    for row in rows:
        if instant(row["recorded_at"]) > as_of:
            continue
        key = order_key(row)
        latest[key] = row
        if row.get("decision"):
            decisions[key] = row["decision"]
        if row.get("execution_day_close"):
            execution_closes[key] = row["execution_day_close"]
    out = []
    now = as_of.astimezone(JST)
    for key, row in latest.items():
        entry = dict(row, decision=decisions.get(key), review=[])
        if row["status"] not in TERMINAL and row.get("good_until") and now.date() > date.fromisoformat(row["good_until"]):
            entry["current_state"] = "LAST_OBSERVATION_EXPIRED_CHECK_BROKER"
        else:
            entry["current_state"] = "HISTORICAL_BROKER_OBSERVATION"
        if row["side"] == "SELL" and row["filled_quantity"] and row.get("execution_date"):
            start = date.fromisoformat(row["execution_date"])
            for horizon in (0, 1, 5, 20):
                day = session_after(start, horizon)
                item = {"session_offset": horizon, "session": day.isoformat(), "status": "PENDING_SESSION"}
                if now >= datetime.combine(day, datetime.min.time().replace(hour=15, minute=30), JST):
                    mark = execution_closes.get(key)
                    if horizon == 0 and mark:
                        value = dict(mark, status="AVAILABLE")
                    else:
                        value = quotes(row["symbol"], start, day) if quotes else None
                    item.update(value or {"status": "NO_VERIFIED_CLOSE"})
                    if item["status"] == "AVAILABLE":
                        if not item.get("evidence_ref") or yen(item["close_jpy"]) <= 0:
                            raise ValueError("unverified close")
                        delta = yen(row["fill_value_jpy"]) - yen(item["close_jpy"]) * row["filled_quantity"]
                        item["sale_minus_hold_jpy"] = format(delta, "f")
                entry["review"].append(item)
            entry["review_status"] = "PRICE_COMPARISON"
        elif row["side"] == "SELL" and row["filled_quantity"]:
            entry["review_status"] = "EXECUTION_DATE_UNVERIFIED"
        else:
            entry["review_status"] = "NOT_AN_EXECUTED_SALE"
        out.append(entry)
    return {"schema_version": 1, "as_of": as_of.isoformat(), "status": "RECORDED_ORDERS_ONLY",
            "ledger_sha256": hashlib.sha256(raw).hexdigest(), "account_wide_coverage": False,
            "comparison_scope": "Price only; excludes tax, fees, dividends, benefits and reinvestment.",
            "orders": out}


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as out:
        temp = Path(out.name)
        try:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
            os.replace(temp, path)
        finally:
            temp.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--out", type=Path, default=Path(".private/trade_review") / REPORT)
    parser.add_argument("--as-of", type=instant)
    parser.add_argument("--no-market-fetch", action="store_true")
    imports = parser.add_mutually_exclusive_group()
    imports.add_argument("--append", type=Path, help="Private JSON array of verified order snapshots")
    imports.add_argument("--rakuten-orders-csv", type=Path)
    parser.add_argument("--observed-at", type=instant)
    parser.add_argument("--account-alias", default="rakuten-primary")
    parser.add_argument("--evidence-ref")
    parser.add_argument("--writeback", action="store_true")
    args = parser.parse_args()
    importing = args.append or args.rakuten_orders_csv
    if importing and (not args.ledger or args.writeback):
        parser.error("append requires a local ledger and cannot publish")
    now = args.as_of or datetime.now(timezone.utc)
    try:
        if importing:
            original = args.ledger.read_bytes() if args.ledger.exists() else b""
            if args.rakuten_orders_csv:
                if not args.observed_at or not args.evidence_ref:
                    raise ValueError("CSV import needs evidence timestamp and reference")
                rows = rakuten_csv_rows(args.rakuten_orders_csv.read_bytes(), observed_at=args.observed_at,
                                        recorded_at=now, account_alias=args.account_alias, evidence_ref=args.evidence_ref)
            else:
                rows = json.loads(args.append.read_text())
            if not isinstance(rows, list) or not rows or any(instant(r["recorded_at"]) > now for r in rows):
                raise ValueError("invalid or future import")
            updated = append_rows(original, rows)
            if updated != original:
                atomic_write(args.ledger, updated)
            if args.ledger.read_bytes() != updated:
                raise ValueError("ledger readback mismatch")
            print("APPEND_READBACK_OK")
            return
        source = args.ledger or download_named(LEDGER, args.out.parent / LEDGER, require_unique=True)
        payload = build_review(source.read_bytes(), now, None if args.no_market_fetch else yahoo_comparison)
    except Exception:
        if importing:
            print("TRADE_IMPORT_REJECTED")
            raise SystemExit(1) from None
        payload = {"as_of": now.isoformat(), "status": "UNAVAILABLE_OR_INVALID", "orders": [],
                   "account_wide_coverage": False}
    try:
        expected = (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode()
        atomic_write(args.out, expected)
        if args.writeback:
            upload_or_replace(args.out, REPORT, "application/json")
            with tempfile.TemporaryDirectory() as dest:
                observed = download_named(REPORT, Path(dest) / REPORT, require_unique=True).read_bytes()
            if observed != expected:
                raise ValueError("report readback mismatch")
    except Exception:
        print("PRIVATE_TRADE_REVIEW_WRITEBACK_FAILED")
        raise SystemExit(1) from None
    print(payload["status"])
    if payload["status"] == "UNAVAILABLE_OR_INVALID":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
