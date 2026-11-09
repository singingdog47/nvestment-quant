"""Production ingestion -> historical ledger -> state -> private decision report.

Availability of the runtime is separate from completeness of brokerage evidence.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from src.private_rakuten_e2e import verify_historical_files


def prepare_ledger(candidates, manifest, account_inputs, private_dir):
    from src.private_account_import import parse_orders_document
    ledger = Path(private_dir) / "verified_facts.jsonl"
    # Source selection is anchored to the holdings export, not upload time.
    source_name = manifest.get("source_file")
    csv = next((p for p, m in candidates if m.get("name") == source_name), None)
    buying_name = (account_inputs.get("inputs", {}).get("buying_power") or {}).get("source_file")
    buying = next((p for p, m in candidates if m.get("name") == buying_name), None)
    documents = {}
    for path, meta in candidates:
        if path.suffix.lower() != ".pdf":
            continue
        try:
            doc = parse_orders_document(path)
        except Exception:
            continue
        scope = doc["scope"]
        if scope not in documents or doc["source_as_of"] > documents[scope][0]:
            documents[scope] = (doc["source_as_of"], path)
    domestic = documents.get("orders_domestic_cash_document", (None, None))[1]
    fund = documents.get("orders_mutual_funds_document", (None, None))[1]
    if any(p is None for p in (csv, buying, domestic, fund)):
        return {"status": "SOURCE_SET_INCOMPLETE", "ledger_path": str(ledger)}
    try:
        result = verify_historical_files(csv, buying, domestic, fund, ledger)
        return {**result, "ledger_path": str(ledger)}
    except Exception:
        return {"status": "SOURCE_VERIFICATION_FAILED", "ledger_path": str(ledger)}


def write_private_event_review(local_portfolio, private_dir: Path, *, now):
    """Fail closed on unknown disclosures; private file only, no network or public artifacts."""
    import csv
    import re
    from src.decision_event_review_bridge import prepare_decision_review

    with open(local_portfolio, encoding="utf-8-sig", newline="") as handle:
        codes = [str(row.get("code", "")).strip()
                 for row in csv.DictReader(handle)]
    symbols = list(dict.fromkeys(code for code in codes if re.fullmatch(r"\d{4}", code)))
    # Never infer that a missing manifest means no events.
    manifest_path = private_dir / "event_disclosures_verified.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    consent_path = private_dir / "event_review_consent.json"
    consent = json.loads(consent_path.read_text(encoding="utf-8")) if consent_path.exists() else None
    result = prepare_decision_review(symbols, manifest, now.isoformat(), consent)
    output = private_dir / "event_review_latest.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output.chmod(0o600)
    return {"analysis_mode": result["analysis_mode"],
            "total": result["event_preflight"]["total"],
            "unverified": result["event_preflight"]["blocked"],
            "private_report": str(output),
            "may_execute_orders": False}


def assess_sources(candidates, private_dir: Path, *, now=None):
    from src.run_portfolio_risk import _build_latest_portfolio, _build_latest_account_inputs, _write_shared_investment_state
    from src.portfolio_policy_report import write_policy_report
    from src.private_horizon_decision import write_private_matrix
    now = now or datetime.now(timezone.utc)
    private_dir.mkdir(parents=True, exist_ok=True)
    local, manifest = _build_latest_portfolio(private_dir, candidates)
    matching = [(p, m) for p, m in candidates if m.get("name") == manifest["source_file"]]
    inputs = _build_latest_account_inputs(private_dir, matching + [x for x in candidates if x not in matching])
    verified = prepare_ledger(candidates, manifest, inputs, private_dir)
    os.environ["PRIVATE_VERIFIED_FACTS_LEDGER_PATH"] = verified["ledger_path"]
    # Dedicated report publisher below owns writeback; avoid double writers.
    previous = os.environ.get("INVESTMENT_STATE_DRIVE_WRITEBACK")
    os.environ["INVESTMENT_STATE_DRIVE_WRITEBACK"] = "false"
    try:
        policy = write_policy_report(local, inputs, private_dir)
        shared = _write_shared_investment_state(private_dir, inputs, manifest, policy, now=now)
    finally:
        if previous is None:
            os.environ.pop("INVESTMENT_STATE_DRIVE_WRITEBACK", None)
        else:
            os.environ["INVESTMENT_STATE_DRIVE_WRITEBACK"] = previous
    event_review = write_private_event_review(local, private_dir, now=now)
    matrix = write_private_matrix(local, source_as_of=manifest.get("source_as_of"),
        policy_payload=policy, investment_state=shared["state"], output_dir=private_dir)
    return {"runtime_status": "PASSED", "as_of": now.isoformat(),
            "source_as_of": manifest.get("source_as_of"),
            "holdings_rows": manifest.get("rows_kept"),
            "source_verification": {k:v for k,v in verified.items() if k != "ledger_path"},
            "source_coherence": shared["state"]["source_coherence"],
            "ledger_coverage": shared["state"].get("private_ledger_audit"),
            "open_order_count": shared["state"]["open_orders"]["count"],
            "decision_report": matrix,
            "event_review": event_review,
            "data_ready": (verified.get("account_wide_orders_verified") is True
                           and verified.get("settlement_verified") is True
                           and shared["state"]["source_coherence"]["decision_safe"] is True),
            "note": "Runtime pass does not prove complete/current order or settlement coverage."}


def main():
    from src.private_drive import download_recent_files, download_latest_assetbalance, upload_or_replace, download_named
    from src.private_decision_monitor import run_monitor
    private_dir = Path(".private/readiness")
    public = {"runtime_status": "FAILED", "writeback": "FAILED"}
    try:
        candidates = download_recent_files(private_dir / "inbox", limit=50)
        latest = download_latest_assetbalance(private_dir / "latest")
        if latest and not any(m.get("id") == latest[1].get("id") for _, m in candidates):
            candidates.append(latest)
        report = assess_sources(candidates, private_dir)
        path = private_dir / "private_readiness_latest.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        path.chmod(0o600)
        upload_or_replace(path, path.name, "application/json")
        readback = download_named(path.name, private_dir / "readback.json", require_unique=True)
        if readback.read_bytes() != path.read_bytes():
            raise ValueError("readiness report readback mismatch")
        public = {"runtime_status": "PASSED", "writeback": "SUCCESS", "data_ready": report["data_ready"]}
        public["decision_monitor"] = run_monitor(private_dir / "monitor", writeback=True)
        if public["decision_monitor"]["writeback"] != "SUCCESS" or public["decision_monitor"]["status"] in {"MISSING_JOURNAL", "UNAVAILABLE_OR_INVALID"}:
            public["runtime_status"] = "FAILED"
    except Exception as exc:
        public["error_type"] = type(exc).__name__
    print(json.dumps(public))
    if public["runtime_status"] != "PASSED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
