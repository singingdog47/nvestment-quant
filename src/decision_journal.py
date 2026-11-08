"""Private append-only decision revisions, observations and explicit reviews.

Run with python -m src.decision_journal. No brokerage actions or public exports.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import math
import os
from datetime import datetime
from pathlib import Path

from .decision_checkpoint import review_rule


def instant(value: str) -> datetime:
    result = datetime.fromisoformat(value)
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamps require a timezone")
    return result


def text_field(event: dict, key: str) -> str:
    value = event.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing {key}")
    return value


def positive(value) -> float:
    if isinstance(value, bool):
        raise ValueError("invalid price")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid price") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError("invalid price")
    return number


def replay(events: list[dict], as_of: datetime) -> list[dict]:
    """Validate the whole journal, but evaluate only information known by as_of.

    PLAN replaces an active revision only with an explicit reason and link.
    REVIEW resolves prior observed triggers; a later trigger requires review again.
    ACT recommendations remain pending until a subsequent explicit review.
    """
    if as_of.tzinfo is None:
        raise ValueError("as_of requires a timezone")
    active, visible, ids = {}, {}, set()
    previous_time = None
    for event in events:
        event_id = text_field(event, "id")
        if event_id in ids:
            raise ValueError("duplicate event id")
        ids.add(event_id)
        recorded = instant(text_field(event, "recorded_at"))
        if previous_time and recorded < previous_time:
            raise ValueError("journal is not chronological")
        previous_time = recorded
        symbol = text_field(event, "symbol")
        kind = event.get("type")
        state = active.get(symbol)
        if kind == "PLAN":
            for field in ("rationale", "falsifier", "evidence", "recommendation"):
                text_field(event, field)
            if event["recommendation"] not in {"HOLD", "TRIM", "EXIT", "BUY", "WAIT"}:
                raise ValueError("invalid recommendation")
            if event.get("basis") not in {"CLOSE", "INTRADAY"}:
                raise ValueError("explicit price basis required")
            if event.get("comparator") not in {"AT_OR_BELOW", "AT_OR_ABOVE"}:
                raise ValueError("invalid comparator")
            positive(event.get("threshold"))
            due = instant(text_field(event, "review_by"))
            if due <= recorded:
                raise ValueError("review deadline must be in the future")
            if state:
                if event.get("supersedes") != state["plan"]["id"]:
                    raise ValueError("revision must link to the active plan")
                text_field(event, "change_reason")
            elif event.get("supersedes"):
                raise ValueError("cannot supersede an unknown plan")
            state = {"plan": event, "due": due, "trigger": None,
                     "observed": None, "last_review": None,
                     "recommendation": event["recommendation"]}
            active[symbol] = state
        elif kind in {"OBSERVATION", "REVIEW"}:
            if not state or event.get("plan_id") != state["plan"]["id"]:
                raise ValueError("event must reference the active plan")
            plan = state["plan"]
            if kind == "REVIEW":
                if any(key in event for key in ("threshold", "basis", "comparator", "falsifier")):
                    raise ValueError("condition changes require a new PLAN revision")
                for field in ("reason", "evidence"):
                    text_field(event, field)
                recommendation = event.get("recommendation")
                if recommendation not in {"HOLD", "TRIM", "EXIT", "BUY", "WAIT"}:
                    raise ValueError("explicit review conclusion required")
                due = instant(text_field(event, "review_by"))
                if due <= recorded:
                    raise ValueError("review deadline must be in the future")
                if state["trigger"] and event.get("resolves") != state["trigger"]:
                    raise ValueError("review must reference the outstanding trigger")
                state.update(due=due, trigger=None, last_review=event_id,
                             recommendation=recommendation)
            else:
                text_field(event, "evidence")
                observed = instant(text_field(event, "observed_at"))
                if not instant(plan["recorded_at"]) <= observed <= recorded:
                    raise ValueError("observation outside the available information window")
                if state["observed"] and observed <= state["observed"]:
                    raise ValueError("observations must advance in time")
                if state.get("reviewed_at") and observed <= state["reviewed_at"]:
                    raise ValueError("observation predates the latest review")
                key = "close" if plan["basis"] == "CLOSE" else (
                    "low" if plan["comparator"] == "AT_OR_BELOW" else "high")
                price = positive(event.get(key))
                # Pass only the declared basis; intraday lows cannot trigger CLOSE rules.
                result = review_rule({"id": plan["id"], "symbol": symbol,
                    "action": "HOLD_REVIEW", "comparator": plan["comparator"],
                    "threshold": plan["threshold"], "created_date": observed.date().isoformat()},
                    {"date": observed.date().isoformat(), "close": price}, observed.date())
                if result["decision_required"] and not state["trigger"]:
                    state["trigger"] = event_id
                state["observed"] = observed
            if kind == "REVIEW":
                state["reviewed_at"] = recorded
        else:
            raise ValueError("unknown event type")
        if recorded <= as_of:
            visible[symbol] = dict(state)
    results = []
    for symbol, state in sorted(visible.items()):
        overdue = as_of >= state["due"]
        status = ("TRIGGERED_AWAITING_DECISION" if state["trigger"] else
                  "OVERDUE_REQUIRES_REVIEW" if overdue else
                  "ACTION_RECOMMENDED" if state["recommendation"] in {"TRIM", "EXIT", "BUY"} else
                  "WAITING_FOR_EVIDENCE" if state["recommendation"] == "WAIT" else
                  "NO_OBSERVATION" if state["observed"] is None else "WATCHING")
        results.append({"symbol": symbol, "plan_id": state["plan"]["id"],
                        "status": status, "overdue": overdue,
                        "decision_required": status != "WATCHING",
                        "trigger_id": state["trigger"], "last_review": state["last_review"],
                        "recommendation": state["recommendation"],
                        "basis": state["plan"]["basis"],
                        "threshold": state["plan"]["threshold"],
                        "falsifier": state["plan"]["falsifier"],
                        "review_by": state["due"].isoformat(),
                        "last_observed_at": state["observed"].isoformat() if state["observed"] else None})
    return results


def read_events(handle) -> list[dict]:
    return [json.loads(line) for line in handle if line.strip()]


def append_event(path: Path, event: dict) -> None:
    """Validate under an exclusive lock before appending; do not overwrite history."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        os.fchmod(handle.fileno(), 0o600)
        events = read_events(handle)
        replay(events + [event], instant(event["recorded_at"]))
        handle.seek(0, os.SEEK_END)
        if handle.tell():
            handle.seek(handle.tell() - 1)
            if handle.read() != "\n":
                raise ValueError("journal must end with a newline")
        handle.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("journal", type=Path, help="private JSONL path outside the repository")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("append")
    add.add_argument("event", type=Path)
    audit = sub.add_parser("audit")
    audit.add_argument("--as-of", required=True, help="timezone-aware ISO timestamp")
    args = parser.parse_args()
    if args.command == "append":
        append_event(args.journal, json.loads(args.event.read_text(encoding="utf-8")))
    else:
        with args.journal.open(encoding="utf-8") as handle:
            fcntl.flock(handle, fcntl.LOCK_SH)
            result = replay(read_events(handle), instant(args.as_of))
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
