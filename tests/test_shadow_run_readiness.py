from datetime import date, datetime
from pathlib import Path
import csv

from shadow_run_readiness import before_today_close, safe_flat_replay
from shadow_swing_v2 import append_csv


DAY = date(2026, 10, 23)


def test_premarket_run_defers_same_day_not_historical_replay():
    morning = datetime.fromisoformat("2026-10-23T09:30:00+09:00")
    evening = datetime.fromisoformat("2026-10-23T17:40:00+09:00")
    assert before_today_close(DAY, morning)
    assert not before_today_close(DAY, evening)
    assert not before_today_close(date(2026, 10, 22), morning)


def test_v1_flat_stale_replay_only_for_same_day_without_execution():
    state = {"positions": {}, "pending_orders": []}
    prior = {"as_of_date": DAY.isoformat(), "data_fresh": False,
             "positions": [], "pending_orders": [], "fills_today": [], "priced_symbols": []}
    assert safe_flat_replay(DAY, state, prior, "v1", today=DAY)
    assert not safe_flat_replay(DAY, state, prior, "v1", today=date(2026, 10, 24))
    assert not safe_flat_replay(DAY, {"positions": {"1234.T": {}}, "pending_orders": []},
                                prior, "v1", today=DAY)
    assert not safe_flat_replay(DAY, state, {**prior, "fills_today": [{"event": "SELL"}]},
                                "v1", today=DAY)


def test_v2_blocked_flat_snapshot_can_recover_but_not_after_fill():
    state = {"positions": {}, "pending_buys": []}
    prior = {"as_of_date": DAY.isoformat(), "market_data_blockers": [
        "screen_outdated_no_new_trades", "benchmark_bar_unavailable"],
        "events": [], "queued_buys": 0, "open_positions": 0}
    assert safe_flat_replay(DAY, state, prior, "v2", today=DAY)
    assert not safe_flat_replay(DAY, state, {**prior, "events": [{"event": "BUY_FILLED"}]},
                                "v2", today=DAY)
    assert not safe_flat_replay(DAY, state, {**prior, "market_data_blockers": [
        "benchmark_bar_unavailable"]}, "v2", today=DAY)


def test_same_day_equity_curve_is_upserted_not_duplicated(tmp_path):
    path = tmp_path / "equity_curve.csv"
    fields = ["date", "nav_jpy"]
    append_csv(path, {"date": DAY.isoformat(), "nav_jpy": 5000000}, fields)
    append_csv(path, {"date": DAY.isoformat(), "nav_jpy": 4999900}, fields)
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows == [{"date": DAY.isoformat(), "nav_jpy": "4999900"}]
