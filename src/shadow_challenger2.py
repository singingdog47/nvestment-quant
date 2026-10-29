"""Challenger 2: independent 5m-yen paper cohort forked from Challenger 1.

The committed state is an auditable, one-time fork of the Oct 28 ledger.
This runner never re-imports live Challenger 1 state, never creates real orders,
and refuses to silently open an empty account if the fork state is absent.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Callable

import shadow_challenger as engine

DATA_ROOT = Path("data")
CONFIG_FILE = Path("config/shadow_challenger2_v1.json")
OUT_DIR = DATA_ROOT / "shadow_challenger2"


def run(as_of: date | None = None, bar_source: Callable | None = None):
    cfg = engine.load_json(CONFIG_FILE)
    state = engine.load_json(OUT_DIR / "state.json")
    if not cfg or not state or "fork_metadata" not in state:
        raise RuntimeError("Challenger2 requires an audited fork state and config; refusing to create an empty 5m book.")
    if cfg["mode"] != "SHADOW_ONLY" or state["mode"] != "SHADOW_ONLY":
        raise ValueError("Only SHADOW_ONLY operation is permitted")
    if state["cohort"] != cfg["cohort"] or state["initial_cash_jpy"] != cfg["initial_cash_jpy"]:
        raise ValueError("Challenger2 cohort/capital mismatch")
    if cfg["initial_cash_jpy"] != 5_000_000:
        raise ValueError("Unexpected Challenger2 capital")
    fork = state["fork_metadata"]
    if fork["source_snapshot_date"] > (as_of.isoformat() if as_of else "9999-12-31"):
        raise ValueError("Cannot replay before the fork snapshot")

    # Run the existing OHLC-verified strategy engine with a distinct state directory
    # and a distinct configuration, without changing Challenger 1 global settings.
    old_data, old_out, old_config = engine.DATA, engine.OUT, engine.CONFIG
    try:
        engine.DATA, engine.OUT, engine.CONFIG = DATA_ROOT, OUT_DIR, CONFIG_FILE
        result = engine.run(as_of=as_of, bar_source=bar_source)
    finally:
        engine.DATA, engine.OUT, engine.CONFIG = old_data, old_out, old_config

    if result.get("status") in ("ALREADY_PROCESSED", "PRE_CLOSE_DEFERRED", "OUTSIDE_SESSION"):
        return result

    current = engine.load_json(OUT_DIR / "state.json")
    snapshot_date = fork["source_snapshot_date"]
    new_fills = [x for x in current.get("execution_log", [])
                 if x["date"] > snapshot_date and x.get("source", "").startswith("verified_")]
    new_trades = [x for x in current.get("trades", []) if x["date"] > snapshot_date]
    result["strategy"] = "CHALLENGER2"
    result["cohort"] = cfg["cohort"]
    result["fork"] = {
        "source_cohort": fork["source_cohort"],
        "source_snapshot_date": snapshot_date,
        "source_state_blob_sha": fork["source_state_blob_sha"],
        "source_nav_jpy": fork["source_nav_jpy"],
        "virtual_capital_injection_jpy": fork["capital_topup_jpy"],
        "starting_nav_jpy": fork["fork_target_nav_jpy"],
        "funding_is_not_profit": True,
        "inherited_executions": fork["pre_fork_executions"],
        "inherited_closed_trades": fork["pre_fork_trades"],
    }
    result["post_fork_verified_fills"] = len(new_fills)
    result["post_fork_closed_trades"] = len(new_trades)
    result["post_fork_verified_fill_log"] = new_fills[-10:]
    result["risk_budget"] = {
        "max_position_pct": cfg["risk"]["max_position_pct"],
        "maximum_ordinary_stop_loss_pct_of_starting_nav_estimate": round(
            100 * cfg["risk"]["max_position_pct"] *
            (cfg["risk"]["stop_loss_pct"] / 100 + 2 * cfg["execution"]["slippage_bps"] / 10000), 3),
        "estimated_only_market_gap_risk_unbounded": True,
        "max_gross_invested_pct": cfg["risk"]["max_gross_invested_pct"],
    }

    baseline = current.get("november_baseline_nav_jpy")
    if baseline and result["date"] >= "2026-11-01" and not result["unpriced_symbols"]:
        pct = 100 * (result["nav_jpy"] / baseline - 1)
        status = ("REVIEW_REQUIRED" if pct <= cfg["risk"]["monthly_review_pct"]
                  else "WARNING" if pct <= cfg["risk"]["monthly_loss_warning_pct"]
                  else "NORMAL")
    else:
        status = "BASELINE_OR_MONTH_NOT_READY"
    result["monthly_risk_status"] = status
    engine.write_json(OUT_DIR / "latest.json", result)

    report_file = OUT_DIR / "latest_report.md"
    report = report_file.read_text(encoding="utf-8")
    report = report.replace("# AI Challenger v1 — SHADOW ONLY",
                            "# AI Challenger 2 — 5m-yen fork — SHADOW ONLY", 1)
    report += (
        "\nFork: " + snapshot_date + " (" + fork["source_cohort"] + ")\n"
        + "Virtual cash injection: ¥" + f'{fork["capital_topup_jpy"]:,.2f}'
        + " (NOT investment return)\n"
        + "Independent verified fills after fork: " + str(len(new_fills)) + "\n"
        + "Monthly risk watch: " + status + "\n"
        + "Market gaps can exceed the planned per-trade loss budget.\n"
    )
    report_file.write_text(report, encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
