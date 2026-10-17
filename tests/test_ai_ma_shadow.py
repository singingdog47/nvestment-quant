from datetime import date
from pathlib import Path
import csv
import json

from ai_ma_shadow import screen_candidates, run


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
