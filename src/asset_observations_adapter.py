"""Asset-class-neutral verified observations.

Source adapters normalize brokerage, bank, crypto, FX, and other records into
facts without assuming that missing fields mean zero. No public account data.
"""
from __future__ import annotations

from import_verified_snapshot import import_verified_snapshot


def import_asset_observations(payload: dict, ledger_path: str) -> dict:
    """Import a verified observation from any asset class or account scope.

    A value is a structured observation with unit, type, and optional currency.
    The source's coverage is explicit and never interpreted as account-wide.
    """
    source = payload.get("source") or {}
    if source.get("verified") is not True or source.get("coherence_verified") is not True:
        raise ValueError("Verified source and coherence evidence required")
    for key in ("observed_at", "evidence_ref", "scope", "asset_class", "account_ref"):
        if not isinstance(source.get(key), str) or not source[key].strip():
            raise ValueError("Missing source metadata: " + key)
    observations = payload.get("observations")
    if not isinstance(observations, list) or not observations:
        raise ValueError("Nonempty observations required")
    facts = []
    for observation in observations:
        if not isinstance(observation, dict):
            raise ValueError("Observation must be an object")
        for key in ("entity_ref", "metric", "value", "unit"):
            if key not in observation or observation[key] is None or observation[key] == "":
                raise ValueError("Missing observation field: " + key)
        metric = str(observation["metric"])
        entity = str(observation["entity_ref"])
        if not metric.strip() or not entity.strip():
            raise ValueError("Entity and metric must be nonempty")
        facts.append({
            "key": f"{source['account_ref']}:{source['asset_class']}:{entity}:{metric}",
            "scope": source["scope"],
            "value": {"amount": observation["value"], "unit": observation["unit"],
                      "currency": observation.get("currency"),
                      "coverage": source.get("coverage", "unknown")},
            "supersedes": observation.get("supersedes"),
        })
    return import_verified_snapshot({
        "verification_status": "verified",
        "observed_at": source["observed_at"],
        "evidence_ref": source["evidence_ref"],
        "quality": {"source_verified": True, "coherence_verified": True,
                    "source_scope": source["scope"]},
        "facts": facts,
    }, ledger_path)
