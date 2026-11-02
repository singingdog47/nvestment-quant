"""Prevent accidental GitHub Actions pending-run eviction of paper cohorts.

GitHub concurrency permits only one running and one pending run per group.
When multiple post-close children are enqueued simultaneously, a shared
group can cancel an earlier pending child even with cancel-in-progress=false.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WRITERS = {
    "shadow-challenger-v1.yml": "shadow-challenger1-writer",
    "shadow-challenger2.yml": "shadow-challenger2-writer",
    "ai-ma-shadow-v1.yml": "ai-ma-shadow-writer",
    "quant-health.yml": "quant-health-writer",
}


def test_post_close_paper_writers_have_distinct_concurrency_groups():
    groups = []
    for filename, expected in WRITERS.items():
        source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
        match = re.search(
            r"(?m)^concurrency:\s*\n\s+group:\s*([^\n]+)\n\s+cancel-in-progress:\s*([^\n]+)",
            source,
        )
        assert match is not None, filename
        assert match.group(1).strip() == expected, filename
        assert match.group(2).strip() == "false", filename
        groups.append(match.group(1).strip())
    assert len(groups) == len(set(groups))
    assert "repository-output-writer" not in groups


def test_independent_writers_retry_non_fast_forward_without_force_push():
    for filename in WRITERS:
        source = (ROOT / ".github" / "workflows" / filename).read_text(encoding="utf-8")
        assert "for attempt in 1 2 3 4; do" in source, filename
        assert "git pull --rebase origin main && git push origin HEAD:main" in source, filename
        assert "git rebase --abort" not in source, filename
        assert "git push --force" not in source, filename
        assert "Rebase conflict" in source, filename
