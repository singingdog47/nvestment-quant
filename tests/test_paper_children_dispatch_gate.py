"""Recovery dispatch must be evidence-gated and never mutate paper state."""
from datetime import datetime
from zoneinfo import ZoneInfo

from tools.paper_children_dispatch_gate import should_dispatch

JST = ZoneInfo("Asia/Tokyo")


def when(day, hour, minute=0):
    return datetime.fromisoformat(day).replace(hour=hour, minute=minute, tzinfo=JST)


def report(utc):
    return f"Generated (UTC): {utc}\n"


def test_dispatch_after_trading_day_close():
    assert should_dispatch(report("2026-11-02T07:35:00+00:00"),
                           when("2026-11-02", 17))


def test_dispatch_overnight_for_previous_jpx_session():
    assert should_dispatch(report("2026-11-02T18:11:00+00:00"),
                           when("2026-11-03", 3, 15))


def test_no_dispatch_on_holiday_daytime_or_preclose():
    assert not should_dispatch(report("2026-11-02T18:11:00+00:00"),
                               when("2026-11-03", 11))
    assert not should_dispatch("", when("2026-11-02", 14))


def test_no_dispatch_on_stale_report_or_future_timestamp():
    assert not should_dispatch(report("2026-10-30T07:40:00+00:00"),
                               when("2026-11-02", 17))
    assert not should_dispatch(report("2026-11-02T19:00:00+00:00"),
                               when("2026-11-03", 3, 15))


def test_workflow_cli_invocation_import_path():
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(["src", "."])
    completed = subprocess.run(
        [sys.executable, "tools/paper_children_dispatch_gate.py"],
        cwd=Path.cwd(), env=env, capture_output=True, text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "paper-child recovery dispatch=" in completed.stdout
