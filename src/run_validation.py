from __future__ import annotations

from validation.decision_log import capture_decision_snapshot
from validation.evaluate import evaluate_due_outcomes
from validation.report import build_validation_report


def main() -> None:
    path = capture_decision_snapshot()
    updated = evaluate_due_outcomes()
    report = build_validation_report()
    print(f"decision_snapshot={path}")
    print(f"outcome_records_updated={updated}")
    print(f"validation_report={report}")


if __name__ == "__main__":
    main()
