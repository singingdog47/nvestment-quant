import csv
import json
from pathlib import Path
from ai_ma_historical import assess, run

def test_missing_data_does_not_create_fake_backtest(tmp_path):
    result=assess(tmp_path)
    assert result["trial_result"]=="NO_STATISTICAL_CONCLUSION"
    assert result["alpha_estimate"] is None
    assert result["takeover_probability_estimate"] is None
    assert result["historical_public_validation"]["usable_outcomes_1w"]==0
    assert result["matched_value_only_control"]["status"]=="NOT_ESTIMABLE"
    published=run(tmp_path,tmp_path/"out")
    assert (tmp_path/"out/historical_audit_latest.md").exists()
    assert published["status"].startswith("INSUFFICIENT")

def test_existing_generic_outcomes_remain_baseline_only(tmp_path):
    d=tmp_path/"validation"
    d.mkdir()
    with (d/"outcomes.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["captured_at","horizon","excess_return"])
        w.writeheader()
        w.writerow({"captured_at":"2026-09-01T07:00:00+00:00","horizon":"1w","excess_return":"0.04"})
    doc=assess(tmp_path)
    assert doc["historical_public_validation"]["usable_outcomes_1w"]==1
    assert doc["historical_public_validation"]["is_AI_MA_target_labeled"] is False
    assert doc["alpha_estimate"] is None

def test_invalid_event_provenance_rejected(tmp_path):
    p=tmp_path/"ai_ma_shadow/reference"
    p.mkdir(parents=True)
    with (p/"verified_corporate_events.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["symbol","announcement_date","event_type","source_url","source_published_at"])
        w.writeheader()
        w.writerow({"symbol":"9999.T","announcement_date":"2026-09-01","event_type":"tob",
                    "source_url":"https://example.org","source_published_at":"2026-08-31T12:00:00+09:00"})
    doc=assess(tmp_path)
    assert doc["corporate_event_evidence"]["verified_events"]==0
    assert doc["corporate_event_evidence"]["unverified_or_invalid_events"]==1
