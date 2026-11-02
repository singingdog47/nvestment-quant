"""Guard against redundant post-close pipeline dispatch on JPX holidays."""
from datetime import datetime
from zoneinfo import ZoneInfo

from tools.post_close_watchdog_gate import report_is_fresh, target_session

JST = ZoneInfo("Asia/Tokyo")
UTC = ZoneInfo("UTC")


def clock(day, hour, minute=0):
    return datetime.fromisoformat(day).replace(hour=hour, minute=minute, tzinfo=JST)


def report(utc_timestamp):
    return "# Daily report\nGenerated (UTC): " + utc_timestamp + "\n"


def test_november_3_holiday_overnight_recovery_targets_november_2():
    now = clock("2026-11-03", 3, 18)
    assert target_session(now).isoformat() == "2026-11-02"
    fresh, reason = report_is_fresh(report("2026-11-02T17:11:00+00:00"), now)
    assert fresh and reason == "fresh_for_2026-11-02"


def test_november_3_holiday_daytime_never_dispatches():
    for hour in (9, 12, 16, 23):
        now = clock("2026-11-03", hour)
        assert target_session(now) is None
        assert report_is_fresh("", now)[0] is True


def test_before_market_close_never_dispatches():
    for hour in (9, 14, 15):
        now = clock("2026-11-02", hour, 0)
        assert target_session(now) is None
        assert report_is_fresh("", now)[0] is True


def test_trading_day_post_close_requires_current_session_report():
    now = clock("2026-11-02", 17, 30)
    assert target_session(now).isoformat() == "2026-11-02"
    assert not report_is_fresh(report("2026-10-30T08:00:00+00:00"), now)[0]
    assert report_is_fresh(report("2026-11-02T07:31:00+00:00"), now)[0]


def test_missing_or_future_timestamp_is_not_fresh_in_recovery_window():
    now = clock("2026-11-03", 3, 18)
    assert not report_is_fresh("", now)[0]
    assert not report_is_fresh(report("2026-11-02T19:00:00+00:00"), now)[0]


def test_no_replay_after_overnight_window():
    now = clock("2026-11-04", 10)
    assert target_session(now) is None
    assert report_is_fresh("", now)[0]


def test_weekend_and_holiday_do_not_create_new_session():
    assert target_session(clock("2026-11-01", 17)) is None
    assert target_session(clock("2026-11-03", 17)) is None
