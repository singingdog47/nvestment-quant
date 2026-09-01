from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

from alert_engine import detect_private_portfolio_alerts
from monthly_performance import PortfolioSnapshot, build_monthly_diagnostics, write_monthly_report
from portfolio_import import infer_portfolio_source_as_of, parse_rakuten_csv_bytes
from portfolio_policy_report import write_policy_report
from portfolio_valuation import build_portfolio_valuation, write_valuation_report
from private_account_import import (
    parse_account_summary_bytes,
    parse_buying_power_pdf,
    parse_orders_bytes,
    source_as_of,
)
from private_drive import (
    append_history_ledger,
    canonical_json_sha256,
    download_recent_files,
    encode_json_cell,
    file_sha256,
    upload_or_replace,
)
from portfolio_risk import main as run_risk
from release_status import SYSTEM_VERSION

JST = timezone(timedelta(hours=9))


def _truthy_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _source_local_date(meta: dict) -> str | None:
    as_of, _method = infer_portfolio_source_as_of(meta.get("name"), meta.get("modifiedTime"))
    dt = _parse_dt(as_of)
    return dt.astimezone(JST).date().isoformat() if dt is not None else None


def _target_date() -> str | None:
    value = os.getenv("PORTFOLIO_TARGET_DATE", "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise ValueError("PORTFOLIO_TARGET_DATE must be YYYY-MM-DD") from exc


def _build_latest_portfolio(private_dir: Path, candidates: list[tuple[Path, dict]]) -> tuple[Path, dict]:
    errors: list[dict] = []
    target = _target_date()
    eligible = [(p, m) for p, m in candidates if target is None or _source_local_date(m) == target]
    for path, meta in eligible:
        try:
            parsed = parse_rakuten_csv_bytes(path.read_bytes())
        except Exception as e:
            errors.append({"name": meta.get("name"), "error": f"{type(e).__name__}:{e}"})
            continue
        local = private_dir / "portfolio_latest.csv"
        parsed.portfolio.to_csv(local, index=False, encoding="utf-8")
        source_as_of_value, source_as_of_method = infer_portfolio_source_as_of(meta.get("name"), meta.get("modifiedTime"))
        manifest = {
            "status": "ok",
            "source_file": meta.get("name"),
            "source_modified_time": meta.get("modifiedTime"),
            "source_as_of": source_as_of_value,
            "source_as_of_method": source_as_of_method,
            "source_encoding": parsed.source_encoding,
            "rows_seen": parsed.rows_seen,
            "rows_kept": parsed.rows_kept,
            "market_value_total": float(parsed.portfolio["market_value"].sum()),
            "weight_sum": float(parsed.portfolio["weight"].sum()),
            "target_date": target,
        }
        (private_dir / "portfolio_import_latest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return local, manifest
    raise FileNotFoundError(
        f"No valid Rakuten Securities holdings CSV found for target={target or 'latest'}. "
        f"Checked {len(eligible)} eligible of {len(candidates)} files; sample errors={errors[:5]}"
    )


def _collect_monthly_snapshots(candidates: list[tuple[Path, dict]], cutoff_date: str | None = None) -> list[PortfolioSnapshot]:
    found: list[PortfolioSnapshot] = []
    seen_times: set[str] = set()
    for path, meta in candidates:
        local_date = _source_local_date(meta)
        if cutoff_date and local_date and local_date > cutoff_date:
            continue
        try:
            parsed = parse_rakuten_csv_bytes(path.read_bytes())
        except Exception:
            continue
        as_of, _method = infer_portfolio_source_as_of(meta.get("name"), meta.get("modifiedTime"))
        dt = _parse_dt(as_of)
        if dt is None:
            continue
        if cutoff_date and dt.astimezone(JST).date().isoformat() > cutoff_date:
            continue
        key = dt.isoformat()
        if key in seen_times:
            continue
        seen_times.add(key)
        found.append(PortfolioSnapshot(dt, parsed.portfolio, meta.get("name")))
    found.sort(key=lambda x: x.as_of)
    if len(found) < 2:
        return found
    latest = found[-1]
    latest_local = latest.as_of.astimezone(JST)
    month_start_local = datetime(latest_local.year, latest_local.month, 1, tzinfo=JST)
    month_start_utc = month_start_local.astimezone(timezone.utc)
    previous = [x for x in found[:-1] if x.as_of < month_start_utc]
    if previous:
        start = previous[-1]
    else:
        in_month = [
            x for x in found
            if (x.as_of.astimezone(JST).year, x.as_of.astimezone(JST).month) == (latest_local.year, latest_local.month)
        ]
        start = in_month[0] if in_month else found[0]
    return [start, latest] if start.as_of != latest.as_of else [latest]


def _build_latest_account_inputs(private_dir: Path, candidates: list[tuple[Path, dict]]) -> dict:
    selected: dict[str, dict] = {}
    errors: list[dict] = []
    parsers = (
        ("account_summary", lambda p: parse_account_summary_bytes(p.read_bytes())),
        ("orders", lambda p: parse_orders_bytes(p.read_bytes())),
        ("buying_power", parse_buying_power_pdf),
    )
    for path, meta in candidates:
        for kind, parser in parsers:
            if kind in selected:
                continue
            try:
                parsed = parser(path)
            except Exception as exc:
                errors.append({"name": meta.get("name"), "kind": kind, "error": f"{type(exc).__name__}:{exc}"})
                continue
            as_of, method = source_as_of(meta.get("name"), meta.get("modifiedTime"))
            if kind == "buying_power" and parsed.get("source_as_of"):
                as_of, method = parsed["source_as_of"], "pdf_embedded_timestamp"
            age_days = None
            if as_of and len(str(as_of)) > 10:
                try:
                    observed = datetime.fromisoformat(str(as_of).replace("Z", "+00:00"))
                    age_days = max(0.0, (datetime.now(timezone.utc) - observed.astimezone(timezone.utc)).total_seconds() / 86400)
                except ValueError:
                    pass
            max_age_days = float(os.getenv("PRIVATE_INPUT_MAX_AGE_DAYS", "7"))
            selected[kind] = {
                "source_file": meta.get("name"), "source_modified_time": meta.get("modifiedTime"),
                "source_as_of": as_of, "source_as_of_method": method, "age_days": age_days,
                "data_status": "stale" if age_days is not None and age_days > max_age_days else "ok", **parsed,
            }
    missing = [x for x in ("account_summary", "orders", "buying_power") if x not in selected]
    stale = [kind for kind, item in selected.items() if item.get("data_status") == "stale"]
    snapshot = {
        "status": "ok" if not missing and not stale else "partial",
        "selection_policy": "newest_parseable_file_by_drive_modified_time",
        "inputs": selected,
        "missing_input_types": missing,
        "stale_input_types": stale,
        "parse_errors_count": len(errors),
    }
    (private_dir / "account_inputs_latest.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return snapshot


def _write_private_alerts(out_dir: Path) -> bool:
    risk_path = out_dir / "portfolio_risk_latest.json"
    if not risk_path.exists():
        return False
    report = json.loads(risk_path.read_text(encoding="utf-8")); alerts = detect_private_portfolio_alerts(report)
    (out_dir / "portfolio_alerts_latest.json").write_text(json.dumps(alerts, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Private Portfolio Alerts v1.9.1", "", f"Generated: {alerts.get('generated_at')}",
        f"Highest severity: {alerts.get('highest_severity')}", "", "## Alerts",
    ]
    items = alerts.get("alerts") or []
    if not items:
        lines.append("- No portfolio-risk exceptions detected.")
    else:
        for a in items:
            lines += [f"- **{a.get('severity')}** {a.get('code')}: {a.get('title')}", f"  - {a.get('message')}"]
    lines += ["", "## Privacy", "- This file is private and must never be committed or uploaded as a public Actions artifact."]
    (out_dir / "portfolio_alerts_latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def _write_valuation_and_monthly(
    local_portfolio: Path, candidates: list[tuple[Path, dict]], out_dir: Path, cutoff_date: str | None
) -> tuple[dict, dict]:
    portfolio = pd.read_csv(local_portfolio)
    screen_path = Path(os.getenv("SCREEN_PATH", "data/screening_latest.csv"))
    screening = pd.read_csv(screen_path) if screen_path.exists() else pd.DataFrame()
    valuation = build_portfolio_valuation(portfolio, screening)
    write_valuation_report(valuation, out_dir)
    snapshots = _collect_monthly_snapshots(candidates, cutoff_date=cutoff_date)
    monthly = build_monthly_diagnostics(snapshots)
    write_monthly_report(monthly, out_dir)
    return valuation, monthly


def _maybe_write_back_to_drive(private_dir: Path, out_dir: Path) -> bool:
    if not _truthy_env("PORTFOLIO_DRIVE_WRITEBACK"):
        return False
    for path, name, mime in (
        (private_dir / "portfolio_latest.csv", "portfolio_latest.csv", "text/csv"),
        (private_dir / "portfolio_import_latest.json", "portfolio_import_latest.json", "application/json"),
        (out_dir / "portfolio_risk_latest.json", "portfolio_risk_latest.json", "application/json"),
        (out_dir / "portfolio_risk_latest.md", "portfolio_risk_latest.md", "text/markdown"),
        (out_dir / "portfolio_alerts_latest.json", "portfolio_alerts_latest.json", "application/json"),
        (out_dir / "portfolio_alerts_latest.md", "portfolio_alerts_latest.md", "text/markdown"),
        (out_dir / "portfolio_policy_latest.json", "portfolio_policy_latest.json", "application/json"),
        (out_dir / "portfolio_policy_latest.md", "portfolio_policy_latest.md", "text/markdown"),
        (out_dir / "portfolio_valuation_latest.json", "portfolio_valuation_latest.json", "application/json"),
        (out_dir / "portfolio_valuation_latest.md", "portfolio_valuation_latest.md", "text/markdown"),
        (out_dir / "portfolio_monthly_latest.json", "portfolio_monthly_latest.json", "application/json"),
        (out_dir / "portfolio_monthly_latest.md", "portfolio_monthly_latest.md", "text/markdown"),
    ):
        if path.exists():
            upload_or_replace(path, name, mime)
    return True


def _persist_private_history(
    private_dir: Path,
    out_dir: Path,
    import_manifest: dict,
    valuation: dict,
    monthly: dict,
) -> dict:
    if not _truthy_env("PORTFOLIO_HISTORY_WRITEBACK"):
        return {"status": "disabled", "written": False}

    source_dt = _parse_dt(import_manifest.get("source_as_of"))
    if source_dt is None:
        source_dt = datetime.now(timezone.utc)
        snapshot_date = source_dt.astimezone(JST).date().isoformat()
        date_basis = "write_time_fallback"
    else:
        snapshot_date = source_dt.astimezone(JST).date().isoformat()
        date_basis = str(import_manifest.get("source_as_of_method") or "source_as_of")

    portfolio_path = private_dir / "portfolio_latest.csv"
    if not portfolio_path.exists():
        return {"status": "withheld", "written": False, "reason": "portfolio_snapshot_missing"}
    portfolio = pd.read_csv(portfolio_path)
    portfolio_records = json.loads(portfolio.to_json(orient="records", force_ascii=False))
    portfolio_payload = {
        "schema_version": "1.0",
        "snapshot_date": snapshot_date,
        "rows": portfolio_records,
        "row_count": int(len(portfolio)),
        "market_value_total_jpy": float(pd.to_numeric(portfolio.get("market_value"), errors="coerce").fillna(0).sum()),
    }

    import_mv = float(import_manifest.get("market_value_total") or 0.0)
    valuation_mv = float(valuation.get("portfolio_market_value_jpy") or 0.0)
    reconciliation_difference = valuation_mv - import_mv
    snapshot_manifest = {
        "snapshot_schema_version": "1.1",
        "system_version": SYSTEM_VERSION,
        "snapshot_date": snapshot_date,
        "snapshot_date_basis": date_basis,
        "source": {
            "file": import_manifest.get("source_file"),
            "modified_time": import_manifest.get("source_modified_time"),
            "as_of": import_manifest.get("source_as_of"),
            "as_of_method": import_manifest.get("source_as_of_method"),
            "rows_kept": import_manifest.get("rows_kept"),
        },
        "quality": {
            "import_status": import_manifest.get("status"),
            "valuation_status": valuation.get("status"),
            "valuation_analysis_mode": valuation.get("analysis_mode"),
            "valuation_decision_actionable": valuation.get("decision_actionable"),
            "valuation_evidence_tier": valuation.get("evidence_tier"),
            "valuation_coverage": valuation.get("coverage"),
            "monthly_status": monthly.get("status"),
            "monthly_twr_status": (monthly.get("performance") or {}).get("twr_status"),
            "market_value_reconciliation_difference_jpy": reconciliation_difference,
        },
        "engines": {
            "portfolio_valuation": valuation.get("version"),
            "monthly_performance": monthly.get("version"),
        },
        "governance": {
            "storage_mode": "user_owned_google_sheet_append_only",
            "immutable_history": True,
            "same_hash_rerun_is_idempotent": True,
            "changed_same_date_creates_corrected_revision": True,
            "public_github_write_prohibited": True,
        },
    }
    (out_dir / "snapshot_manifest_latest.json").write_text(
        json.dumps(snapshot_manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_file = str(import_manifest.get("source_file") or "")
    source_as_of = str(import_manifest.get("source_as_of") or "")
    entries = [
        {
            "snapshot_date": snapshot_date,
            "snapshot_kind": "portfolio",
            "sha256": file_sha256(portfolio_path),
            "system_version": SYSTEM_VERSION,
            "source_file": source_file,
            "source_as_of": source_as_of,
            "status": import_manifest.get("status"),
            "analysis_mode": "source_snapshot",
            "evidence_tier": "brokerage_export",
            "coverage_json": encode_json_cell({"holdings_rows": len(portfolio), "weight_sum": import_manifest.get("weight_sum")}),
            "payload_json": encode_json_cell(portfolio_payload),
            "created_at_utc": created_at,
        },
        {
            "snapshot_date": snapshot_date,
            "snapshot_kind": "valuation",
            "sha256": canonical_json_sha256(valuation),
            "system_version": SYSTEM_VERSION,
            "source_file": source_file,
            "source_as_of": source_as_of,
            "status": valuation.get("status"),
            "analysis_mode": valuation.get("analysis_mode"),
            "evidence_tier": valuation.get("evidence_tier"),
            "coverage_json": encode_json_cell(valuation.get("coverage") or {}),
            "payload_json": encode_json_cell(valuation),
            "created_at_utc": created_at,
        },
        {
            "snapshot_date": snapshot_date,
            "snapshot_kind": "monthly",
            "sha256": canonical_json_sha256(monthly),
            "system_version": SYSTEM_VERSION,
            "source_file": source_file,
            "source_as_of": source_as_of,
            "status": monthly.get("status"),
            "analysis_mode": monthly.get("analysis_mode"),
            "evidence_tier": "portfolio_snapshots",
            "coverage_json": encode_json_cell({
                "boundary_quality": monthly.get("boundary_quality"),
                "attribution_coverage": (monthly.get("attribution") or {}).get("stable_quantity_start_value_coverage"),
                "twr_status": (monthly.get("performance") or {}).get("twr_status"),
            }),
            "payload_json": encode_json_cell(monthly),
            "created_at_utc": created_at,
        },
        {
            "snapshot_date": snapshot_date,
            "snapshot_kind": "manifest",
            "sha256": canonical_json_sha256(snapshot_manifest),
            "system_version": SYSTEM_VERSION,
            "source_file": source_file,
            "source_as_of": source_as_of,
            "status": "ok",
            "analysis_mode": valuation.get("analysis_mode"),
            "evidence_tier": valuation.get("evidence_tier"),
            "coverage_json": encode_json_cell(snapshot_manifest.get("quality") or {}),
            "payload_json": encode_json_cell(snapshot_manifest),
            "created_at_utc": created_at,
        },
    ]
    ledger = append_history_ledger(entries)
    return {
        "status": ledger.get("status"),
        "written": True,
        "storage_mode": "user_owned_google_sheet_append_only",
        "snapshot_date": snapshot_date,
        "snapshot_date_basis": date_basis,
        "ledger_id": ledger.get("ledger_id"),
        "appended": ledger.get("appended"),
        "idempotent": ledger.get("idempotent"),
        "rows": ledger.get("rows"),
    }


def main() -> None:
    private_dir = Path(os.getenv("PRIVATE_WORKDIR", ".private")); private_dir.mkdir(parents=True, exist_ok=True)
    candidates = download_recent_files(private_dir / "drive_inbox", limit=int(os.getenv("PORTFOLIO_SCAN_LIMIT", "50")))
    local_portfolio, manifest = _build_latest_portfolio(private_dir, candidates)
    account_inputs = _build_latest_account_inputs(private_dir, candidates)
    os.environ["PORTFOLIO_PATH"] = str(local_portfolio)
    if manifest.get("source_as_of"):
        os.environ["PORTFOLIO_SOURCE_AS_OF"] = str(manifest["source_as_of"])
    os.environ.setdefault("PRIVATE_OUTPUT_DIR", str(private_dir / "portfolio_risk")); run_risk()
    out_dir = Path(os.environ["PRIVATE_OUTPUT_DIR"])
    policy_payload = write_policy_report(local_portfolio, account_inputs, out_dir)
    valuation_payload, monthly_payload = _write_valuation_and_monthly(
        local_portfolio, candidates, out_dir, cutoff_date=_target_date()
    )
    private_alerts_written = _write_private_alerts(out_dir)
    writeback = _maybe_write_back_to_drive(private_dir, out_dir)
    history = _persist_private_history(private_dir, out_dir, manifest, valuation_payload, monthly_payload)
    print(json.dumps({
        "status": "ok",
        "source_file": manifest.get("source_file"),
        "source_as_of": manifest.get("source_as_of"),
        "target_date": manifest.get("target_date"),
        "rows_kept": manifest.get("rows_kept"),
        "weight_sum": manifest.get("weight_sum"),
        "account_input_status": account_inputs.get("status"),
        "account_input_types": sorted((account_inputs.get("inputs") or {}).keys()),
        "account_selection_policy": account_inputs.get("selection_policy"),
        "portfolio_policy_status": policy_payload.get("status"),
        "portfolio_valuation_status": valuation_payload.get("status"),
        "portfolio_valuation_mode": valuation_payload.get("analysis_mode"),
        "monthly_performance_status": monthly_payload.get("status"),
        "monthly_twr_status": (monthly_payload.get("performance") or {}).get("twr_status"),
        "private_alerts_written": private_alerts_written,
        "drive_writeback": writeback,
        "history_writeback": history,
        "privacy_mode": "private_drive_sheet_history" if history.get("written") else (
            "private_drive_writeback" if writeback else "ephemeral_runner_only"
        ),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
