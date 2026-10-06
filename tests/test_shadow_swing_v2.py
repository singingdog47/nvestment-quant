from datetime import date
import pandas as pd
from shadow_swing_v2 import generate_signals, score_row
CFG={"research":{"signals_per_day":10,"min_liquidity_score":40,"min_avg_turnover_jpy":50000000,"horizons_sessions":[1,3,5,10,20]}}
def row(**kw):
 b={"ticker":"1234.T","code":"1234","name":"Test","market":"JP","eligible":True,"price":1000,"liquidity_score":80,"avg_turnover_30d":100000000,"value_score":70,"quality_score":80,"growth_score":85,"momentum_score":75,"risk_score":70,"return_1m":2,"return_3m":10,"theme":"Other","total_score":77};b.update(kw);return b
def test_missing_optional_models_not_fabricated():
 m={x["model"] for x in score_row(pd.Series(row()))};assert "expectation_gap" in m and "earnings_revision" not in m and "event_rerating" not in m
def test_chasing_penalized():
 a=next(x["score"] for x in score_row(pd.Series(row(return_1m=5))) if x["model"]=="expectation_gap");b=next(x["score"] for x in score_row(pd.Series(row(return_1m=45))) if x["model"]=="expectation_gap");assert a>b
def test_revision_activates_with_data():
 assert any(x["model"]=="earnings_revision" for x in score_row(pd.Series(row(earnings_revision_score=.9))))
def test_japan_only_and_diverse():
 d=pd.DataFrame([row(),row(ticker="5678.T",code="5678",return_1m=-8),row(ticker="USX",code="USX",market="US")]);o=generate_signals(d,CFG,date(2026,10,7));assert set(o.symbol)<= {"1234.T","5678.T"} and o.model.nunique()>=2
