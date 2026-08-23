from pathlib import Path

from tools import preflight_v1_3


def test_daily_quant_screen_implementation_is_preserved():
    for source in preflight_v1_3.REQUIRED_V1_3_SOURCES:
        assert Path(source).is_file(), f"missing Daily Quant Screen source: {source}"

    workflow = Path(".github/workflows/daily.yml").read_text(encoding="utf-8")
    assert "name: Daily Quant Screen" in workflow
    assert 'cron: "17 7 * * 1-5"' in workflow


def test_generated_output_workflows_are_serialized():
    workflows = [
        Path(".github/workflows/daily.yml"),
        Path(".github/workflows/intelligence-v1.6.yml"),
    ]

    for path in workflows:
        workflow = path.read_text(encoding="utf-8")
        assert "group: repository-output-writer" in workflow
        assert "cancel-in-progress: false" in workflow
