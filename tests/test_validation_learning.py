from pathlib import Path

from validation.learning import build_learning_summary


def test_learning_empty(tmp_path: Path):
    s = build_learning_summary(tmp_path)
    assert s["rows"] == 0
    assert s["change_gate"]["eligible_for_model_change_review"] is False
    assert s["change_gate"]["benchmark_relative_observations"] == 0
    assert s["findings"] == []


def test_learning_segments_and_benchmark_gate(tmp_path: Path):
    d = tmp_path / "data/validation"
    d.mkdir(parents=True)
    p = d / "outcomes.csv"
    p.write_text(
        "decision_id,captured_at,market_regime,recommended_action,horizon,symbol,rank,return,benchmark_symbol,benchmark_return,excess_return,max_up,max_down,evaluated_price_date,model_version\n"
        + "\n".join(
            f"d{i},2026-01-01T00:00:00+00:00,RISK-ON,SELECTIVE_BUY,1w,T{i},1,0.02,1306.T,0.005,0.015,0.03,-0.01,2026-01-08,2.1.0"
            for i in range(60)
        )
        + "\n",
        encoding="utf-8",
    )
    s = build_learning_summary(tmp_path)
    h = s["segments"]["horizon"]["1w"]
    assert h["n"] == 60
    assert h["benchmark_n"] == 60
    assert h["outperform_rate"] == 1.0
    assert s["segments"]["rank_bucket"]["top1|1w"]["mean_excess_return"] == 0.015
    assert s["change_gate"]["eligible_for_model_change_review"] is True
    assert s["change_gate"]["basis"] == "benchmark_relative_observations"
    assert any(x["dimension"] == "action" and x["metric"] == "excess_return" for x in s["findings"])


def test_absolute_only_history_does_not_open_model_change_gate(tmp_path: Path):
    d = tmp_path / "data/validation"
    d.mkdir(parents=True)
    p = d / "outcomes.csv"
    p.write_text(
        "decision_id,captured_at,market_regime,recommended_action,horizon,symbol,rank,return,max_up,max_down,evaluated_price_date,model_version\n"
        + "\n".join(
            f"old{i},2026-01-01T00:00:00+00:00,NEUTRAL,REVIEW,1w,T{i},1,0.03,0.04,-0.01,2026-01-08,1.7.0"
            for i in range(100)
        )
        + "\n",
        encoding="utf-8",
    )
    s = build_learning_summary(tmp_path)
    assert s["change_gate"]["matured_observations"] == 100
    assert s["change_gate"]["benchmark_relative_observations"] == 0
    assert s["change_gate"]["eligible_for_model_change_review"] is False
    assert s["findings"] == []
