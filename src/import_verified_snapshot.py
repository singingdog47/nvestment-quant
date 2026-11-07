"""Import explicitly verified private brokerage observations into the facts ledger.

The input is a private JSON document, never a public repository fixture.
Unknown order scope is retained as unknown, never interpreted as zero orders.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from verified_facts_ledger import append_verified_fact, read_verified_facts, FactConflict


def import_verified_snapshot(snapshot: dict, ledger_path: str | Path) -> dict:
    if snapshot.get("verification_status") != "verified":
        raise ValueError("Snapshot must be explicitly verified before ledger import")
    observed_at = snapshot.get("observed_at")
    evidence_ref = snapshot.get("evidence_ref")
    if not isinstance(snapshot.get("facts"), list) or not snapshot["facts"]:
        raise ValueError("Snapshot must contain verified facts")
    if not observed_at or not evidence_ref:
        raise ValueError("Snapshot observation time and evidence reference required")
    timestamp = datetime.fromisoformat(str(observed_at).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Observation timestamp requires timezone")
    # Caller-provided "verified" is insufficient for execution-sensitive facts.
    # Reconciliation status must be independently supplied by the upstream
    # brokerage parser; this importer cannot infer completeness itself.
    quality = snapshot.get("quality") or {}
    if quality.get("source_verified") is not True:
        raise ValueError("Upstream source verification required")
    if quality.get("coherence_verified") is not True:
        raise ValueError("Upstream source coherence verification required")
    if quality.get("source_scope") not in ("domestic_cash_equities", "fund_orders", "account_summary", "buying_power"):
        raise ValueError("Explicit supported source scope required")
    facts = snapshot["facts"]
    keys = [fact.get("key") for fact in facts]
    if any(not isinstance(k, str) or not k.strip() for k in keys) or len(keys) != len(set(keys)):
        raise ValueError("Fact keys must be nonempty and unique")
    # Validate the complete batch before any persistent writes.
    current = read_verified_facts(ledger_path)
    for fact in facts:
        key = fact["key"]
        if "value" not in fact or not fact.get("scope"):
            raise ValueError("Fact value and scope are required")
        existing = current.get(key)
        if existing and timestamp < datetime.fromisoformat(existing["observed_at"].replace("Z", "+00:00")):
            raise FactConflict("Snapshot observation older than verified fact")
        if existing and existing["value"] != fact["value"]:
            if fact.get("supersedes") != existing["fact_id"]:
                raise FactConflict("Conflicting fact requires explicit supersession")
    imported = []
    for fact in facts:
        imported.append(append_verified_fact(
            ledger_path, key=fact["key"], value=fact["value"],
            scope=fact["scope"], observed_at=observed_at,
            evidence_ref=evidence_ref, supersedes=fact.get("supersedes")))
    return {"status": "ok", "facts_imported": len(imported),
            "ledger_path": str(ledger_path), "source_as_of": observed_at}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.snapshot.read_text(encoding="utf-8"))
    print(json.dumps(import_verified_snapshot(payload, args.ledger), ensure_ascii=False))


if __name__ == "__main__":
    main()
