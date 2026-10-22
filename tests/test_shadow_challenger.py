import csv
import json
from datetime import date

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
