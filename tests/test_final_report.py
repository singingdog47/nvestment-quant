import json
from pathlib import Path

from final_report import build_final_report


def test_final_report_blocks_when_quality_not_actionable(tmp_path: Path):
    (tmp_path / 'data/regime').mkdir(parents=True)
    (tmp_path / 'data/alerts').mkdir(parents=True)
    (tmp_path / 'data/validation').mkdir(parents=True)
    (tmp_path / 'data/decision_context_latest.json').write_text(json.dumps({
        'quality': {'actionable': False, 'quality_score': 0.3},
        'policy_guardrails': {'decision_gate': 'BLOCK_DATA_QUALITY'}
    }), encoding='utf-8')
    (tmp_path / 'data/regime/market_regime_latest.json').write_text(json.dumps({'regime_label':'CONSTRUCTIVE'}), encoding='utf-8')
    (tmp_path / 'data/alerts/alerts_latest.json').write_text(json.dumps({'highest_severity':'INFO','alerts':[]}), encoding='utf-8')
    (tmp_path / 'data/validation/learning_latest.json').write_text(json.dumps({'change_gate':{}}), encoding='utf-8')
    (tmp_path / 'data/screening_latest.csv').write_text('rank,name,ticker,total_score\n1,Example,1111.T,80\n', encoding='utf-8')
    public_path, private_path = build_final_report(tmp_path)
    text = public_path.read_text(encoding='utf-8')
    assert 'WAIT / DATA QUALITY REVIEW' in text
    assert 'Example' in text
    assert private_path is None


def test_final_report_separates_quality_and_regime_actionability(tmp_path: Path):
    (tmp_path / 'data/regime').mkdir(parents=True)
    (tmp_path / 'data/alerts').mkdir(parents=True)
    (tmp_path / 'data/validation').mkdir(parents=True)
    (tmp_path / 'data/decision_context_latest.json').write_text(json.dumps({
        'quality': {'actionable': True, 'quality_score': 0.8},
        'policy_guardrails': {'decision_gate': 'OPEN_FOR_ANALYSIS'}
    }), encoding='utf-8')
    (tmp_path / 'data/regime/market_regime_latest.json').write_text(json.dumps({
        'regime_label': 'CONSTRUCTIVE', 'actionable': False, 'data_status': 'partial',
        'actionability': {'reasons': ['core_credit_or_financial_conditions_missing']},
    }), encoding='utf-8')
    (tmp_path / 'data/alerts/alerts_latest.json').write_text(json.dumps({'highest_severity':'INFO','alerts':[]}), encoding='utf-8')
    (tmp_path / 'data/validation/learning_latest.json').write_text(json.dumps({'change_gate':{}}), encoding='utf-8')
    (tmp_path / 'data/screening_latest.csv').write_text('market,market_rank,name,ticker,total_score\nJP,1,Example,1111.T,80\n', encoding='utf-8')
    public_path, _ = build_final_report(tmp_path)
    text = public_path.read_text(encoding='utf-8')
    assert 'Screening / intelligence data actionable: `True`' in text
    assert 'Regime context actionable: `False`' in text
    assert 'Overall analysis mode: `REVIEW_ONLY_PARTIAL_REGIME`' in text
    assert 'Data actionable: `True`' not in text


def test_private_appendix_is_not_public(tmp_path: Path):
    (tmp_path / 'data/regime').mkdir(parents=True)
    (tmp_path / 'data/alerts').mkdir(parents=True)
    (tmp_path / 'data/validation').mkdir(parents=True)
    (tmp_path / '.private/portfolio_risk').mkdir(parents=True)
    (tmp_path / '.private/portfolio_risk/portfolio_risk_latest.md').write_text('SECRET_RISK_VALUE', encoding='utf-8')
    public_path, private_path = build_final_report(tmp_path)
    assert 'SECRET_RISK_VALUE' not in public_path.read_text(encoding='utf-8')
    assert private_path is not None
    assert 'SECRET_RISK_VALUE' in private_path.read_text(encoding='utf-8')
