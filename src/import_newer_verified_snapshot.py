"""Prepare explicit supersession links for a new verified asset snapshot.

Only verified upstream observations are accepted. The importer remains the
final validator; this helper never authorizes trading.
"""
from __future__ import annotations

from datetime import datetime

from import_verified_snapshot import import_verified_snapshot
from verified_facts_ledger import FactConflict, read_verified_facts


def import_newer_verified_snapshot(snapshot: dict, ledger_path: str) -> dict:
    if snapshot.get("verification_status") != "verified":
        raise ValueError("Unverified snapshot cannot be automatically superseded")
    quality = snapshot.get("quality") or {}
    if quality.get("source_verified") is not True or quality.get("coherence_verified") is not True:
        raise ValueError("Upstream source and coherence verification required")
    if not isinstance(snapshot.get("evidence_ref"), str) or not snapshot["evidence_ref"].strip():
        raise ValueError("Concrete evidence reference required")
    timestamp = datetime.fromisoformat(str(snapshot.get("observed_at", "")).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Timezone required")
    current = read_verified_facts(ledger_path)
    prepared = []
    for fact in snapshot.get("facts") or []:
        if not isinstance(fact, dict) or not isinstance(fact.get("key"), str):
            raise ValueError("Invalid fact")
        old = current.get(fact["key"])
        new_fact = dict(fact)
        if old is not None:
            previous = datetime.fromisoformat(old["observed_at"].replace("Z", "+00:00"))
            if timestamp <= previous:
                raise FactConflict("Automatic supersession requires strictly newer observation")
            if old["scope"] != fact.get("scope"):
                raise FactConflict("Scope changed; manual reconciliation required")
            supplied = fact.get("supersedes")
            if supplied is not None and supplied != old["fact_id"]:
                raise FactConflict("Conflicting explicit supersession")
            new_fact["supersedes"] = old["fact_id"]
        elif fact.get("supersedes") is not None:
            raise FactConflict("Cannot supersede a nonexistent fact")
        prepared.append(new_fact)
    payload = {**snapshot, "facts": prepared}
    return import_verified_snapshot(payload, ledger_path)
