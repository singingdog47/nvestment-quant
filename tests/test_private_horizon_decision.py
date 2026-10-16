from datetime import datetime, timezone
import pandas as pd
from private_horizon_decision import build_private_matrix

NOW = datetime(2026, 10, 16, 13, 30, tzinfo=timezone.utc)

def make_args():
    holdings = pd.DataFrame([
        {"asset_type":"国内株式","code":"6701","ticker":"6701.T","name":"NEC","account":"特定","market_value":500000},
        {"asset_type":"国内株式","code":"5803","ticker":"5803.T","name":"フジクラ","account":"特定","market_value":500000},
        {"asset_type":"投資信託","code":"","ticker":"","name":"VTI","account":"旧NISA","market_value":12000000},
    ])
    return holdings, dict(
        outlook={"as_of_jst":"2026-10-16","prospective_hypotheses":[{"symbol":"6701.T","as_of_jst":"2026-10-16","expected_sign":"positive","id":"a1"}]},
        supply_rows=[{"ticker":"5803.T","observed_date":"2026-10-16","data_status":"ok","confidence":"0.8","price_as_of":"2026-10-16T06:30:00+00:00","context_flags":"VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION"}],
        screening_rows=[{"ticker":"6701.T","return_3m":"15","data_retrieved_at_utc":NOW.isoformat()}],
        policy={"policy":{"actionable":True,"blocks":[]}},
        investment_state={"policy":{"decision_gate":"OPEN"},"open_orders":{"count":0}},
        source_as_of="2026-10-16T17:19:00+09:00")

def test_matrix_is_research_only():
    holdings, params = make_args()
    result = build_private_matrix(holdings, **params, now=NOW)
    rows = {item["symbol"]:item for item in result["holdings"] if item["symbol"]}
    assert rows["6701.T"]["research_action"] == "WATCH_ADDITION_ONLY"
    assert rows["5803.T"]["research_action"] == "HOLD_REVIEW_DOWNSIDE"
    assert result["execution"]["authorized"] is False
    assert result["execution"]["orders_created"] == 0
    assert all(x["horizons"]["long_1_3y"]["signal"]=="UNASSESSED_FUNDAMENTALS" for x in result["holdings"])

def test_staleness_and_policy_blockers():
    holdings, params = make_args()
    params["source_as_of"]="2026-10-15T17:19:00+09:00"
    params["investment_state"]["open_orders"]["count"]=2
    params["investment_state"]["policy"]["decision_gate"]="BLOCK"
    result=build_private_matrix(holdings, **params, now=NOW)
    assert result["status"] == "partial_data"
    assert "STALE_PRIVATE_PORTFOLIO" in result["execution"]["blocking_conditions"]
    assert "OPEN_ORDERS_NEED_RECONCILIATION" in result["execution"]["blocking_conditions"]
    assert "EXISTING_DECISION_GATE_BLOCK" in result["execution"]["blocking_conditions"]
    assert result["execution"]["authorized"] is False
