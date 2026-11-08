"""Audit private advice on every watch run. Public stdout contains status only."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .decision_journal import instant, read_events, replay
from .private_drive import download_named, upload_or_replace

JOURNAL = "decision_journal.jsonl"
REPORT = "decision_monitor_latest.json"


def audit_file(path: Path, as_of: datetime) -> dict:
    with path.open(encoding="utf-8") as handle:
        events = read_events(handle)
    rows = replay(events, as_of)
    for row in rows:
        row["due_soon"] = as_of < instant(row["review_by"]) <= as_of + timedelta(hours=4)
    attention = sum(row["decision_required"] or row["due_soon"] for row in rows)
    return {"schema_version": "1.0", "as_of": as_of.isoformat(),
            "status": "NO_PLANS" if not rows else "REVIEW_REQUIRED" if attention else "TRACKING",
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "plan_count": len(rows), "attention_count": attention, "items": rows,
            "coverage_note": "Registered advice only; not complete portfolio coverage or market safety."}


def write_report(payload: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / REPORT
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json_path.chmod(0o600)
    lines = ["# 判断の確認待ち", f"確認日時: {payload['as_of']}", f"状態: {payload['status']}",
             "登録済み判断のみの確認です。PF全体の監視完了を意味しません。", "",
             "| 対象 | 状態 | 次の期限 | 期限間近 |", "|---|---|---|---|"]
    for row in payload.get("items", []):
        # Values are private source data, not markdown instructions.
        cells = [str(row[k]).replace('|', '\\|').replace('\n', ' ') for k in ('symbol', 'status', 'review_by', 'due_soon')]
        lines.append("| " + " | ".join(cells) + " |")
    md = output / "decision_monitor_latest.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    md.chmod(0o600)


def run_monitor(workdir: Path, *, as_of: datetime | None = None,
                journal_path: Path | None = None, writeback: bool = False) -> dict:
    as_of = as_of or datetime.now(timezone.utc)
    workdir.mkdir(parents=True, exist_ok=True)
    try:
        source = journal_path or download_named(JOURNAL, workdir / JOURNAL, require_unique=True)
        source.chmod(0o600)
        payload = audit_file(source, as_of)
    except FileNotFoundError:
        payload = {"as_of": as_of.isoformat(), "status": "MISSING_JOURNAL", "items": []}
    except Exception:
        # Never publish exception text (it can contain file IDs, advice or credentials).
        payload = {"as_of": as_of.isoformat(), "status": "UNAVAILABLE_OR_INVALID", "items": []}
    write_report(payload, workdir)
    public = {"status": payload["status"], "writeback": "DISABLED"}
    if writeback:
        try:
            for name, mime in [(REPORT, "application/json"), ("decision_monitor_latest.md", "text/markdown")]:
                upload_or_replace(workdir / name, name, mime)
            public["writeback"] = "SUCCESS"
        except Exception:
            public["writeback"] = "FAILED"
    return public


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(".private/decision_monitor"))
    parser.add_argument("--journal", type=Path)
    parser.add_argument("--as-of")
    parser.add_argument("--writeback", action="store_true")
    args = parser.parse_args()
    result = run_monitor(args.workdir, as_of=instant(args.as_of) if args.as_of else None,
                         journal_path=args.journal, writeback=args.writeback)
    print(json.dumps(result))
    if result["status"] in {"MISSING_JOURNAL", "UNAVAILABLE_OR_INVALID"} or result["writeback"] == "FAILED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
