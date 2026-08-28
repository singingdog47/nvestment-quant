from pathlib import Path


WORKFLOWS = Path('.github/workflows')


def _text(name: str) -> str:
    return (WORKFLOWS / name).read_text(encoding='utf-8')


def test_single_scheduled_post_close_orchestrator():
    master = _text('post-close-pipeline-v2.2.yml')
    assert "cron: '17 7 * * 1-5'" in master

    manual_components = [
        'daily.yml',
        'decision-system-v1.7.yml',
        'portfolio-risk-v1.8.yml',
        'validation-v1.7.yml',
        'validation-learning-v2.yml',
    ]
    for name in manual_components:
        text = _text(name)
        assert 'schedule:' not in text, f'{name} must stay manual-only'


def test_post_close_watchdog_has_staggered_idempotent_recovery_checks():
    text = _text('post-close-watchdog.yml')
    for cron in (
        "cron: '42 7 * * 1-5'",
        "cron: '12 8 * * 1-5'",
        "cron: '42 8 * * 1-5'",
        "cron: '12 9 * * 1-5'",
    ):
        assert cron in text
    assert 'active_count=' in text
    assert 'no duplicate dispatch' in text


def test_morning_intelligence_has_no_post_close_schedule():
    text = _text('intelligence-v1.6.yml')
    assert "cron: '15 22 * * 0-4'" in text
    assert "cron: '30 7 * * 1-5'" not in text


def test_master_pipeline_order_and_privacy_guards():
    text = _text('post-close-pipeline-v2.2.yml')
    expected = [
        '1. Daily Quant Screen',
        '3. Market Regime Engine',
        '4. Company Intelligence',
        '5. Exception Alerts',
        '7. Decision validation and benchmark-relative learning',
        '8. Private Portfolio Risk Engine',
        'Commit public-safe outputs once',
    ]
    positions = [text.index(x) for x in expected]
    assert positions == sorted(positions)
    assert "PORTFOLIO_DRIVE_WRITEBACK: 'false'" in text
    assert 'data/validation' in text
    assert '.private/portfolio_risk' in text
