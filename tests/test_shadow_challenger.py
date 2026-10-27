import csv
import json
from datetime import date, datetime
from zoneinfo import ZoneInfo

import shadow_challenger as c


def setup_case(tmp_path, monkeypatch):
    cfg = json.loads(__import__("pathlib").Path("config/shadow_challenger_v1.json").read_text())
    cfg["cohort"] = "test-cohort"
    data = tmp_path / "data"
    data.mkdir()
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(cfg))
    monkeypatch.setattr(c, "DATA", data)
    monkeypatch.setattr(c, "OUT", data / "shadow_challenger")
    monkeypatch.setattr(c, "CONFIG", cfg_path)
    with (data / "screening_latest.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "market", "ticker", "eligible", "total_score", "momentum_score",
            "liquidity_score", "avg_turnover_30d", "price", "theme", "flags",
            "data_retrieved_at_utc"
        ])
        w.writeheader()
        w.writerow({"market": "JP", "ticker": "1234.T", "eligible": "True",
                    "total_score": 79, "momentum_score": 71, "liquidity_score": 80,
                    "avg_turnover_30d": 200000000, "price": 1000, "theme": "Industrials",
                    "flags": "ok", "data_retrieved_at_utc": "2026-10-22T07:45:00Z"})
    return cfg, data


def test_signal_created_without_optional_regime_and_without_real_fill(tmp_path, monkeypatch):
    _, _ = setup_case(tmp_path, monkeypatch)
    r = c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    assert r["screen_fresh"] and r["positions"] == 0
    assert r["pending_buys"] == 1 and r["sizing_multiplier"] == 0.5
    assert any(x["event"] == "BUY_SIGNAL" for x in r["events"])


def test_next_session_verified_open_and_position_limit(tmp_path, monkeypatch):
    _, _ = setup_case(tmp_path, monkeypatch)
    c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    b = {"open": 1010, "high": 1020, "low": 1005, "close": 1015}
    r = c.run(date(2026, 10, 23), bar_source=lambda s, d: b if s == "1234.T" else None)
    state = c.load_json(c.OUT / "state.json")
    assert r["positions"] == 1 and r["pending_buys"] == 0
    pos = state["positions"]["1234.T"]
    assert pos["entry_price"] > 1010
    assert pos["qty"] * pos["entry_price"] <= 103000  # 10% target + bounded 3% open-gap tolerance
    assert pos["qty"] * pos["entry_price"] <= 200000  # hard per-name cap remains absolute
    assert r["cash_jpy"] == round(1000000 - pos["qty"] * pos["entry_price"], 2)
    assert c.run(date(2026, 10, 23), bar_source=lambda s, d: None)["status"] == "ALREADY_PROCESSED"


def test_missing_ohlc_never_creates_fill(tmp_path, monkeypatch):
    _, _ = setup_case(tmp_path, monkeypatch)
    c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    r = c.run(date(2026, 10, 23), bar_source=lambda s, d: None)
    assert r["positions"] == 0 and r["pending_buys"] == 1
    assert any(x["event"] == "ENTRY_BAR_MISSING" for x in r["events"])


def test_stop_first_if_both_stop_and_profit_hit(tmp_path, monkeypatch):
    _, _ = setup_case(tmp_path, monkeypatch)
    c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    c.run(date(2026, 10, 23), bar_source=lambda s, d: {
        "open": 1000, "high": 1010, "low": 990, "close": 1000} if s == "1234.T" else None)
    r = c.run(date(2026, 10, 26), bar_source=lambda s, d: {
        "open": 1000, "high": 1200, "low": 900, "close": 1050} if s == "1234.T" else None)
    assert r["positions"] == 0 and r["trades"] == 1
    assert [x["reason"] for x in r["events"] if x["event"] == "SELL"] == ["STOP"]


def test_screen_not_postclose_does_not_generate_signals(tmp_path, monkeypatch):
    _, data = setup_case(tmp_path, monkeypatch)
    p = data / "screening_latest.csv"
    p.write_text(p.read_text().replace("2026-10-22T07:45:00Z", "2026-10-22T05:20:00Z"))
    r = c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    assert r["status"] == "NO_NEW_SIGNALS" and r["pending_buys"] == 0


def test_midnight_delayed_workflow_uses_prior_postclose_session():
    now = datetime(2026, 10, 23, 2, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    screen = [{"data_retrieved_at_utc": "2026-10-22T12:57:00Z"}]
    assert c.resolve_market_session(now, screen) == date(2026, 10, 22)
    assert c.resolve_market_session(datetime(2026, 10, 23, 9, 1, tzinfo=ZoneInfo("Asia/Tokyo")), screen) == date(2026, 10, 23)
    assert c.resolve_market_session(now, [{"data_retrieved_at_utc": "2026-10-21T12:57:00Z"}]) == date(2026, 10, 23)


def test_activity_and_november_target_audit_without_fake_trades(tmp_path, monkeypatch):
    cfg, data = setup_case(tmp_path, monkeypatch)
    # Recreate historical cohort close to the user's challenge.
    state = c.new_state(cfg)
    state["last_run_date"] = "2026-10-30"
    state["nav_jpy"] = 980000
    state["cash_jpy"] = 980000
    c.write_json(c.OUT / "state.json", state)
    nov_bar = {"open": 1000, "high": 1010, "low": 990, "close": 1000}
    first = c.run(date(2026, 11, 2), bar_source=lambda s, d: nov_bar if s == "1306.T" else None)
    assert first["activity_goal"]["status"] == "DEADLINE_MISSED"
    assert first["activity_goal"]["verified_fills_since_start"] == 0
    assert first["monthly_goal"]["baseline_nav_jpy"] == 980000
    assert first["monthly_goal"]["return_pct"] == 0
    assert first["monthly_goal"]["status"] == "BELOW_TARGET_SO_FAR"


def test_verified_buy_logged_once_and_counts_for_activity(tmp_path, monkeypatch):
    setup_case(tmp_path, monkeypatch)
    c.run(date(2026, 10, 22), bar_source=lambda s, d: None)
    b = {"open": 1010, "high": 1020, "low": 1005, "close": 1015}
    r = c.run(date(2026, 10, 26), bar_source=lambda s, d: b if s == "1234.T" else None)
    # Existing order expiry is four calendar days; 22 -> 26 is still permitted.
    assert r["activity_goal"]["status"] == "PASSED"
    assert r["activity_goal"]["verified_fills_since_start"] == 1
    assert r["activity_goal"]["fills"][0]["side"] == "BUY"
    assert r["activity_goal"]["fills"][0]["source"] == "verified_session_open"
    again = c.run(date(2026, 10, 26), bar_source=lambda s, d: b)
    assert again["status"] == "ALREADY_PROCESSED"
    assert len(c.load_json(c.OUT / "state.json")["execution_log"]) == 1


def test_next_day_0104_jst_screen_is_prior_market_session():
    ts = "2026-10-26T16:04:39+00:00"  # 2026-10-27 01:04 JST
    screen = [{"data_retrieved_at_utc": ts}]
    now = datetime(2026, 10, 27, 4, 53, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert c.resolve_market_session(now, screen) == date(2026, 10, 26)
    assert c._postclose_source_for_session(ts, date(2026, 10, 26))
    assert not c._postclose_source_for_session(ts, date(2026, 10, 27))
    assert c.resolve_market_session(datetime(2026, 10, 27, 9, 1, tzinfo=ZoneInfo("Asia/Tokyo")), screen) == date(2026, 10, 27)


def test_after_midnight_screen_can_signal_yesterday_without_fake_fill(tmp_path, monkeypatch):
    _, data = setup_case(tmp_path, monkeypatch)
    import csv
    path = data / "screening_latest.csv"
    path.write_text(path.read_text().replace("2026-10-22T07:45:00Z", "2026-10-23T01:02:00Z"))
    observed = c.run(date(2026, 10, 22), bar_source=lambda symbol, day: None)
    assert observed["screen_fresh"] is True
    assert observed["pending_buys"] == 1
    assert observed["positions"] == 0
    assert observed["events"][0]["event"] == "BUY_SIGNAL"


def test_overnight_screen_rejects_wrong_day(tmp_path, monkeypatch):
    _, data = setup_case(tmp_path, monkeypatch)
    path = data / "screening_latest.csv"
    path.write_text(path.read_text().replace("2026-10-22T07:45:00Z", "2026-10-22T01:04:00Z"))
    r = c.run(date(2026, 10, 22), bar_source=lambda symbol, day: None)
    assert r["screen_fresh"] is False
    assert r["pending_buys"] == 0
