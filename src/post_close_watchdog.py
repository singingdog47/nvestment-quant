"""Freshness and dispatch-window checks for the JPX post-close watchdog.

A GitHub cron scheduled on a trading day may be delivered after midnight JST,
including on a following holiday. Such delivery must not launch another full
pipeline if the prior session's report was already generated overnight.
This module does not run trades or modify investment state.
"""
from __future__ import annotations

import os
import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from jpx_market_calendar import is_jpx_session

JST = ZoneInfo("Asia/Tokyo")
POST_CLOSE = time(15, 30)
# A late GitHub schedule should not relaunch a stale session days afterward.
MAX_RECOVERY_AGE = timedelta(hours=18)


def latest_completed_session(now: datetime) -> date:
    if now.tzinfo is None:
        raise ValueError("An aware timestamp is required")
    local = now.astimezone(JST)
    day = local.date()
    if not is_jpx_session(day) or local.time() < POST_CLOSE:
        day -= timedelta(days=1)
    while not is_jpx_session(day):
        day -= timedelta(days=1)
    return day


def parse_generated(report_text: str) -> datetime | None:
    match = re.search(r"Generated \(UTC\):\s*([^\n]+)", report_text)
    if not match:
        return None
    try:
        generated = datetime.fromisoformat(match.group(1).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return generated.astimezone(JST) if generated.tzinfo is not None else None


def assess_report(report_text: str, now: datetime) -> dict:
    if now.tzinfo is None:
        raise ValueError("An aware timestamp is required")
    local_now = now.astimezone(JST)
    session = latest_completed_session(local_now)
    close = datetime.combine(session, POST_CLOSE, tzinfo=JST)
    end = close + MAX_RECOVERY_AGE
    generated = parse_generated(report_text)
    fresh = generated is not None and close <= generated <= min(local_now, end)
    recovery_allowed = close <= local_now <= end
    return {
        "target_session": session.isoformat(),
        "generated": generated.isoformat() if generated else "unknown",
        "fresh": bool(fresh),
        "recovery_allowed": recovery_allowed,
    }


def main() -> None:
    now = datetime.now(JST)
    path = Path("data/integrated_report_latest.md")
    report = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    status = assess_report(report, now)
    print(f"post_close_watchdog={status}")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            for key in ("fresh", "recovery_allowed"):
                handle.write(f"{key}={str(status[key]).lower()}\n")
            handle.write(f"target_session={status['target_session']}\n")
            handle.write(f"generated={status['generated']}\n")


if __name__ == "__main__":
    main()
