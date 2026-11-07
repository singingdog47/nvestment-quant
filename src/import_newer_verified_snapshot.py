"""Atomically import strictly newer verified observations into a private ledger.

Verification flags are upstream assertions, not independent proof of authenticity.
This module never authorizes trading.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from verified_facts_ledger import append_verified_facts


def import_newer_verified_snapshot(snapshot: dict, ledger_path: str | Path) -> dict:
    if snapshot.get("verification_status") != "verified":
        raise ValueError("Unverified snapshot cannot be automatically superseded")
    quality = snapshot.get("quality") or {}
    if quality.get("source_verified") is not True or quality.get("coherence_verified") is not True:
        raise ValueError("Upstream source and coherence verification required")
    scope = quality.get("source_scope")
    if not isinstance(scope, str) or not scope.strip():
        raise ValueError("Explicit source scope required")
    evidence = snapshot.get("evidence_ref")
    if not isinstance(evidence, str) or not evidence.strip():
        raise ValueError("Concrete evidence reference required")
    observed_at = snapshot.get("observed_at")
    if not isinstance(observed_at, str):
        raise ValueError("Observation timestamp required")
    timestamp = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Timezone required")
    facts = snapshot.get("facts")
    if not isinstance(facts, list) or not facts:
        raise ValueError("Snapshot must contain verified facts")
    keys = [fact.get("key") for fact in facts if isinstance(fact, dict)]
    if len(keys) != len(facts) or any(not isinstance(k, str) or not k.strip() for k in keys) or len(set(keys)) != len(keys):
        raise ValueError("Fact keys must be nonempty and unique")
    batch = []
    for fact in facts:
        if "value" not in fact or not isinstance(fact.get("scope"), str) or not fact["scope"].strip():
            raise ValueError("Fact value and scope are required")
        batch.append({"key": fact["key"], "value": fact["value"],
                      "scope": fact["scope"], "observed_at": observed_at,
                      "evidence_ref": evidence, "supersedes": fact.get("supersedes")})
    # Read, validate, determine supersession, and write under the same lock.
    imported = append_verified_facts(ledger_path, batch, auto_supersede=True)
    return {"status": "ok", "facts_imported": len(imported),
            "ledger_path": str(ledger_path), "source_as_of": observed_at}
