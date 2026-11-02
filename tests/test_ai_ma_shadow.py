from datetime import date, datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import csv
import json

from ai_ma_shadow import screen_candidates, run, infer_run_session, is_postclose_jst_date


def sample(day):
    return {
        "market":"JP","ticker":"1000.T","name":"Candidate A","eligible":"True",
        "data_retrieved_at_utc":f"{day}T07:30:00+00:00",
        "market_cap":"30000000000","pe":"10","pb":"0.7","roe":"9",
        "operating_margin":"7","avg_turnover_30d":"500000000",
    }


def config(tmp_path, date_start="2026-10-19"):
    config={
        "cohort":"test-ai-ma-5m","mode":"SHADOW_ONLY","start_date":date_start,
        "end_date":"2027-10-19","virtual_initial_cash_jpy":5000000,
        "benchmark_symbol":"1306.T",
        "gate":{"market_cap_min":4000000000,"market_cap_max":150000000000,
                "pe_max":17,"pb_max":1.5,"roe_min":4,
                "operating_margin_min":2,"turnover_min":150000000},
        "risk":{"max_positions":8,"max_position_weight":0.1,
                "max_new_entries_per_day":2,"max_holding_calendar_days":90,
                "max_avg_turnover_participation":0.02},
        "execution":{"slippage_bps":15,"max_open_gap_pct":5,"lot":100},
        "audit":{"max_candidates":5},
        "governance":{"real_orders_forbidden":True}
    }
    p=tmp_path/"config.json"
    p.write_text(json.dumps(config),encoding="utf-8")
    return p


def feed(tmp_path, rows):
    p=tmp_path/"screening_latest.csv"
    p.parent.mkdir(exist_ok=True)
    with p.open("w",encoding="utf-8",newline="") as s:
        w=csv.DictWriter(s,fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def prices(symbol, day):
    close=1000 if symbol=="1306.T" else 500
    return {"open":close,"high":close*1.01,"low":close*.99,"close":close}


def test_screen_is_not_takeover_prediction(tmp_path):
    cfg=json.loads(config(tmp_path).read_text())
    good,bad=screen_candidates([sample("2026-10-19")],cfg,date(2026,10,19))
    assert len(good)==1 and len(bad)==0
    assert good[0]["target_event_probability"] is None
    assert good[0]["ai_restructuring_evidence"]=="UNVERIFIED"
    assert good[0]["ownership_takeover_evidence"]=="UNVERIFIED"
    old=sample("2026-10-16")
    good,bad=screen_candidates([old],cfg,date(2026,10,19))
    assert good==[] and bad[0]["vetoes"]==["stale_or_undated_screen"]


def test_stale_data_never_generates_orders(tmp_path):
    cp=config(tmp_path)
    feed(tmp_path,[sample("2026-10-16")])
    out=run(date(2026,10,19),root=tmp_path,cfg_path=cp,price_loader=prices)
    assert out["pending_buys"]==0
    assert out["nav_jpy"]==5000000
    assert "fresh_jp_screen_unavailable" in out["data_blockers"]


def test_virtual_order_is_only_filled_next_session(tmp_path):
    cp=config(tmp_path)
    feed(tmp_path,[sample("2026-10-19")])
    first=run(date(2026,10,19),root=tmp_path,cfg_path=cp,price_loader=prices)
    assert first["pending_buys"]==1
    assert first["positions_count"]==0
    feed(tmp_path,[sample("2026-10-20")])
    second=run(date(2026,10,20),root=tmp_path,cfg_path=cp,price_loader=prices)
    assert second["positions_count"]==1
    assert second["pending_buys"]==0
    assert second["completed_trades"]==0
    assert second["nav_jpy"]<5000000
    third=run(date(2026,10,20),root=tmp_path,cfg_path=cp,price_loader=prices)
    assert third==second


def test_virtual_money_is_immutable_and_real_money_disabled(tmp_path):
    cp=config(tmp_path)
    feed(tmp_path,[sample("2026-10-19")])
    out=run(date(2026,10,19),root=tmp_path,cfg_path=cp,price_loader=prices)
    assert out["paper_only"] is True
    c=json.loads(cp.read_text())
    c["virtual_initial_cash_jpy"]=8000000
    cp.write_text(json.dumps(c))
    try:
        run(date(2026,10,20),root=tmp_path,cfg_path=cp,price_loader=prices)
    except RuntimeError as e:
        assert "cohort mismatch" in str(e)
    else:
        assert False, "capital increase must create a new cohort"

def test_holiday_does_not_write_fake_session_or_orders(tmp_path):
    cp = config(tmp_path)
    feed(tmp_path, [sample("2026-11-03")])
    out = run(date(2026, 11, 3), root=tmp_path, cfg_path=cp, price_loader=prices)
    assert out["status"] == "OUTSIDE_SESSION"
    assert not (tmp_path / "ai_ma_shadow" / "state.json").exists()


def test_preclose_screen_cannot_queue_paper_buys(tmp_path):
    cp = config(tmp_path)
    row = sample("2026-10-19")
    row["data_retrieved_at_utc"] = "2026-10-19T00:30:00+00:00"
    feed(tmp_path, [row])
    out = run(date(2026, 10, 19), root=tmp_path, cfg_path=cp, price_loader=prices)
    assert out["pending_buys"] == 0
    assert "fresh_jp_screen_unavailable" in out["data_blockers"]


def test_expired_pending_buy_never_fills_after_data_outage(tmp_path):
    cp = config(tmp_path)
    feed(tmp_path, [sample("2026-10-19")])
    first = run(date(2026, 10, 19), root=tmp_path, cfg_path=cp, price_loader=prices)
    assert first["pending_buys"] == 1
    # Simulate an outage: the last screen is still from the signal day.
    # A fresh screen could legitimately queue a *new* independent order.
    feed(tmp_path, [sample("2026-10-19")])
    later = run(date(2026, 10, 26), root=tmp_path, cfg_path=cp, price_loader=prices)
    assert later["pending_buys"] == 0
    assert later["positions_count"] == 0
    assert {"event": "ENTRY_EXPIRED", "symbol": "1000.T"} in later["events"]


def test_delayed_postclose_snapshot_is_attributed_to_prior_jpx_session(tmp_path):
    cp = config(tmp_path)
    row = sample("2026-11-02")
    # Pipeline scheduled for Nov 2 but actually executed at Nov 3 02:06 JST.
    row["data_retrieved_at_utc"] = "2026-11-02T17:06:38+00:00"
    feed(tmp_path, [row])
    now = datetime(2026, 11, 3, 2, 20, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(now, [row]) == date(2026, 11, 2)
    assert is_postclose_jst_date(row["data_retrieved_at_utc"], date(2026, 11, 2))
    result = run(date(2026, 11, 2), root=tmp_path, cfg_path=cp, price_loader=prices)
    assert result["as_of_date"] == "2026-11-02"
    assert "fresh_jp_screen_unavailable" not in result["data_blockers"]


def test_overnight_inference_rejects_preclose_and_market_open(tmp_path):
    row = sample("2026-11-02")
    row["data_retrieved_at_utc"] = "2026-11-02T05:00:00+00:00"  # 14:00 JST
    overnight = datetime(2026, 11, 3, 2, 20, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(overnight, [row]) == date(2026, 11, 3)
    assert not is_postclose_jst_date(row["data_retrieved_at_utc"], date(2026, 11, 2))
    row["data_retrieved_at_utc"] = "2026-11-02T17:06:38+00:00"
    market_open = datetime(2026, 11, 3, 9, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(market_open, [row]) == date(2026, 11, 3)
    holiday_previous = datetime(2026, 11, 4, 2, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    # Nov 3 is a JPX holiday: Nov 2 remains the latest completed session.
    assert infer_run_session(holiday_previous, [row]) == date(2026, 11, 2)


def test_holiday_evening_can_catch_up_previous_completed_session():
    # A Nov 2 screen retrieved after midnight Nov 3 is still Nov 2 evidence.
    row = sample("2026-11-02")
    row["data_retrieved_at_utc"] = "2026-11-02T18:14:32+00:00"
    holiday_evening = datetime(2026, 11, 3, 21, 55, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(holiday_evening, [row]) == date(2026, 11, 2)
    # Do not infer a holiday session or create new holiday fills.
    assert is_postclose_jst_date(row["data_retrieved_at_utc"], date(2026, 11, 2))


def test_holiday_catchup_does_not_skip_newer_cash_session():
    row = sample("2026-11-02")
    row["data_retrieved_at_utc"] = "2026-11-02T18:14:32+00:00"
    # On Nov 5 (after Nov 4 has completed), Nov 2 is too old to backfill
    # merely from an old screen.
    later_holiday_window = datetime(2026, 11, 5, 7, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(later_holiday_window, [row]) == date(2026, 11, 5)


def test_weekend_recovery_uses_last_trading_day_only_with_fresh_evidence():
    row = sample("2026-11-06")
    row["data_retrieved_at_utc"] = "2026-11-07T00:10:00+00:00"  # Sat 09:10 JST: too late
    weekend = datetime(2026, 11, 8, 12, 0, tzinfo=ZoneInfo("Asia/Tokyo"))
    assert infer_run_session(weekend, [row]) == date(2026, 11, 8)
    row["data_retrieved_at_utc"] = "2026-11-06T18:10:00+00:00"  # Sat 03:10 JST
    assert infer_run_session(weekend, [row]) == date(2026, 11, 6)
