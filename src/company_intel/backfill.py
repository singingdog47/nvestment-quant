"""Bounded historical EDINET discovery with checkpointed progress.

Never substitutes filing-event discovery for verified numeric coverage.
Public target codes only; no holdings, quantities, or brokerage balances.
"""
from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import requests

from .common import Event, normalize_code, now_iso, save_json, load_json, stable_hash
from .edinet import BASE

DEFAULT_LOOKBACK = 450


def _targets_by_code(targets: pd.DataFrame) -> dict[str, dict]:
    return {
        normalize_code(r.get("code")): r
        for r in targets.to_dict("records")
        if str(r.get("market") or "").upper() == "JP"
    }


def scan_historical_edinet(
    targets: pd.DataFrame, checkpoint_path: str | Path, *,
    today: date | None = None, days_per_run: int = 14,
    lookback_days: int = DEFAULT_LOOKBACK, session=None,
) -> tuple[list[Event], dict]:
    """Move the historical window only over successfully fetched calendar dates.

    A failed request stops the batch and retries that date at the next run;
    previously scanned dates do not repeat. No EDINET key means no cursor change.
    """
    today = today or date.today()
    state = load_json(checkpoint_path, {})
    anchor = date.fromisoformat(state.get("anchor_date", today.isoformat()))
    # After completing a historical window, a fresh cycle is explicit, not automatic.
    if state.get("complete"):
        return [], {**state, "status": "complete", "new_events": 0}
    if not os.getenv("EDINET_API_KEY"):
        return [], {**state, "status": "unconfigured", "new_events": 0}
    cursor = date.fromisoformat(state["next_date"]) if state.get("next_date") else anchor - timedelta(days=7)
    floor = anchor - timedelta(days=lookback_days)
    codes = _targets_by_code(targets)
    http = session or requests.Session()
    events: list[Event] = []
    scanned = 0
    errors = []
    until = max(cursor - timedelta(days=max(1, days_per_run) - 1), floor)
    current = cursor
    while current >= until:
        try:
            response = http.get(
                BASE,
                params={"date": current.isoformat(), "type": 2, "Subscription-Key": os.environ["EDINET_API_KEY"]},
                timeout=25,
            )
            response.raise_for_status()
            result = response.json()
            if not isinstance(result.get("results"), list):
                raise ValueError("EDINET response has no results list")
        except Exception as exc:
            errors.append(f"{current.isoformat()}:{type(exc).__name__}")
            break
        for filing in result["results"]:
            code = normalize_code(filing.get("secCode"))
            row = codes.get(code)
            if row is None:
                continue
            title = str(filing.get("docDescription") or "")
            # Do not mix ownership / registration documents into numeric filing ingestion.
            if not any(x in title for x in ("有価証券報告書", "半期報告書", "四半期報告書")):
                continue
            # Exclude amendment filings until revision precedence is independently validated.
            if "訂正" in title:
                continue
            docid = str(filing.get("docID") or "")
            if not docid:
                continue
            url = f"https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID={docid}"
            events.append(Event("JP", code, str(row.get("ticker") or code + ".T"),
                                str(row.get("name") or ""), current.isoformat(), "filing",
                                title, "", "EDINET", url, "primary", "ok", "high",
                                now_iso(), stable_hash(f"edinet|{docid}|{code}|{title}")[:24], ""))
        scanned += 1
        current -= timedelta(days=1)
    state = {
        "anchor_date": anchor.isoformat(),
        "next_date": current.isoformat(),
        "lookback_days": lookback_days,
        "days_scanned_this_run": scanned,
        "new_events": len(events),
        "failures": errors,
        "complete": current < floor,
        "status": "partial" if errors else ("complete" if current < floor else "in_progress"),
        "updated_at_utc": now_iso(),
    }
    save_json(checkpoint_path, state)
    return events, state


METRICS = ["net_sales_jpy", "operating_income_jpy", "net_income_jpy",
           "operating_cash_flow_jpy", "assets_jpy", "liabilities_jpy"]


def audit_primary_coverage(targets: pd.DataFrame, primary: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Per-JP-target and per-metric observed primary coverage, not a forecast."""
    jp = targets[targets["market"].eq("JP")].copy()
    jp["code"] = jp["code"].astype(str)
    columns = ["code", "ticker", "name", "source", "document_id", "filed_date", "status", *METRICS]
    if primary.empty:
        mapped = pd.DataFrame(columns=["code", "document_id", "filed_date", *METRICS])
    else:
        available = ["code", "document_id", "filed_date", *[m for m in METRICS if m in primary]]
        mapped = primary[available].copy()
        mapped["code"] = mapped["code"].astype(str)
        mapped = mapped.drop_duplicates("code", keep="first")
    out = jp[["code", "ticker", "name", "source"]].merge(mapped, on="code", how="left")
    metric_counts = {}
    for metric in METRICS:
        values = pd.to_numeric(out[metric], errors="coerce") if metric in out else pd.Series(index=out.index, dtype=float)
        out[metric] = values.notna().astype(int)
        metric_counts[metric] = int(out[metric].sum())
    out["status"] = out[METRICS].sum(axis=1).map(lambda n: "missing" if n == 0 else ("complete" if n == len(METRICS) else "partial"))
    n = len(out)
    report = {
        "generated_at_utc": now_iso(),
        "population": "JP Company Intelligence targets; not whole-market screening",
        "target_count": n,
        "companies_with_any_primary_metric": int(out["status"].ne("missing").sum()),
        "companies_with_all_six_metrics": int(out["status"].eq("complete").sum()),
        "coverage_any": float(out["status"].ne("missing").sum() / n) if n else 0,
        "metric_counts": metric_counts,
        "metric_coverage": {k: (v / n if n else 0) for k, v in metric_counts.items()},
        "note": "A metric is covered only when a verified numeric primary observation exists.",
    }
    return out[columns], report
