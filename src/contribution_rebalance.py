from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from .portfolio_risk import (
        RiskConfig,
        build_return_matrix,
        factor_tilts,
        fetch_close,
        normalize_portfolio,
        portfolio_metrics,
        yahoo_symbol,
    )
except ImportError:  # direct script execution with PYTHONPATH=src
    from portfolio_risk import (
        RiskConfig,
        build_return_matrix,
        factor_tilts,
        fetch_close,
        normalize_portfolio,
        portfolio_metrics,
        yahoo_symbol,
    )

VERSION = "1.0.0"
DEFAULT_POLICY = Path("config/contribution_rebalance_v1.json")


def load_rebalance_policy(path: str | Path = DEFAULT_POLICY) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _text(value: Any) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def _number(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if pd.notna(x) else None


def _review_window(as_of: date, policy: dict[str, Any]) -> bool:
    cfg = policy["review"]
    return (
        as_of.month == int(cfg["review_month"])
        and int(cfg["review_day_start"]) <= as_of.day <= int(cfg["review_day_end"])
    )


def _match_proxy_rule(name: str, policy: dict[str, Any]) -> dict[str, Any] | None:
    folded = name.casefold()
    for rule in policy.get("risk_proxy_rules", []):
        patterns = [_text(x).casefold() for x in rule.get("contains", []) if _text(x)]
        if patterns and any(p in folded for p in patterns):
            return rule
    return None


def prepare_rebalance_portfolio(
    portfolio: pd.DataFrame, policy: dict[str, Any] | None = None
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Prepare a private risk-only copy of the portfolio.

    Explicit private overlay columns (`risk_proxy_symbol`, `rebalance_bucket`)
    take precedence.  Otherwise only documented public index-fund proxy rules
    are used.  The source portfolio itself is never modified or written back.
    """
    p = policy or load_rebalance_policy()
    x = portfolio.copy()
    if "market_value" not in x.columns:
        raise ValueError("portfolio requires market_value")

    proxy_count = 0
    proxy_weight_jpy = 0.0
    buckets: list[str] = []
    symbols: list[str | None] = []
    proxy_bases: list[str] = []

    for _, row in x.iterrows():
        explicit_proxy = _text(row.get("risk_proxy_symbol"))
        explicit_bucket = _text(row.get("rebalance_bucket"))
        explicit_basis = _text(row.get("risk_proxy_basis"))
        name = _text(row.get("name"))
        rule = None if explicit_proxy and explicit_bucket else _match_proxy_rule(name, p)

        bucket = explicit_bucket or _text((rule or {}).get("rebalance_bucket")) or "other"
        proxy = explicit_proxy or _text((rule or {}).get("proxy_symbol"))
        basis = explicit_basis or _text((rule or {}).get("basis"))

        if proxy:
            symbol = proxy
            proxy_count += 1
            proxy_weight_jpy += float(pd.to_numeric(row.get("market_value"), errors="coerce") or 0.0)
            proxy_bases.append(basis or "explicit_private_proxy")
        else:
            symbol = yahoo_symbol(row)
            proxy_bases.append("direct_market_symbol" if symbol else "unpriced")
        buckets.append(bucket)
        symbols.append(symbol)

    x["rebalance_bucket"] = buckets
    x["symbol"] = symbols
    x["risk_proxy_basis"] = proxy_bases

    mv = pd.to_numeric(x["market_value"], errors="coerce").fillna(0.0)
    total = float(mv.sum())
    if total <= 0:
        raise ValueError("portfolio market_value sum must be positive")
    x["weight"] = mv / total

    quality = {
        "proxy_positions": proxy_count,
        "proxy_market_value_weight": proxy_weight_jpy / total,
        "explicit_or_policy_bucket_coverage": float(
            x.loc[x["rebalance_bucket"].ne("other"), "weight"].sum()
        ),
    }
    return x.reset_index(drop=True), quality


def _risk_contribution_by_bucket(
    portfolio: pd.DataFrame, risk_contribution: dict[str, float]
) -> dict[str, float]:
    if not risk_contribution:
        return {}
    out: dict[str, float] = {}
    for symbol, contribution in risk_contribution.items():
        rows = portfolio.loc[portfolio["symbol"].astype(str).eq(str(symbol))]
        if rows.empty:
            continue
        symbol_weight = float(rows["weight"].sum())
        if symbol_weight <= 0:
            continue
        for bucket, grp in rows.groupby("rebalance_bucket"):
            share = float(grp["weight"].sum()) / symbol_weight
            out[str(bucket)] = out.get(str(bucket), 0.0) + float(contribution) * share
    return out


def _standard_nisa_routing(
    growth_tilt_jpy: int, policy: dict[str, Any]
) -> dict[str, Any]:
    total = int(policy["objective"]["base_monthly_contribution_jpy"])
    core = total - int(growth_tilt_jpy)
    nisa = policy["nisa_routing"]
    tsumitate_cap = int(nisa["tsumitate_monthly_cap_jpy"])
    core_tsumitate = min(core, tsumitate_cap)
    core_growth = max(0, core - core_tsumitate)
    growth_growth = int(growth_tilt_jpy)
    annual_growth_used = (core_growth + growth_growth) * 12
    annual_growth_cap = int(nisa["growth_annual_cap_jpy"])
    return {
        "monthly_total_jpy": total,
        "diversified_core_total_jpy": core,
        "growth_tilt_total_jpy": int(growth_tilt_jpy),
        "nisa_tsumitate_diversified_core_jpy": core_tsumitate,
        "nisa_growth_diversified_core_jpy": core_growth,
        "nisa_growth_growth_tilt_jpy": growth_growth,
        "annual_nisa_growth_used_by_auto_contributions_jpy": annual_growth_used,
        "annual_nisa_growth_remaining_for_satellite_jpy": max(0, annual_growth_cap - annual_growth_used),
        "current_year_capacity_check_required": bool(
            nisa.get("current_year_remaining_capacity_must_be_checked_before_applying", True)
        ),
    }


def _threshold_severity(
    growth_risk: float | None,
    growth_weight: float,
    policy: dict[str, Any],
) -> str:
    cfg = policy["risk_model"]
    if str(cfg.get("threshold_status")) != "active":
        return "calibration_required"

    severe = False
    mild = False
    severe_risk = _number(cfg.get("severe_upper_growth_risk_contribution"))
    mild_risk = _number(cfg.get("mild_upper_growth_risk_contribution"))
    severe_weight = _number(cfg.get("severe_upper_growth_market_value_weight"))
    mild_weight = _number(cfg.get("mild_upper_growth_market_value_weight"))

    if severe_risk is not None and growth_risk is not None and growth_risk >= severe_risk:
        severe = True
    if severe_weight is not None and growth_weight >= severe_weight:
        severe = True
    if mild_risk is not None and growth_risk is not None and growth_risk >= mild_risk:
        mild = True
    if mild_weight is not None and growth_weight >= mild_weight:
        mild = True

    if severe:
        return "severe"
    if mild:
        return "mild"
    return "normal"


def analyze_contribution_rebalance(
    portfolio: pd.DataFrame,
    screen: pd.DataFrame | None = None,
    policy: dict[str, Any] | None = None,
    *,
    as_of: date | None = None,
    force_review: bool = False,
    fetcher=fetch_close,
) -> dict[str, Any]:
    p = policy or load_rebalance_policy()
    as_of_date = as_of or datetime.now(timezone.utc).date()
    prepared, prep_quality = prepare_rebalance_portfolio(portfolio, p)

    risk_cfg = p["risk_model"]
    cfg = RiskConfig(
        lookback_days=int(risk_cfg.get("lookback_days", 400)),
        min_observations=int(risk_cfg.get("min_observations", 120)),
        benchmark=str(risk_cfg.get("benchmark", "1306.T")),
    )
    symbols = [s for s in prepared["symbol"].dropna().astype(str).unique().tolist() if s]
    if cfg.benchmark:
        symbols.append(cfg.benchmark)
    returns, fetch_errors = build_return_matrix(symbols, cfg, fetcher=fetcher)
    metrics = portfolio_metrics(prepared, returns, cfg.benchmark, cfg.var_confidence)
    risk_by_bucket = _risk_contribution_by_bucket(prepared, metrics.get("risk_contribution", {}))

    growth_mask = prepared["rebalance_bucket"].astype(str).eq("growth_tilt")
    growth_weight = float(prepared.loc[growth_mask, "weight"].sum())
    growth_risk = risk_by_bucket.get("growth_tilt")
    market_data_coverage = float(metrics.get("portfolio_weight_coverage") or 0.0)

    raw_for_factors = normalize_portfolio(portfolio)
    factors = factor_tilts(raw_for_factors, screen if screen is not None else pd.DataFrame())
    growth_factor = factors.get("growth_score", {"value": None, "coverage": 0.0})

    in_window = _review_window(as_of_date, p)
    review_active = bool(force_review or in_window)
    threshold_state = str(risk_cfg.get("threshold_status") or "calibration_required")
    min_coverage = float(risk_cfg.get("minimum_market_data_weight_coverage", 0.80))

    if not review_active:
        decision = "NO_CHANGE_OUTSIDE_REVIEW_WINDOW"
        growth_monthly = int(p["baseline_contribution"]["growth_tilt_jpy"])
        actionable = False
        reason = "Annual diagnostic window is closed; keep the last approved contribution plan."
    elif threshold_state != "active":
        decision = "CALIBRATION_REQUIRED_KEEP_BASELINE"
        growth_monthly = int(p["baseline_contribution"]["growth_tilt_jpy"])
        actionable = False
        reason = "Live risk metrics are available for calibration, but policy thresholds are intentionally not active yet."
    elif market_data_coverage < min_coverage:
        decision = "WITHHELD_DATA_COVERAGE_KEEP_BASELINE"
        growth_monthly = int(p["baseline_contribution"]["growth_tilt_jpy"])
        actionable = False
        reason = "Historical market-data coverage is below the policy minimum; do not change contributions from incomplete evidence."
    else:
        severity = _threshold_severity(growth_risk, growth_weight, p)
        if severity == "severe":
            growth_monthly = 0
            decision = "REDUCE_GROWTH_TILT_TO_ZERO"
        elif severity == "mild":
            growth_monthly = 25000
            decision = "REDUCE_GROWTH_TILT_TO_HALF"
        else:
            growth_monthly = 50000
            decision = "KEEP_BASELINE"
        actionable = True
        reason = "Mechanical annual threshold rule; no macro or price forecast is used."

    routing = _standard_nisa_routing(growth_monthly, p)
    base_growth = int(p["baseline_contribution"]["growth_tilt_jpy"])
    plan_changed = growth_monthly != base_growth

    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of_date": as_of_date.isoformat(),
        "status": "ok",
        "privacy": "private_ephemeral_output",
        "review": {
            "in_scheduled_window": in_window,
            "force_review": bool(force_review),
            "review_active": review_active,
            "market_forecast_used": False,
        },
        "decision": {
            "code": decision,
            "actionable_for_manual_setting_change": actionable,
            "plan_changed_from_baseline": plan_changed,
            "reason": reason,
            "trade_orders_created": False,
            "broker_settings_changed": False,
            "automatic_sales": False,
        },
        "recommended_monthly_plan": routing,
        "instruments": {
            "diversified_core": p["baseline_contribution"]["diversified_core_label"],
            "growth_tilt": p["baseline_contribution"]["growth_tilt_label"],
        },
        "risk_diagnostics": {
            "growth_tilt_market_value_weight": growth_weight,
            "growth_tilt_risk_contribution": growth_risk,
            "risk_contribution_by_bucket": risk_by_bucket,
            "portfolio_market_data_weight_coverage": market_data_coverage,
            "portfolio_metrics_status": metrics.get("status"),
            "annualized_volatility": metrics.get("annualized_volatility"),
            "max_drawdown": metrics.get("max_drawdown"),
            "growth_factor_score": growth_factor.get("value"),
            "growth_factor_score_weight_coverage": growth_factor.get("coverage"),
            "threshold_status": threshold_state,
        },
        "data_quality": {
            **prep_quality,
            "price_fetch_errors": fetch_errors,
            "minimum_market_data_weight_coverage": min_coverage,
        },
        "governance": {
            "monthly_contribution_continuity_is_primary": True,
            "change_frequency": "annual_review_only_unless_household_or_NISA_structure_changes",
            "rebalance_method": "cash_flow_first_no_forced_sales",
            "market_timing_prohibited": True,
            "wealth_target_is_not_a_required_return_constraint": True,
        },
    }


def write_contribution_rebalance_report(
    report: dict[str, Any], out_dir: str | Path
) -> tuple[Path, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "contribution_rebalance_latest.json"
    md_path = out / "contribution_rebalance_latest.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    plan = report["recommended_monthly_plan"]
    risk = report["risk_diagnostics"]
    decision = report["decision"]
    lines = [
        "# Annual Contribution Rebalance v1.0",
        "",
        f"Generated: {report.get('generated_at')}",
        f"Decision: **{decision.get('code')}**",
        f"Manual setting change actionable: {decision.get('actionable_for_manual_setting_change')}",
        f"Reason: {decision.get('reason')}",
        "",
        "## Recommended monthly plan",
        f"- Diversified core total: {plan.get('diversified_core_total_jpy')} JPY",
        f"- Growth tilt total: {plan.get('growth_tilt_total_jpy')} JPY",
        f"- NISA tsumitate / diversified core: {plan.get('nisa_tsumitate_diversified_core_jpy')} JPY",
        f"- NISA growth / diversified core: {plan.get('nisa_growth_diversified_core_jpy')} JPY",
        f"- NISA growth / growth tilt: {plan.get('nisa_growth_growth_tilt_jpy')} JPY",
        f"- NISA growth remaining for satellite (annual): {plan.get('annual_nisa_growth_remaining_for_satellite_jpy')} JPY",
        "",
        "## Risk diagnostics",
        f"- Growth-tilt market-value weight: {risk.get('growth_tilt_market_value_weight')}",
        f"- Growth-tilt risk contribution: {risk.get('growth_tilt_risk_contribution')}",
        f"- Market-data weight coverage: {risk.get('portfolio_market_data_weight_coverage')}",
        f"- Growth-factor score (diagnostic only): {risk.get('growth_factor_score')}",
        f"- Growth-factor score coverage: {risk.get('growth_factor_score_weight_coverage')}",
        f"- Threshold status: {risk.get('threshold_status')}",
        "",
        "## Governance",
        "- The engine never places trades or changes brokerage settings.",
        "- Market forecasts are not used to change monthly contributions.",
        "- Existing assets are not sold merely to rebalance; new cash flow is the first adjustment tool.",
        "- Current-year NISA remaining capacity must be checked before manually applying a recommendation.",
        "- Private output must never be committed or uploaded as a public Actions artifact.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
