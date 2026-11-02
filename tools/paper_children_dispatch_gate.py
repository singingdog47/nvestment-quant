"""Evidence-gated recovery dispatch for post-close paper-only child workflows."""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from tools.post_close_watchdog_gate import report_is_fresh, target_session

JST = ZoneInfo("Asia/Tokyo")


def should_dispatch(report: str, now: datetime) -> bool:
    """Never dispatch paper children for pre-close or holiday-only snapshots."""
    return target_session(now) is not None and report_is_fresh(report, now)[0]


def main() -> None:
    now = datetime.now(JST)
    path = Path("data/integrated_report_latest.md")
    report = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    dispatch = should_dispatch(report, now)
    session = target_session(now)
    print(f"paper-child recovery dispatch={dispatch} target_session={session}")
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as stream:
            stream.write(f"dispatch={str(dispatch).lower()}\n")


if __name__ == "__main__":
    main()
