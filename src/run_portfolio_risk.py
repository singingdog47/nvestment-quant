from __future__ import annotations

import json
import os
from pathlib import Path

from alert_engine import detect_private_portfolio_alerts
from portfolio_import import infer_portfolio_source_as_of, parse_rakuten_csv_bytes
from private_drive import download_recent_csvs, upload_or_replace
from portfolio_risk import main as run_risk


def _truthy_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _build_latest_portfolio(private_dir: Path) -> tuple[Path, dict]:
    inbox = private_dir / "drive_inbox"
    candidates = download_recent_csvs(inbox, limit=int(os.getenv("PORTFOLIO_SCAN_LIMIT", "25")))
    errors: list[dict] = []
    for path, meta in candidates:
        # Generated normalized/output CSV files are harmless: the Rakuten parser
        # rejects them because they lack the Japanese holdings-detail header.
        try:
            parsed = parse_rakuten_csv_bytes(path.read_bytes())
        except Exception as e:
            errors.append({"name": meta.get("name"), "error": f"{type(e).__name__}:{e}"})
            continue
        local = private_dir / "portfolio_latest.csv"
        parsed.portfolio.to_csv(local, index=False, encoding="utf-8")
        source_as_of, source_as_of_method = infer_portfolio_source_as_of(
            meta.get("name"), meta.get("modifiedTime")
        )
        manifest = {
            "status": "ok",
            "source_file": meta.get("name"),
            "source_modified_time": meta.get("modifiedTime"),
            "source_as_of": source_as_of,
            "source_as_of_method": source_as_of_method,
            "source_encoding": parsed.source_encoding,
            "rows_seen": parsed.rows_seen,
            "rows_kept": parsed.rows_kept,
            "market_value_total": float(parsed.portfolio["market_value"].sum()),
            "weight_sum": float(parsed.portfolio["weight"].sum()),
        }
        (private_dir / "portfolio_import_latest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return local, manifest
    raise FileNotFoundError(
        "No valid Rakuten Securities holdings CSV found in private Drive folder. "
        f"Checked {len(candidates)} CSV/text files; sample errors={errors[:5]}"
    )


def _write_private_alerts(out_dir: Path) -> bool:
    risk_path = out_dir / "portfolio_risk_latest.json"
    if not risk_path.exists():
        return False
    report = json.loads(risk_path.read_text(encoding="utf-8"))
    alerts = detect_private_portfolio_alerts(report)
    alert_json = out_dir / "portfolio_alerts_latest.json"
    alert_json.write_text(json.dumps(alerts, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Private Portfolio Alerts v1.9.1",
        "",
        f"Generated: {alerts.get('generated_at')}",
        f"Highest severity: {alerts.get('highest_severity')}",
        "",
        "## Alerts",
    ]
    items = alerts.get("alerts") or []
    if not items:
        lines.append("- No portfolio-risk exceptions detected.")
    else:
        for a in items:
            lines.append(f"- **{a.get('severity')}** {a.get('code')}: {a.get('title')}")
            lines.append(f"  - {a.get('message')}")
    lines += ["", "## Privacy", "- This file is private and ephemeral. It must never be committed or uploaded as a public Actions artifact."]
    (out_dir / "portfolio_alerts_latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def _maybe_write_back_to_drive(private_dir: Path, out_dir: Path) -> bool:
    """Optionally write normalized/private outputs back to Drive.

    Service accounts on regular My Drive do not have independent storage quota,
    so creating new files can fail with storageQuotaExceeded. The safe default is
    therefore read-only Drive access: inputs are downloaded, analysis runs in the
    ephemeral GitHub Actions workspace, and no portfolio data is persisted to the
    public repository or Actions artifacts.

    Set PORTFOLIO_DRIVE_WRITEBACK=true only when the configured Drive backend can
    accept service-account writes (for example, a Shared Drive or another setup
    that provides writable quota).
    """
    if not _truthy_env("PORTFOLIO_DRIVE_WRITEBACK"):
        return False

    upload_or_replace(private_dir / "portfolio_latest.csv", "portfolio_latest.csv", "text/csv")
    upload_or_replace(
        private_dir / "portfolio_import_latest.json",
        "portfolio_import_latest.json",
        "application/json",
    )
    upload_or_replace(
        out_dir / "portfolio_risk_latest.json",
        "portfolio_risk_latest.json",
        "application/json",
    )
    upload_or_replace(
        out_dir / "portfolio_risk_latest.md",
        "portfolio_risk_latest.md",
        "text/markdown",
    )
    # Private alerts are written back only when the whole private writeback mode
    # has explicitly been enabled for a backend with writable quota.
    for name, mime in (
        ("portfolio_alerts_latest.json", "application/json"),
        ("portfolio_alerts_latest.md", "text/markdown"),
    ):
        p = out_dir / name
        if p.exists():
            upload_or_replace(p, name, mime)
    return True


def main() -> None:
    private_dir = Path(os.getenv("PRIVATE_WORKDIR", ".private"))
    private_dir.mkdir(parents=True, exist_ok=True)

    local_portfolio, manifest = _build_latest_portfolio(private_dir)

    os.environ["PORTFOLIO_PATH"] = str(local_portfolio)
    if manifest.get("source_as_of"):
        os.environ["PORTFOLIO_SOURCE_AS_OF"] = str(manifest["source_as_of"])
    os.environ.setdefault("PRIVATE_OUTPUT_DIR", str(private_dir / "portfolio_risk"))
    run_risk()

    out_dir = Path(os.environ["PRIVATE_OUTPUT_DIR"])
    private_alerts_written = _write_private_alerts(out_dir)
    writeback = _maybe_write_back_to_drive(private_dir, out_dir)

    # Do not print holdings, risk values, or alert details into Actions logs.
    print(
        json.dumps(
            {
                "status": "ok",
                "source_file": manifest.get("source_file"),
                "rows_kept": manifest.get("rows_kept"),
                "weight_sum": manifest.get("weight_sum"),
                "private_alerts_written": private_alerts_written,
                "drive_writeback": writeback,
                "privacy_mode": "ephemeral_runner_only" if not writeback else "private_drive_writeback",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
