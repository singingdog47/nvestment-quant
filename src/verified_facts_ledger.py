"""Private, append-only verified facts ledger. Never store brokerage data in public git."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class FactConflict(ValueError):
    pass


def _canonical(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def append_verified_fact(path: str | Path, *, key: str, value: object,
                         observed_at: str, evidence_ref: str,
                         scope: str, supersedes: str | None = None) -> dict:
    """Append evidence-backed fact. Conflicting updates require explicit supersession."""
    if not all(isinstance(x, str) and x.strip() for x in (key, observed_at, evidence_ref, scope)):
        raise ValueError("key, observed_at, evidence_ref and scope are required")
    stamp = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("observed_at must include timezone")
    p = Path(path)
    previous = read_verified_facts(p)
    active = previous.get(key)
    if active and _canonical(active["value"]) != _canonical(value):
        if supersedes != active["fact_id"]:
            raise FactConflict("Conflicting fact requires explicit supersedes reference")
        if stamp < datetime.fromisoformat(active["observed_at"].replace("Z", "+00:00")):
            raise FactConflict("Cannot supersede with an older observation")
    elif supersedes is not None and (not active or supersedes != active["fact_id"]):
        raise FactConflict("Supersedes reference does not match active fact")
    record = {"key": key, "value": value, "observed_at": observed_at,
              "evidence_ref": evidence_ref, "scope": scope,
              "supersedes": supersedes, "recorded_at_utc": datetime.now(timezone.utc).isoformat()}
    record["fact_id"] = hashlib.sha256(_canonical({k: v for k, v in record.items() if k != "recorded_at_utc"}).encode()).hexdigest()
    if active and active["fact_id"] == record["fact_id"]:
        return active
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(_canonical(record) + "\n")
    return record


def read_verified_facts(path: str | Path) -> dict[str, dict]:
    """Validate full chain; reject malformed or untraceable changes."""
    p = Path(path)
    if not p.exists():
        return {}
    current: dict[str, dict] = {}
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        digest = hashlib.sha256(_canonical({k: v for k, v in row.items() if k not in ("fact_id", "recorded_at_utc")}).encode()).hexdigest()
        if row.get("fact_id") != digest:
            raise FactConflict("Ledger integrity check failed")
        old = current.get(row["key"])
        if old and _canonical(old["value"]) != _canonical(row["value"]):
            if row.get("supersedes") != old["fact_id"]:
                raise FactConflict("Ledger contains unapproved fact replacement")
        current[row["key"]] = row
    return current
