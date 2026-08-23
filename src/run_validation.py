from __future__ import annotations

from validation.decision_log import capture_decision_snapshot
from validation.evaluate import evaluate_due_outcomes
from validation.learning import write_learning_outputs
from validation.report import build_validation_report


def main() -> None:
    path = capture_decision_snapshot()
    updated = evaluate_due_outcomes()
    report = build_validation_report()
    learning_json, learning_md = write_learning_outputs()
    print(f"decision_snapshot={path}")
    print(f"outcome_records_updated={updated}")
    print(f"validation_report={report}")
    print(f"learning_json={learning_json}")
    print(f"learning_report={learning_md}")


if __name__ == "__main__":
    main()
