"""JPX-session-aware, idempotent gate for the post-close recovery watchdog.

A scheduled GitHub Actions job may arrive after midnight JST. In that case,
a report generated overnight belongs to the previous completed JPX session.
Never dispatch a post-close recovery on a holiday or before the cash close.
"""
from __future__ import annotations

import os
import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from jpx_market_calendar import is_jpx_session

JST = ZoneInfo("Asia/Tokyo")
CLOSE = time(15, 30)
OVERNIGHT_CUTOFF = time(9, 0)


def target_session(now: datetime) -> date | None:
    """Return a completed JPX session eligible for a watchdog recovery."""
    if now.tzinfo is None:
        raise ValueError("watchdog clock must be timezone-aware")
    local = now.astimezone(JST)
    today = local.date()
    if is_jpx_session(today) and local.time() >= CLOSE:
        return today
    yesterday = today - timedelta(days=1)
    if local.time() < OVERNIGHT_CUTOFF and is_jpx_session(yesterday):
        return yesterday
    return None


def report_is_fresh(report: str, now: datetime) -> tuple[bool, str]:
    """Require a report timestamp after the eligible session's market close."""
    session = target_session(now)
    if session is None:
        return True, "no_completed_jpx_session_in_recovery_window"
    match = re.search(r"Generated \(UTC\):\s*([^\n]+)", report)
    if not match:
        return False, "report_timestamp_missing"
    try:
        generated = datetime.fromisoformat(match.group(1).strip().replace("Z", "+00:00"))
        if generated.tzinfo is None:
            return False, "report_timestamp_naive"
        if generated > now:
            return False, "report_timestamp_in_future"
        local = generated.astimezone(JST)
    except (ValueError, TypeError):
        return False, "report_timestamp_invalid"
    same_day = local.date() == session and local.time() >= CLOSE
    overnight = (local.date() == session + timedelta(days=1)
                 and local.time() < OVERNIGHT_CUTOFF)
    return (True, "fresh_for_" + session.isoformat()) if (same_day or overnight) else (
        False, "stale_for_" + session.isoformat())


def main() -> None:
    now = datetime.now(JST)
    path = Path("data/integrated_report_latest.md")
    report = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    fresh, reason = report_is_fresh(report, now)
    session = target_session(now)
    print(f"watchdog target_session={session} fresh={fresh} reason={reason}")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"fresh={str(fresh).lower()}\n")
            stream.write(f"reason={reason}\n")
            stream.write(f"target_session={session.isoformat() if session else 'none'}\n")


if __name__ == "__main__":
    main()
