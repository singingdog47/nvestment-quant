from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FACTOR_COLUMNS = (
    "value_score",
    "quality_score",
    "growth_score",
    "momentum_score",
    "risk_score",
    "liquidity_score",
    "pre_score",
    "total_score",
    "score",
)

INPUT_PATHS = (
    Path("data/decision_context_latest.json"),
    Path("data/regime/market_regime_latest.json"),
    Path("data/intelligence/data_quality_latest.json"),
    Path("data/screening_latest.csv"),
    Path("data/quality_report.json"),
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _coerce_number(value: Any) -> Any:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def _top_screening(path: Path, limit: int = 10) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return []

    rank_column = next(
        (c for c in ("market_rank", "rank", "pre_score", "total_score", "score") if c in rows[0]),
        None,
    )
    if rank_column in ("pre_score", "total_score", "score"):
        rows.sort(key=lambda r: float(r.get(rank_column) or "-inf"), reverse=True)
    elif rank_column:
        rows.sort(key=lambda r: float(r.get(rank_column) or "inf"))

    out: list[dict[str, Any]] = []
    for row in rows[:limit]:
        item: dict[str, Any] = {
            "market": row.get("market"),
            "code": row.get("code") or row.get("ticker"),
            "ticker": row.get("ticker") or row.get("symbol"),
            "name": row.get("name"),
            "rank": _coerce_number(row.get(rank_column)) if rank_column else None,
            "price": _coerce_number(row.get("price") or row.get("close")),
        }
        factors = {
            c: _coerce_number(row.get(c))
            for c in FACTOR_COLUMNS
            if c in row and row.get(c) not in (None, "")
        }
        item["factors"] = factors
        out.append(item)
    return out


def _recommended_action(context: dict[str, Any]) -> str:
    policy = context.get("policy_guardrails") or {}
    gate = str(policy.get("decision_gate") or "").upper()
    if gate.startswith("BLOCK"):
        return "WAIT_DATA_QUALITY"
    explicit = context.get("recommended_action")
    if explicit:
        return str(explicit)
    return "REVIEW"


def capture_decision_snapshot(
    root: str | Path = ".",
    *,
    model_version: str = "1.7.0",
    top_n: int = 10,
) -> Path:
    """Persist the information set available at decision time.

    The record is intentionally public-safe: it does not include brokerage
    holdings or human trades. Human actions can be joined later from a private
    source by `decision_id`.
    """
    root = Path(root)
    context = _load_json(root / "data/decision_context_latest.json")
    now = _utcnow()

    regime = context.get("market_regime") or {}
    quality = context.get("quality") or {}
    policy = context.get("policy_guardrails") or {}

    input_manifest: list[dict[str, Any]] = []
    for rel in INPUT_PATHS:
        path = root / rel
        if path.exists():
            stat = path.stat()
            input_manifest.append(
                {
                    "path": str(rel),
                    "sha256": _sha256(path),
                    "size": stat.st_size,
                    "mtime_utc": datetime.fromtimestamp(
                        stat.st_mtime, tz=timezone.utc
                    ).isoformat(timespec="seconds"),
                }
            )
        else:
            input_manifest.append({"path": str(rel), "missing": True})

    top = _top_screening(root / "data/screening_latest.csv", limit=top_n)
    decision_basis = {
        "captured_at": now.isoformat(timespec="seconds"),
        "market_regime": regime.get("regime_label"),
        "regime_score": regime.get("regime_score"),
        "risk_flags": regime.get("regime_flags", []),
        "quality_score": quality.get("quality_score"),
        "data_actionable": quality.get("actionable"),
        "decision_gate": policy.get("decision_gate"),
        "recommended_action": _recommended_action(context),
        "top_screening": top,
        "model_version": model_version,
        "input_manifest": input_manifest,
    }
    decision_id = hashlib.sha256(
        json.dumps(decision_basis, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:20]

    record = {
        "schema_version": "1.0",
        "decision_id": decision_id,
        **decision_basis,
        "regime_components": regime.get("components", {}),
        "market_evidence": regime.get("evidence", {}),
        "policy_guardrails": {
            "absolute_defense_cash_jpy": policy.get("absolute_defense_cash_jpy"),
            "cash_target_range": policy.get("cash_target_range"),
            "max_single_stock_weight": policy.get("max_single_stock_weight"),
        },
        "quality": quality,
        "actual_human_action": None,
        "actual_human_action_note": "Private join field; do not commit brokerage activity to a public repository.",
        "outcomes": {},
    }

    out_dir = root / "data/validation/decisions" / now.strftime("%Y")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{now.strftime('%Y-%m-%d')}.json"

    if out_path.exists():
        existing = _load_json(out_path)
        if existing.get("decision_id") == decision_id:
            return out_path
        # Preserve multiple intraday observations without overwriting history.
        out_path = out_dir / f"{now.strftime('%Y-%m-%dT%H%M%SZ')}.json"

    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return out_path
