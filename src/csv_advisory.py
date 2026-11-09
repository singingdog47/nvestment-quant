"""CSV-first advisory cash; never certify broker buying power or settlement."""
from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone

from src.private_account_import import reconcile_account_components

JST = timezone(timedelta(hours=9))
DECLARATION_NAME = "private_order_declaration.json"


def fresh(stamp, now):
    try:
        value = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        return (value.tzinfo is not None
                and value.astimezone(JST).date() == now.astimezone(JST).date()
                and 0 <= (now - value).total_seconds() <= 8 * 3600)
    except (TypeError, ValueError):
        return False


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def build_csv_advisory(account_inputs, candidates=(), *, now=None, reserve_jpy=500000):
    now = now or datetime.now(timezone.utc)
    inputs = account_inputs.get("inputs", {})
    account = inputs.get("account_summary", {})
    reconciled = reconcile_account_components(account).get("status") == "RECONCILED_HISTORICAL"
    current = fresh(account.get("source_as_of"), now)
    cash = number(account.get("cash_deposit_jpy"))
    bank = number(account.get("rakuten_bank_jpy"))
    total = cash + bank if cash is not None and bank is not None else None
    ready = reconciled and current and total is not None and cash >= 0 and bank >= 0

    declarations = []
    for path, meta in candidates:
        if meta.get("name") != DECLARATION_NAME:
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
            if (isinstance(d, dict) and d.get("source") == "user_statement"
                    and d.get("scope") == "all_open_orders"
                    and type(d.get("count")) is int and d["count"] == 0
                    and fresh(d.get("observed_at"), now)):
                declarations.append(d)
        except (OSError, ValueError):
            continue
    declaration = max(declarations, key=lambda d: d["observed_at"], default=None)
    conflicts = []
    # A same-day open order in any parsed document must not be erased by a
    # zero declaration. Older PDFs remain historical evidence only.
    from src.private_account_import import summarize_open_orders
    docs = list(account_inputs.get("order_documents", {}).values())
    docs.append(inputs.get("orders", {}))
    for doc in docs:
        if fresh(doc.get("source_as_of"), now) and isinstance(doc.get("items"), list):
            open_items, count = summarize_open_orders(doc["items"])
            if open_items or count is None:
                conflicts.append("DOCUMENT_HAS_OPEN_ORDERS")
    buying = inputs.get("buying_power", {})
    broker_value = number(buying.get("cash_buying_power_jpy"))
    # Field used by the existing Rakuten PDF parser.
    if broker_value is None:
        broker_value = number(buying.get("domestic_cash_buying_power_jpy"))
    comparison = "NOT_AVAILABLE_OPTIONAL"
    if fresh(buying.get("source_as_of"), now) and broker_value is not None and total is not None:
        comparison = "MATCH" if abs(total - broker_value) < 1 else "DIFFERENT_REQUIRES_REVIEW"
        if comparison != "MATCH":
            conflicts.append("BROKER_BUYING_POWER_DIFFERS_FROM_CSV_CASH")
    planning = ready and declaration is not None and not conflicts
    return {
        "analysis_ready": bool(ready),
        "analysis_status": "READY_WITH_LIMITS" if ready else "CSV_MISSING_STALE_OR_UNRECONCILED",
        "capital_planning_ready": bool(planning),
        "source_as_of": account.get("source_as_of"),
        "cash_and_bank_jpy": total if ready else None,
        "defense_reserve_jpy": reserve_jpy,
        "planning_cash_after_reserve_jpy": max(0, total - reserve_jpy) if planning else None,
        "broker_buying_power_comparison": comparison,
        "orders": {"count": 0 if declaration and not conflicts else None,
                   "source": "user_statement" if declaration else "unconfirmed",
                   "observed_at": declaration.get("observed_at") if declaration else None,
                   "broker_verified": False},
        "conflicts": sorted(set(conflicts)),
        "buying_power_pdf_required_for_analysis": False,
        "execution_ready": False,
        "limits": ["Cash estimate excludes margin collateral and FX collateral.",
                   "Not broker-certified buying power; settlement and household spending remain separate.",
                   "Zero-order declaration expires on the same JST day or after eight hours; update after an order change."],
    }
