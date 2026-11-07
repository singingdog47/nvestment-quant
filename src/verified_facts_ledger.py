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


def append_verified_facts(path: str | Path, facts: list[dict]) -> list[dict]:
    """Validate a batch against the complete ledger, then atomically replace file.

    Concurrent writers must be serialized by the caller; no cross-process lock.
    """
    import os
    import tempfile

    if not facts:
        raise ValueError("Empty fact batch")
    p = Path(path)
    current = read_verified_facts(p)
    rows = []
    now = datetime.now(timezone.utc).isoformat()
    for item in facts:
        key, value = item["key"], item["value"]
        observed_at, evidence_ref, scope = item["observed_at"], item["evidence_ref"], item["scope"]
        supersedes = item.get("supersedes")
        if not all(isinstance(x, str) and x.strip() for x in (key, observed_at, evidence_ref, scope)):
            raise ValueError("key, observed_at, evidence_ref and scope are required")
        stamp = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError("observed_at must include timezone")
        old = current.get(key)
        if old:
            old_stamp = datetime.fromisoformat(old["observed_at"].replace("Z", "+00:00"))
            if stamp < old_stamp:
                raise FactConflict("Cannot supersede with an older observation")
            if _canonical(old["value"]) != _canonical(value):
                if supersedes != old["fact_id"]:
                    raise FactConflict("Conflicting fact requires explicit supersedes reference")
            elif supersedes is not None and supersedes != old["fact_id"]:
                raise FactConflict("Supersedes reference does not match active fact")
        elif supersedes is not None:
            raise FactConflict("Cannot supersede missing fact")
        row = {"key": key, "value": value, "observed_at": observed_at,
               "evidence_ref": evidence_ref, "scope": scope,
               "supersedes": supersedes, "recorded_at_utc": now}
        row["fact_id"] = hashlib.sha256(_canonical({k: v for k, v in row.items() if k != "recorded_at_utc"}).encode()).hexdigest()
        if not old or old["fact_id"] != row["fact_id"]:
            rows.append(row)
            current[key] = row
    if not rows:
        return [current[item["key"]] for item in facts]
    p.parent.mkdir(parents=True, exist_ok=True)
    existing = p.read_bytes() if p.exists() else b""
    if existing and not existing.endswith(b"\n"):
        raise FactConflict("Ledger has incomplete trailing record")
    data = existing + "".join(_canonical(row) + "\n" for row in rows).encode("utf-8")
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(dir=p.parent, prefix=".facts-", delete=False) as tmp:
            temp_name = tmp.name
            os.chmod(temp_name, 0o600)
            tmp.write(data)
            tmp.flush()
            os.fsync(tmp.fileno())
        os.replace(temp_name, p)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
    return [current[item["key"]] for item in facts]


def append_verified_fact(path: str | Path, *, key: str, value: object,
                         observed_at: str, evidence_ref: str,
                         scope: str, supersedes: str | None = None) -> dict:
    return append_verified_facts(path, [{
        "key": key, "value": value, "observed_at": observed_at,
        "evidence_ref": evidence_ref, "scope": scope, "supersedes": supersedes,
    }])[0]


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
