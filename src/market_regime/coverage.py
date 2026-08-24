from __future__ import annotations

from collections import Counter


PUBLIC_STATUSES = {"ok", "partial", "missing", "stale", "not_implemented"}
STATUS_ALIASES = {
    "error": "missing",
    "failed": "missing",
    "failure": "missing",
    "empty": "missing",
    "disabled": "not_implemented",
}


def normalize_status(value):
    status = str(value or "missing").strip().lower()
    status = STATUS_ALIASES.get(status, status)
    return status if status in PUBLIC_STATUSES else "partial"


def _spec(value):
    return {"source": value} if isinstance(value, str) else dict(value)


def build_data_coverage(
    health,
    *,
    generated_at,
    expected_sources=None,
    not_implemented=None,
    files=None,
):
    """Build a machine-readable manifest without inferring unavailable data."""
    expected = {
        item["source"]: item for item in map(_spec, expected_sources or [])
    }
    sources = []
    seen = set()

    for raw in health or []:
        entry = dict(raw)
        source = str(entry.get("source") or "unknown")
        spec = expected.get(source, {})
        entry["source"] = source
        entry["raw_status"] = str(entry.get("status") or "missing").lower()
        entry["status"] = normalize_status(entry.get("status"))
        entry["required"] = bool(spec.get("required", False))
        for key, value in spec.items():
            entry.setdefault(key, value)
        sources.append(entry)
        seen.add(source)

    for source, spec in expected.items():
        if source in seen:
            continue
        entry = dict(spec)
        entry.update(
            {
                "source": source,
                "status": "missing",
                "raw_status": "not_reported",
                "records": 0,
                "required": bool(spec.get("required", False)),
                "error": "expected source was not reported by the collector",
            }
        )
        sources.append(entry)

    for raw in not_implemented or []:
        entry = _spec(raw)
        source = str(entry.get("source") or "unknown")
        if source in seen or source in expected:
            continue
        entry.update(
            {
                "source": source,
                "status": "not_implemented",
                "raw_status": "not_implemented",
                "records": 0,
                "required": False,
            }
        )
        sources.append(entry)

    file_rows = []
    for raw in files or []:
        entry = dict(raw)
        entry["status"] = normalize_status(entry.get("status"))
        file_rows.append(entry)

    source_counts = Counter(x["status"] for x in sources)
    file_counts = Counter(x["status"] for x in file_rows)
    implemented = [x for x in sources if x["status"] != "not_implemented"]
    if not implemented or all(x["status"] == "missing" for x in implemented):
        overall = "missing"
    elif any(x["status"] != "ok" for x in implemented):
        overall = "partial"
    else:
        overall = "ok"

    critical_missing = [
        x["source"]
        for x in sources
        if x.get("required") and x["status"] != "ok"
    ]
    return {
        "schema_version": "1.0.0",
        "generated_at_utc": generated_at,
        "data_status": overall,
        "status_definitions": {
            "ok": "retrieval and content validation succeeded",
            "partial": "retrieval succeeded but content/coverage is incomplete",
            "missing": "no usable current or cached observation is available",
            "stale": "a prior observation is retained for audit only and excluded from scoring",
            "not_implemented": "the source is intentionally listed but not integrated",
        },
        "summary": {
            "sources": dict(sorted(source_counts.items())),
            "files": dict(sorted(file_counts.items())),
            "critical_missing": critical_missing,
        },
        "sources": sources,
        "files": file_rows,
    }

