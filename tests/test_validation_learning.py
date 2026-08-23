from pathlib import Path

from validation.learning import build_learning_summary


def test_learning_empty(tmp_path: Path):
    s = build_learning_summary(tmp_path)
    assert s["rows"] == 0
    assert s["change_gate"]["eligible_for_model_change_review"] is False
    assert s["findings"] == []


def test_learning_segments_and_gate(tmp_path: Path):
    d = tmp_path / "data/validation"
    d.mkdir(parents=True)
    p = d / "outcomes.csv"
    p.write_text(
        "decision_id,captured_at,market_regime,recommended_action,horizon,symbol,rank,return,max_up,max_down,evaluated_price_date,model_version\n"
        + "\n".join(
            f"d{i},2026-01-01T00:00:00+00:00,RISK-ON,SELECTIVE_BUY,1w,T{i},1,0.02,0.03,-0.01,2026-01-08,1.7.0"
            for i in range(60)
        )
        + "\n",
        encoding="utf-8",
    )
    s = build_learning_summary(tmp_path)
    assert s["segments"]["horizon"]["1w"]["n"] == 60
    assert s["segments"]["rank_bucket"]["top1|1w"]["win_rate"] == 1.0
    assert s["change_gate"]["eligible_for_model_change_review"] is True
    assert any(x["dimension"] == "action" for x in s["findings"])
