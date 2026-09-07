from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from contribution_rebalance import (
    analyze_contribution_rebalance,
    load_rebalance_policy,
    write_contribution_rebalance_report,
)
from private_drive import upload_or_replace


def _truthy(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def main() -> None:
    portfolio_path = Path(os.getenv("PORTFOLIO_PATH", ".private/portfolio_latest.csv"))
    out_dir = Path(os.getenv("PRIVATE_OUTPUT_DIR", ".private/portfolio_risk"))
    screen_path = Path(os.getenv("SCREEN_PATH", "data/screening_latest.csv"))
    policy_path = Path(os.getenv("CONTRIBUTION_REBALANCE_POLICY", "config/contribution_rebalance_v1.json"))

    if not portfolio_path.exists():
        raise FileNotFoundError(f"Private portfolio input not found: {portfolio_path}")

    portfolio = pd.read_csv(portfolio_path)
    screen = pd.read_csv(screen_path) if screen_path.exists() else pd.DataFrame()
    policy = load_rebalance_policy(policy_path)
    force_review = _truthy("REBALANCE_FORCE_REVIEW")

    report = analyze_contribution_rebalance(
        portfolio,
        screen,
        policy,
        as_of=datetime.now(timezone.utc).date(),
        force_review=force_review,
    )
    json_path, md_path = write_contribution_rebalance_report(report, out_dir)

    writeback = False
    if _truthy("REBALANCE_DRIVE_WRITEBACK"):
        upload_or_replace(json_path, json_path.name, "application/json")
        upload_or_replace(md_path, md_path.name, "text/markdown")
        writeback = True

    # Deliberately keep Actions logs free of portfolio weights and risk values.
    print(json.dumps({
        "version": report.get("version"),
        "status": report.get("status"),
        "decision_code": (report.get("decision") or {}).get("code"),
        "manual_setting_change_actionable": (report.get("decision") or {}).get("actionable_for_manual_setting_change"),
        "plan_changed_from_baseline": (report.get("decision") or {}).get("plan_changed_from_baseline"),
        "review_active": (report.get("review") or {}).get("review_active"),
        "private_drive_writeback": writeback,
        "privacy": "private_output_only",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
