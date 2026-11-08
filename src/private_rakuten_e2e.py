"""Local-only Rakuten real-file historical E2E; never commits or uploads source data.

Usage: python -m src.private_rakuten_e2e --csv FILE --buying-power-pdf FILE
       --domestic-orders-pdf FILE --fund-orders-pdf FILE --ledger PRIVATE_PATH

This verifies only supplied document coverage, never account-wide completeness.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from src.private_account_import import (parse_account_summary_bytes,
                                        parse_buying_power_pdf,
                                        reconcile_account_components,
                                        source_as_of)
from src.verified_facts_ledger import append_verified_facts, read_verified_facts
from src.advisory_continuity import classify_advisory_continuity


def _digest(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise ValueError("Source must be a regular non-symlink file")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pdf_text(path: Path) -> str:
    import fitz
    with fitz.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)


def verify_historical_files(csv_path: Path, buying_pdf: Path, domestic_pdf: Path,
                            fund_pdf: Path, ledger_path: Path) -> dict:
    sources = [csv_path, buying_pdf, domestic_pdf, fund_pdf]
    if any(not p.is_file() or p.is_symlink() for p in sources):
        raise ValueError("Missing or symlinked source")
    # A reused path could falsely count one document as multiple independent
    # sources. Distinct paths alone are insufficient: reject identical bytes.
    if len({p.resolve() for p in sources}) != len(sources):
        raise ValueError("Source paths must be distinct")
    source_hashes = [_digest(p) for p in sources]
    if len(set(source_hashes)) != len(source_hashes):
        raise ValueError("Duplicate source content across required documents")
    stamp, method = source_as_of(csv_path.name, None)
    if method != "filename_embedded_export_time" or stamp is None:
        raise ValueError("CSV requires an explicit export timestamp")
    if datetime.fromisoformat(stamp).tzinfo is None:
        raise ValueError("Naive CSV observation time")
    raw = csv_path.read_bytes()
    parsed = parse_account_summary_bytes(raw)
    balance = reconcile_account_components(parsed)
    if balance["status"] != "RECONCILED_HISTORICAL":
        raise ValueError("Account balance reconciliation failed")
    buying = parse_buying_power_pdf(buying_pdf)
    if buying["source_as_of"] is None:
        raise ValueError("Buying power PDF requires explicit year in footer")
    if abs((datetime.fromisoformat(stamp) -
            datetime.fromisoformat(buying["source_as_of"])).total_seconds()) > 3600:
        raise ValueError("CSV/PDF source timestamp skew > 1h")
    buying_text = _pdf_text(buying_pdf)
    domestic_text = _pdf_text(domestic_pdf)
    fund_text = _pdf_text(fund_pdf)
    # Require the document-specific headings and dated footer. This is NOT
    # proof that the order list includes every account or asset class.
    for label, content, marker in [
        ("domestic", domestic_text, "注文一覧"),
        ("fund", fund_text, "購入・売却履歴"),
    ]:
        if marker not in content or not re.search(r"20\d\d/\d\d/\d\d\s+\d\d:\d\d", content):
            raise ValueError(f"{label} order PDF missing expected heading/year")
    bank = re.search(r"楽天銀行普通預金残高\s*([\d,]+)", buying_text)
    if not bank or int(bank.group(1).replace(",", "")) != int(parsed.get("rakuten_bank_jpy", -1)):
        # The CSV parser does not expose bank balance: read the exact summary
        # line from source bytes, never infer from buying power.
        import csv as csvmod
        import io
        from src.portfolio_import import decode_rakuten_bytes
        decoded, _ = decode_rakuten_bytes(raw)
        rows = csvmod.reader(io.StringIO(decoded))
        bank_csv = next((int(row[1].replace(",", "")) for row in rows
                         if len(row) > 1 and row[0] == "楽天銀行普通預金残高"), None)
        if not bank or bank_csv is None or int(bank.group(1).replace(",", "")) != bank_csv:
            raise ValueError("Rakuten bank balance CSV/PDF mismatch")
    digests = source_hashes
    # Source hashes are provenance labels, not independent broker signatures.
    facts = [
        {"key": "rakuten_historical:account_summary",
         "value": {k: v for k, v in parsed.items() if k != "source_encoding"},
         "observed_at": stamp, "scope": "account_summary",
         "evidence_ref": "private:sha256:" + digests[0]},
        {"key": "rakuten_historical:buying_power",
         "value": {k: v for k, v in buying.items() if k != "status"},
         "observed_at": buying["source_as_of"], "scope": "buying_power",
         "evidence_ref": "private:sha256:" + digests[1]},
    ]
    # Record both order PDFs as *document evidence only*, never as proof
    # of complete orders or parsed fills. Each has its own dated footer.
    for label, content, digest, scope in [
        ("domestic", domestic_text, digests[2], "orders_domestic_cash_document"),
        ("fund", fund_text, digests[3], "orders_mutual_funds_document"),
    ]:
        # Only a trailing print/footer timestamp can date a document.
        # Transaction timestamps in the order table are NOT export times.
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        footer = "\n".join(lines[-8:])
        # Printed Rakuten PDFs end with a dated browser-print footer followed
        # by a page counter. An order-table date is not acceptable evidence.
        footer_match = re.search(
            r"(20\d{2}/\d{2}/\d{2}\s+\d{2}:\d{2})\s+\d+\s*/\s*\d+\s*ページ\s*$",
            footer,
        )
        if not footer_match:
            raise ValueError(f"{label} PDF lacks explicit footer timestamp/page counter")
        doc_time = datetime.strptime(footer_match.group(1), "%Y/%m/%d %H:%M")
        doc_time = doc_time.replace(tzinfo=datetime.fromisoformat(stamp).tzinfo)
        if abs((datetime.fromisoformat(stamp) - doc_time).total_seconds()) > 3600:
            raise ValueError(f"{label} order PDF timestamp skew > 1h")
        facts.append({
            "key": "rakuten_historical:" + scope,
            "value": {"document_present": True, "order_rows_verified": False,
                      "account_wide_coverage_verified": False},
            "observed_at": doc_time.isoformat(), "scope": scope,
            "evidence_ref": "private:sha256:" + digest,
        })
    # Write only after all checks pass; no real order identifiers in public CI.
    if ledger_path.resolve() in [p.resolve() for p in sources]:
        raise ValueError("Ledger path must differ from source")
    existing = read_verified_facts(ledger_path)
    pending = []
    for fact in facts:
        old = existing.get(fact["key"])
        if old and all(old.get(k) == fact[k] for k in
                       ("key", "value", "observed_at", "scope", "evidence_ref")):
            continue  # Exact historical replay is idempotent.
        pending.append(fact)
    if pending:
        append_verified_facts(ledger_path, pending, auto_supersede=True)
    actual = read_verified_facts(ledger_path)
    # Read-back must establish provenance and observation identity, not just
    # coincidentally matching numeric values.
    fields = ("value", "observed_at", "scope", "evidence_ref")
    if any(any(actual.get(f["key"], {}).get(field) != f[field]
               for field in fields) for f in facts):
        raise ValueError("Private ledger read-back mismatch")
    advisory = classify_advisory_continuity(
        verified_scopes=["account_summary", "buying_power",
                         "orders_domestic_cash_document", "orders_mutual_funds_document"],
        missing_scopes=["orders_foreign_equities", "cash_and_settlement",
                        "account_wide_order_coverage"],
        conflicting_scopes=[], stale_scopes=[])
    return {"advisory": advisory, "status": "HISTORICAL_PARTIAL_COVERAGE",
            "source_count": 4, "ledger_facts_verified": len(facts),
            "account_reconciliation": balance["status"],
            "bank_balance_crosschecked": True,
            "orders_documents_checked": ["domestic_cash", "mutual_funds"],
            "account_wide_orders_verified": False,
            "settlement_verified": False, "deployable_cash_jpy": None,
            "execution_ready": False}


def main() -> None:
    parser = argparse.ArgumentParser()
    for arg in ("csv", "buying-power-pdf", "domestic-orders-pdf",
                "fund-orders-pdf", "ledger"):
        parser.add_argument("--" + arg, required=True, type=Path)
    args = parser.parse_args()
    result = verify_historical_files(args.csv, args.buying_power_pdf,
                                     args.domestic_orders_pdf,
                                     args.fund_orders_pdf, args.ledger)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
