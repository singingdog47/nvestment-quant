from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from googleapiclient.errors import HttpError

from contribution_rebalance import (
    analyze_contribution_rebalance,
    load_rebalance_policy,
    write_contribution_rebalance_report,
)
from private_drive import upload_or_replace


def _truthy(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _safe_drive_writeback(paths: list[tuple[Path, str]]) -> tuple[bool, str]:
    """Best-effort private Drive writeback.

    The rebalance analysis itself must not fail merely because the service account
    cannot create files in My Drive (service accounts have no personal storage
    quota). Keep the private report ephemeral on the runner and expose only a
    coarse status in Actions logs.
    """
    try:
        for path, mime_type in paths:
            upload_or_replace(path, path.name, mime_type)
        return True, "ok"
    except HttpError as exc:
        status = getattr(exc.resp, "status", None)
        # Do not print response bodies: they can contain Drive/file metadata.
        if status == 403:
            return False, "drive_writeback_unavailable_403"
        return False, f"drive_writeback_http_{status or 'unknown'}"
    except Exception:
        # Writeback is auxiliary. Preserve the completed private analysis while
        # keeping potentially sensitive exception details out of public logs.
        return False, "drive_writeback_failed"


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
    writeback_status = "disabled"
    if _truthy("REBALANCE_DRIVE_WRITEBACK"):
        writeback, writeback_status = _safe_drive_writeback([
            (json_path, "application/json"),
            (md_path, "text/markdown"),
        ])

    # Deliberately keep Actions logs free of portfolio weights and risk values.
    print(json.dumps({
        "version": report.get("version"),
        "status": report.get("status"),
        "decision_code": (report.get("decision") or {}).get("code"),
        "manual_setting_change_actionable": (report.get("decision") or {}).get("actionable_for_manual_setting_change"),
        "plan_changed_from_baseline": (report.get("decision") or {}).get("plan_changed_from_baseline"),
        "review_active": (report.get("review") or {}).get("review_active"),
        "private_drive_writeback": writeback,
        "private_drive_writeback_status": writeback_status,
        "privacy": "private_output_only",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
