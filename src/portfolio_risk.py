from __future__ import annotations

import json
import io
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

VERSION = "1.9.1"
DEFAULT_BENCHMARK = "1306.T"


@dataclass(frozen=True)
class RiskConfig:
    lookback_days: int = 400
    min_observations: int = 120
    var_confidence: float = 0.95
    candidate_weight: float = 0.02
    candidate_top_n: int = 10
    benchmark: str = DEFAULT_BENCHMARK


def _num(s: pd.Series | Any) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def _json_default(v: Any) -> Any:
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating,)): return None if np.isnan(v) else float(v)
    if isinstance(v, pd.Timestamp): return v.isoformat()
    if pd.isna(v): return None
    return str(v)


def yahoo_symbol(row: pd.Series | dict[str, Any]) -> str | None:
    def clean(value: Any) -> str:
        return "" if value is None or pd.isna(value) else str(value).strip()
    ticker = clean(row.get("ticker"))
    code = clean(row.get("code"))
    market = str(row.get("market") or "").upper()
    if ticker:
        return ticker
    if code.isdigit() and len(code) == 4 and market in {"", "JP", "JAPAN", "TSE", "TOKYO"}:
        return f"{code}.T"
    return code or None


def normalize_portfolio(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        raise ValueError("portfolio is empty")
    out = df.copy()
    if not any(c in out.columns for c in ("ticker", "code", "holding_id", "name")):
        raise ValueError("portfolio requires ticker, code, holding_id, or name")
    if "weight" not in out.columns:
        if "market_value" not in out.columns:
            raise ValueError("portfolio requires weight or market_value")
        mv = _num(out["market_value"]).fillna(0.0)
        total = float(mv.sum())
        if total <= 0:
            raise ValueError("market_value sum must be positive")
        out["weight"] = mv / total
    out["weight"] = _num(out["weight"]).fillna(0.0)
    out = out[out["weight"] > 0].copy()
    total = float(out["weight"].sum())
    if total <= 0:
        raise ValueError("weight sum must be positive")
    out["weight"] = out["weight"] / total
    out["symbol"] = out.apply(yahoo_symbol, axis=1)
    if out.empty:
        raise ValueError("no positive-weight holdings")
    return out.reset_index(drop=True)


def _parse_timestamp(value: Any) -> datetime | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        dt = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def validate_private_profile(
    profile: dict[str, Any] | None,
    portfolio_invested_jpy: float,
    portfolio_source_as_of: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Classify private inputs without treating staleness as a total stop.

    Structural/numeric failures may withhold only the affected component.  Old,
    undated, or unreconciled-but-usable inputs remain available for explicitly
    labelled reference calculations and are never promoted to trade-actionable
    output.
    """
    if profile is not None and not isinstance(profile, dict):
        return {
            "status": "withheld", "analysis_mode": "withheld",
            "actionable": False, "calculation_allowed": False,
            "fx_calculation_allowed": False, "scenario_calculation_allowed": False,
            "capacity_calculation_allowed": False,
            "errors": ["profile_must_be_json_object"], "warnings": [],
        }
    if not profile or profile.get("enabled") is False:
        return {
            "status": "disabled", "analysis_mode": "withheld",
            "actionable": False, "calculation_allowed": False,
            "fx_calculation_allowed": False, "scenario_calculation_allowed": False,
            "capacity_calculation_allowed": False, "errors": [], "warnings": [],
        }
    now_utc = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    errors: list[str] = []
    warnings: list[str] = []
    age_days: dict[str, float | None] = {}
    max_age_days = _finite_float(profile.get("max_age_days", 7))
    fx_max_age_days = _finite_float(profile.get("fx_max_age_days", 2))
    if max_age_days is None or max_age_days < 0:
        warnings.append("max_age_days_invalid_using_default")
        max_age_days = 7.0
    if fx_max_age_days is None or fx_max_age_days < 0:
        warnings.append("fx_max_age_days_invalid_using_default")
        fx_max_age_days = 2.0
    profile_as_of = _parse_timestamp(profile.get("as_of_jst"))
    fx_as_of = _parse_timestamp(profile.get("base_usdjpy_as_of_jst"))
    source_as_of = _parse_timestamp(portfolio_source_as_of or profile.get("portfolio_source_as_of_jst"))
    for label, dt, limit in (("profile", profile_as_of, max_age_days),
                             ("portfolio_source", source_as_of, max_age_days),
                             ("base_usdjpy", fx_as_of, fx_max_age_days)):
        if dt is None:
            age_days[label] = None
            warnings.append(f"{label}_as_of_missing_or_invalid")
            continue
        age = (now_utc - dt).total_seconds() / 86400
        age_days[label] = age
        if age > limit:
            warnings.append(f"{label}_stale")
        elif dt > now_utc + timedelta(hours=1):
            warnings.append(f"{label}_timestamp_in_future")
    total_assets = _finite_float(profile.get("total_assets_jpy"))
    invested = _finite_float(profile.get("invested_assets_jpy"))
    if total_assets is None or total_assets <= 0:
        errors.append("total_assets_missing_or_nonpositive")
    if invested is None or invested <= 0:
        warnings.append("invested_assets_missing_or_nonpositive")
    else:
        tolerance_jpy = _finite_float(profile.get("reconciliation_tolerance_jpy", 1000))
        tolerance_ratio = _finite_float(profile.get("reconciliation_tolerance_ratio", 0.005))
        if tolerance_jpy is None or tolerance_jpy < 0 or tolerance_ratio is None or tolerance_ratio < 0:
            warnings.append("reconciliation_tolerance_invalid_using_default")
            tolerance_jpy, tolerance_ratio = 1000.0, 0.005
        tolerance = max(tolerance_jpy, abs(invested) * tolerance_ratio)
        difference = portfolio_invested_jpy - invested
        if abs(difference) > tolerance:
            warnings.append("portfolio_market_value_reconciliation_failed")
    base_fx = _finite_float(profile.get("base_usdjpy"))
    if base_fx is None or base_fx <= 0:
        errors.append("base_usdjpy_missing_or_nonpositive")
    effective_total_assets = total_assets if total_assets is not None and total_assets > 0 else portfolio_invested_jpy
    if total_assets is not None and invested is not None and total_assets < invested:
        warnings.append("total_assets_below_invested_assets")
    if effective_total_assets < portfolio_invested_jpy:
        effective_total_assets = portfolio_invested_jpy
        warnings.append("total_assets_adjusted_to_portfolio_market_value")
    total_assets_basis = str(profile.get("total_assets_basis") or "declared_total_assets")
    if total_assets_basis == "invested_assets_proxy":
        warnings.append("total_assets_uses_invested_assets_proxy")
    targets = profile.get("target_usdjpy", [156, 155, 153, 150])
    targets_valid = isinstance(targets, list) and bool(targets) and not any(
        _finite_float(x) is None or float(x) <= 0 for x in targets
    )
    if not targets_valid:
        errors.append("target_usdjpy_invalid")
    scenarios = profile.get("cause_scenarios", [])
    global_minimum = _finite_float(profile.get("minimum_scenario_coverage", .90))
    if global_minimum is None or not 0 <= global_minimum <= 1:
        errors.append("minimum_scenario_coverage_invalid")
    scenarios_valid = isinstance(scenarios, list)
    if not scenarios_valid:
        errors.append("cause_scenarios_invalid")
    else:
        for scenario in scenarios:
            if not isinstance(scenario, dict) or not str(scenario.get("id", "")).strip():
                errors.append("cause_scenario_id_missing")
                scenarios_valid = False
                continue
            target = scenario.get("target_usdjpy")
            if target is not None and (_finite_float(target) is None or float(target) <= 0):
                errors.append(f"cause_scenario_{scenario.get('id')}_target_invalid")
                scenarios_valid = False
            minimum = _finite_float(scenario.get("min_coverage", global_minimum))
            if minimum is None or not 0 <= minimum <= 1:
                errors.append(f"cause_scenario_{scenario.get('id')}_coverage_invalid")
                scenarios_valid = False
    resilience = profile.get("resilience") or {}
    if not isinstance(resilience, dict):
        errors.append("resilience_must_be_object")
        resilience = {}
    capacity_valid = bool(resilience.get("enabled"))
    if capacity_valid:
        for key in ("unrealized_gain_jpy", "free_cash_jpy", "defensive_cash_jpy", "shock_loss_jpy"):
            value = _finite_float(resilience.get(key))
            if value is None or value < 0:
                errors.append(f"resilience_{key}_missing_or_invalid")
                capacity_valid = False
        if (_finite_float(resilience.get("unrealized_gain_jpy")) or 0) <= 0:
            errors.append("resilience_unrealized_gain_nonpositive")
            capacity_valid = False
    fx_allowed = base_fx is not None and base_fx > 0 and effective_total_assets > 0 and targets_valid
    scenario_allowed = fx_allowed and scenarios_valid
    capacity_allowed = capacity_valid and effective_total_assets > 0
    calculation_allowed = fx_allowed or scenario_allowed or capacity_allowed
    def relevant(items: list[str], prefixes: tuple[str, ...]) -> list[str]:
        return [item for item in items if item.startswith(prefixes)]
    fx_prefixes = (
        "profile_", "portfolio_source_", "base_usdjpy_", "total_assets_",
        "invested_assets_", "portfolio_market_value_", "reconciliation_",
        "target_usdjpy_", "max_age_days_", "fx_max_age_days_",
    )
    scenario_prefixes = fx_prefixes + ("cause_", "minimum_scenario_",)
    capacity_prefixes = (
        "profile_", "total_assets_", "invested_assets_", "portfolio_market_value_",
        "reconciliation_", "resilience_", "max_age_days_",
    )
    component_errors = {
        "fx": relevant(errors, fx_prefixes),
        "scenario": relevant(errors, scenario_prefixes),
        "capacity": relevant(errors, capacity_prefixes),
    }
    component_warnings = {
        "fx": relevant(warnings, fx_prefixes),
        "scenario": relevant(warnings, scenario_prefixes),
        "capacity": relevant(warnings, capacity_prefixes),
    }
    fx_actionable = fx_allowed and not component_errors["fx"] and not component_warnings["fx"]
    scenario_actionable = scenario_allowed and not component_errors["scenario"] and not component_warnings["scenario"]
    capacity_actionable = capacity_allowed and not component_errors["capacity"] and not component_warnings["capacity"]
    requested_states = [fx_actionable]
    if isinstance(scenarios, list) and scenarios:
        requested_states.append(scenario_actionable)
    if resilience.get("enabled"):
        requested_states.append(capacity_actionable)
    actionable = calculation_allowed and all(requested_states)
    analysis_mode = "current" if actionable else "reference_only" if calculation_allowed else "withheld"
    return {
        "status": analysis_mode, "analysis_mode": analysis_mode,
        "actionable": actionable, "calculation_allowed": calculation_allowed,
        "fx_calculation_allowed": fx_allowed,
        "scenario_calculation_allowed": scenario_allowed,
        "capacity_calculation_allowed": capacity_allowed,
        "fx_actionable": fx_actionable,
        "scenario_actionable": scenario_actionable,
        "capacity_actionable": capacity_actionable,
        "component_errors": component_errors,
        "component_warnings": component_warnings,
        "errors": errors,
        "warnings": list(dict.fromkeys(warnings)),
        "age_days": age_days,
        "profile_as_of": profile.get("as_of_jst"),
        "portfolio_source_as_of": portfolio_source_as_of or profile.get("portfolio_source_as_of_jst"),
        "base_usdjpy_as_of": profile.get("base_usdjpy_as_of_jst"),
        "portfolio_invested_jpy": portfolio_invested_jpy,
        "declared_invested_jpy": invested,
        "reconciliation_difference_jpy": portfolio_invested_jpy - invested if invested else None,
        "declared_total_assets_jpy": total_assets,
        "effective_total_assets_jpy": effective_total_assets,
        "total_assets_basis": total_assets_basis,
    }


def enrich_private_profile(
    profile: dict[str, Any] | None,
    portfolio: pd.DataFrame,
    portfolio_source_as_of: str | None,
    market_dashboard_path: str | Path = "data/regime/market_dashboard_latest.csv",
) -> dict[str, Any] | None:
    """Fill safe reference inputs from the imported portfolio and public market data.

    An explicitly disabled profile stays disabled.  When no private profile is
    configured, the invested market value is a conservative denominator proxy
    and the latest public USD/JPY dashboard observation supplies the FX base.
    These derived inputs are labelled reference-only by validation.
    """
    if isinstance(profile, dict) and profile.get("enabled") is False:
        return profile
    p = dict(profile or {})
    derived: list[str] = list(p.get("derived_fields") or [])
    auto_profile = not bool(profile)
    p["schema_version"] = str(p.get("schema_version") or "1.2")
    p["enabled"] = True
    p["input_mode"] = str(p.get("input_mode") or ("auto_reference" if auto_profile else "private_profile"))

    invested = float(_num(portfolio.get("market_value", pd.Series(dtype=float))).fillna(0).sum())
    if (_finite_float(p.get("invested_assets_jpy")) or 0) <= 0 and invested > 0:
        p["invested_assets_jpy"] = invested
        derived.append("invested_assets_jpy")
    if (_finite_float(p.get("total_assets_jpy")) or 0) <= 0 and invested > 0:
        p["total_assets_jpy"] = invested
        p["total_assets_basis"] = "invested_assets_proxy"
        derived.append("total_assets_jpy")
    if portfolio_source_as_of:
        p["portfolio_source_as_of_jst"] = portfolio_source_as_of
        if not p.get("as_of_jst"):
            p["as_of_jst"] = portfolio_source_as_of
            derived.append("as_of_jst")
    p.setdefault("target_usdjpy", [156, 155, 153, 150])
    p.setdefault("cause_scenarios", [])
    p.setdefault("minimum_scenario_coverage", 0.90)
    p.setdefault("max_age_days", 7)
    p.setdefault("fx_max_age_days", 2)
    p.setdefault("resilience", {"enabled": False})

    dashboard = Path(market_dashboard_path)
    if dashboard.exists() and p.get("auto_refresh_base_usdjpy", True):
        try:
            market = pd.read_csv(dashboard)
            mask = pd.Series(False, index=market.index)
            if "ticker" in market:
                mask |= market["ticker"].astype(str).eq("JPY=X")
            if "series" in market:
                mask |= market["series"].astype(str).str.upper().eq("USDJPY")
            rows = market.loc[mask].copy()
            if "data_status" in rows:
                rows = rows[rows["data_status"].astype(str).str.lower().eq("ok")]
            if not rows.empty:
                sort_col = "fetched_at" if "fetched_at" in rows else "date" if "date" in rows else None
                if sort_col:
                    rows = rows.sort_values(sort_col)
                row = rows.iloc[-1]
                close = _finite_float(row.get("close"))
                if close is not None and close > 0:
                    p["base_usdjpy"] = close
                    p["base_usdjpy_as_of_jst"] = row.get("fetched_at") or row.get("date")
                    p["base_usdjpy_source"] = str(row.get("source") or "market_dashboard")
                    derived.extend(["base_usdjpy", "base_usdjpy_as_of_jst"])
        except Exception:
            # Validation will label FX analysis unavailable; core portfolio
            # analysis must continue even when this optional fallback fails.
            pass
    p["derived_fields"] = list(dict.fromkeys(derived))
    return p


def fx_sensitivity_matrix(
    portfolio: pd.DataFrame,
    base_usdjpy: float,
    target_rates: tuple[float, ...] = (156.0, 155.0, 153.0, 150.0),
    total_assets: float | None = None,
) -> dict[str, Any]:
    """Direct USD/JPY translation sensitivity using only explicit numeric betas.

    Currency baskets and unknown exposures are excluded rather than silently
    receiving a beta of one. Values are static translation estimates, not P&L
    forecasts and not estimates of underlying asset-price changes.
    """
    if base_usdjpy <= 0:
        raise ValueError("base_usdjpy must be positive")
    p = portfolio.copy()
    if "market_value" not in p or "fx_beta_usdjpy" not in p:
        return {"status": "missing", "reason": "market_value_or_fx_beta_missing", "scenarios": []}
    mv = _num(p["market_value"])
    beta = _num(p["fx_beta_usdjpy"])
    eligible = mv.notna() & beta.notna() & (beta != 0)
    exposure = float((mv[eligible] * beta[eligible]).sum())
    gross = float(mv.fillna(0).sum())
    assets = float(total_assets) if total_assets is not None else gross
    if assets <= 0:
        return {"status": "invalid", "reason": "total_assets_nonpositive", "scenarios": []}
    currency = p.get("currency", pd.Series("UNKNOWN", index=p.index)).fillna("UNKNOWN").astype(str)
    exposure_type = p.get("fx_exposure_type", pd.Series("unknown", index=p.index)).fillna("unknown").astype(str)
    bucket_masks = {
        "direct_usd": currency.eq("USD") & beta.notna() & beta.ne(0),
        "jpy_or_domestic": currency.eq("JPY") | exposure_type.eq("domestic"),
        "hedged": currency.eq("HEDGED") | exposure_type.eq("hedged"),
        "currency_basket": currency.eq("EM_BASKET") | exposure_type.eq("currency_basket"),
        "unknown": currency.eq("UNKNOWN") | exposure_type.eq("unknown"),
    }
    buckets = {k: float(mv[mask].fillna(0).sum()) for k, mask in bucket_masks.items()}
    buckets["beta_missing"] = float(mv[beta.isna()].fillna(0).sum())
    buckets["explicit_zero_beta"] = float(mv[beta.eq(0)].fillna(0).sum())
    scenarios = []
    for target in target_rates:
        impact = exposure * (float(target) / base_usdjpy - 1.0)
        scenarios.append({"target_usdjpy": float(target), "direct_fx_impact_jpy": impact,
                          "impact_pct_total_assets": impact / assets if assets > 0 else None})
    return {
        "status": "ok", "method": "explicit_beta_static_translation", "base_usdjpy": base_usdjpy,
        "usdjpy_beta_equivalent_jpy": exposure, "direct_usd_market_value_jpy": buckets["direct_usd"],
        "direct_weight_total_assets": exposure / assets,
        "impact_per_one_yen_down_jpy": -exposure / base_usdjpy,
        "market_value_buckets_jpy": buckets,
        "explicit_beta_coverage_ratio": float(mv[beta.notna()].fillna(0).sum()) / gross if gross > 0 else 0.0,
        "scenarios": scenarios,
        "limitations": ["Underlying security returns are excluded.", "Currency baskets require look-through or an OOS-estimated beta."],
    }


def position_weighted_shock(portfolio: pd.DataFrame, symbol: str, return_shock: float,
                            total_assets: float | None = None) -> dict[str, Any]:
    """Apply a return shock to the actual position value, never to portfolio notionals."""
    p = portfolio.copy()
    if "market_value" not in p:
        return {"status": "missing", "reason": "market_value_missing"}
    symbols = p.apply(yahoo_symbol, axis=1)
    value = float(_num(p.loc[symbols == symbol, "market_value"]).fillna(0).sum())
    invested_total = float(_num(p["market_value"]).fillna(0).sum())
    denominator = float(total_assets) if total_assets is not None else invested_total
    return {"status": "ok" if value > 0 else "not_held", "symbol": symbol, "position_value_jpy": value,
            "portfolio_weight": value / denominator if denominator > 0 else None,
            "weight_basis": "total_assets" if total_assets is not None else "invested_assets",
            "return_shock": float(return_shock),
            "impact_jpy": value * float(return_shock)}


def investor_capacity_metrics(total_assets: float, unrealized_gain: float, free_cash: float,
                              defensive_cash: float, shock_loss: float) -> dict[str, Any]:
    """Report financial-capacity ratios without manufacturing a portfolio score."""
    vals = (total_assets, unrealized_gain, free_cash, defensive_cash, shock_loss)
    if any(v < 0 for v in vals) or total_assets <= 0 or unrealized_gain <= 0:
        raise ValueError("resilience inputs must be non-negative and denominators positive")
    loss_assets = shock_loss / total_assets
    loss_gains = shock_loss / unrealized_gain
    liquid = free_cash + defensive_cash
    return {"status": "ok", "score": None, "score_status": "not_scored_without_validated_rubric",
            "shock_loss_jpy": shock_loss,
            "shock_loss_pct_assets": loss_assets, "shock_loss_pct_unrealized_gain": loss_gains,
            "remaining_unrealized_gain_jpy": unrealized_gain - shock_loss,
            "liquid_resources_jpy": liquid, "liquidity_coverage_ratio": liquid / shock_loss if shock_loss > 0 else None,
            "free_cash_covers_shock": free_cash >= shock_loss,
            "liquid_resources_cover_shock": liquid >= shock_loss,
            "interpretation": "investor_financial_capacity_not_return_forecast"}


def resilience_score(total_assets: float, unrealized_gain: float, free_cash: float,
                     defensive_cash: float, shock_loss: float) -> dict[str, Any]:
    """Backward-compatible alias; intentionally returns no numeric score."""
    return investor_capacity_metrics(total_assets, unrealized_gain, free_cash, defensive_cash, shock_loss)


def cause_scenarios(portfolio: pd.DataFrame, base_usdjpy: float,
                    scenarios: list[dict[str, Any]], total_assets: float,
                    default_min_coverage: float = 0.90) -> list[dict[str, Any]]:
    """Cause-conditional stress tests with explicit, reviewable holding assumptions.

    A scenario return is read from `scenario_return_<id>` per holding. Missing
    assumptions stay missing; coverage is reported and no proxy is substituted.
    """
    p = portfolio.copy()
    mv = _num(p.get("market_value", pd.Series(index=p.index, dtype=float)))
    beta = _num(p.get("fx_beta_usdjpy", pd.Series(index=p.index, dtype=float)))
    out: list[dict[str, Any]] = []
    for scenario in scenarios:
        sid = str(scenario["id"])
        col = f"scenario_return_{sid}"
        basis_col = f"scenario_return_basis_{sid}"
        ret = _num(p[col]) if col in p else pd.Series(np.nan, index=p.index)
        basis = p[basis_col].fillna("").astype(str) if basis_col in p else pd.Series("", index=p.index)
        beta_nonzero = beta.notna() & beta.ne(0)
        valid_basis = ~beta_nonzero | basis.isin({"local_currency", "jpy_nav"})
        covered = mv.notna() & ret.notna() & valid_basis
        asset_impact = float((mv[covered] * ret[covered]).sum())
        target = scenario.get("target_usdjpy")
        fx_impact = 0.0
        if target is not None:
            local_fx = covered & beta_nonzero & basis.eq("local_currency")
            fx_impact = float((mv[local_fx] * beta[local_fx]).sum()) * (float(target) / base_usdjpy - 1.0)
        partial_impact = asset_impact + fx_impact
        coverage = float(mv[covered].sum()) / float(mv.fillna(0).sum()) if mv.fillna(0).sum() > 0 else 0.0
        min_coverage = float(scenario.get("min_coverage", default_min_coverage))
        coefficient_status = str(scenario.get("coefficient_status", "unvalidated"))
        actionable = coverage >= min_coverage and coefficient_status == "validated_oos"
        out.append({
            "id": sid, "label": scenario.get("label", sid), "target_usdjpy": target,
            "asset_return_impact_jpy": asset_impact, "direct_fx_impact_jpy": fx_impact,
            "partial_covered_impact_jpy": partial_impact,
            "estimated_total_impact_jpy": partial_impact if actionable else None,
            "impact_pct_total_assets": partial_impact / total_assets if actionable and total_assets > 0 else None,
            "assumption_coverage_market_value": float(mv[covered].sum()),
            "assumption_coverage_ratio": coverage, "minimum_coverage_required": min_coverage,
            "status": "actionable" if actionable else "non_actionable",
            "actionable": actionable, "coefficient_status": coefficient_status,
            "uncovered_market_value_jpy": float(mv[~covered].fillna(0).sum()),
            "missing_return_basis_market_value_jpy": float(mv[ret.notna() & ~valid_basis].fillna(0).sum()),
        })
    return out


def classify_treasury_operation(operation: str) -> dict[str, Any]:
    """Prevent Treasury buybacks from being conflated with central-bank QE."""
    if operation.strip().lower() in {"treasury_buyback", "us_treasury_buyback"}:
        return {"classification": "debt_management_liquidity_operation", "is_qe": False,
                "is_monetization": False, "notes": "Exchanges/cancels Treasury liabilities; does not itself create central-bank reserves."}
    return {"classification": "unclassified", "is_qe": None, "is_monetization": None}


def fetch_close(symbol: str, start: datetime, end: datetime) -> pd.Series:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "period1": int(start.timestamp()),
        "period2": int(end.timestamp()),
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    r = requests.get(url, params=params, timeout=20, headers={"User-Agent": f"investment-quant/{VERSION}"})
    r.raise_for_status()
    result = r.json().get("chart", {}).get("result") or []
    if not result:
        return pd.Series(dtype=float, name=symbol)
    x = result[0]
    ts = x.get("timestamp") or []
    ind = x.get("indicators", {})
    adj = (ind.get("adjclose") or [{}])[0].get("adjclose") or []
    raw = (ind.get("quote") or [{}])[0].get("close") or []
    values = adj if len(adj) == len(ts) else raw
    s = pd.Series(values, index=pd.to_datetime(ts, unit="s", utc=True), dtype=float, name=symbol)
    return s.dropna().sort_index()


def build_return_matrix(symbols: list[str], config: RiskConfig, fetcher=fetch_close) -> tuple[pd.DataFrame, dict[str, str]]:
    end = datetime.now(timezone.utc) + timedelta(days=1)
    start = end - timedelta(days=config.lookback_days)
    closes: dict[str, pd.Series] = {}
    errors: dict[str, str] = {}
    for symbol in dict.fromkeys(symbols):
        try:
            s = fetcher(symbol, start, end)
            if len(s) < 2:
                errors[symbol] = "insufficient_price_history"
                continue
            closes[symbol] = s
        except Exception as e:
            errors[symbol] = f"{type(e).__name__}:{str(e)[:120]}"
    if not closes:
        return pd.DataFrame(), errors
    px = pd.concat(closes.values(), axis=1, join="outer").sort_index()
    px = px.ffill(limit=3)
    returns = px.pct_change(fill_method=None)
    return returns, errors


def _aligned_weights(columns: pd.Index, portfolio: pd.DataFrame) -> pd.Series:
    w = portfolio.groupby("symbol")["weight"].sum().reindex(columns).fillna(0.0)
    s = float(w.sum())
    return w / s if s > 0 else w


def portfolio_return_series(returns: pd.DataFrame, weights: pd.Series, min_assets: int = 1) -> pd.Series:
    if returns.empty:
        return pd.Series(dtype=float)
    r = returns.copy()
    w = weights.reindex(r.columns).fillna(0.0)
    valid_weight = r.notna().mul(w, axis=1).sum(axis=1)
    weighted = r.fillna(0.0).mul(w, axis=1).sum(axis=1)
    count = r.notna().sum(axis=1)
    out = weighted / valid_weight.replace(0, np.nan)
    return out[count >= min_assets].dropna()


def max_drawdown(returns: pd.Series) -> float | None:
    if returns.empty: return None
    wealth = (1.0 + returns).cumprod()
    dd = wealth / wealth.cummax() - 1.0
    return float(dd.min())


def beta_to_benchmark(port: pd.Series, benchmark: pd.Series) -> float | None:
    x = pd.concat([port.rename("p"), benchmark.rename("b")], axis=1).dropna()
    if len(x) < 30:
        return None
    var = float(x["b"].var(ddof=1))
    if var <= 0: return None
    return float(x[["p", "b"]].cov().loc["p", "b"] / var)


def historical_var_cvar(returns: pd.Series, confidence: float = 0.95) -> tuple[float | None, float | None]:
    r = returns.dropna()
    if len(r) < 30:
        return None, None
    q = float(r.quantile(1.0 - confidence))
    tail = r[r <= q]
    cvar = float(tail.mean()) if len(tail) else q
    return max(0.0, -q), max(0.0, -cvar)


def covariance_risk_contribution(asset_returns: pd.DataFrame, weights: pd.Series) -> dict[str, float]:
    r = asset_returns.dropna(how="all")
    cols = [c for c in r.columns if r[c].notna().sum() >= 60 and weights.get(c, 0) > 0]
    if not cols:
        return {}
    x = r[cols].dropna()
    if len(x) < 60:
        return {}
    w = weights.reindex(cols).fillna(0.0).to_numpy(float)
    if w.sum() <= 0: return {}
    w = w / w.sum()
    cov = x.cov().to_numpy(float)
    port_var = float(w @ cov @ w)
    if port_var <= 0: return {}
    marginal = cov @ w
    contrib = w * marginal / port_var
    return {c: float(v) for c, v in zip(cols, contrib)}


def weighted_group_exposure(portfolio: pd.DataFrame, column: str) -> dict[str, float]:
    if column not in portfolio.columns:
        return {}
    x = portfolio[[column, "weight"]].copy()
    x[column] = x[column].fillna("UNKNOWN").astype(str)
    g = x.groupby(column, dropna=False)["weight"].sum().sort_values(ascending=False)
    return {str(k): float(v) for k, v in g.items()}


def weighted_numeric_exposure(portfolio: pd.DataFrame, column: str) -> dict[str, Any]:
    if column not in portfolio.columns:
        return {"value": None, "coverage": 0.0}
    x = _num(portfolio[column])
    valid = x.notna()
    coverage = float(portfolio.loc[valid, "weight"].sum())
    value = float((x[valid] * portfolio.loc[valid, "weight"]).sum() / coverage) if coverage > 0 else None
    return {"value": value, "coverage": coverage}


def factor_tilts(portfolio: pd.DataFrame, screen: pd.DataFrame) -> dict[str, dict[str, float | None]]:
    if screen.empty: return {}
    key_pf = "ticker" if "ticker" in portfolio.columns and "ticker" in screen.columns else "code"
    if key_pf not in portfolio.columns or key_pf not in screen.columns:
        return {}
    m = portfolio.merge(screen, on=key_pf, how="left", suffixes=("_pf", ""))
    factors = ["value_score", "quality_score", "growth_score", "momentum_score", "risk_score", "liquidity_score", "regime_adjusted_score"]
    out: dict[str, dict[str, float | None]] = {}
    for c in factors:
        if c not in m.columns: continue
        x = _num(m[c]); valid = x.notna(); cov = float(m.loc[valid, "weight"].sum())
        val = float((x[valid] * m.loc[valid, "weight"]).sum() / cov) if cov > 0 else None
        out[c] = {"value": val, "coverage": cov}
    return out


def concentration_stats(weights: pd.Series) -> dict[str, float | None]:
    w = weights[weights > 0].sort_values(ascending=False)
    hhi = float((w ** 2).sum()) if len(w) else 0.0
    return {
        "hhi": hhi,
        "effective_holdings": float(1.0 / hhi) if hhi > 0 else None,
        "largest_weight": float(w.iloc[0]) if len(w) else None,
        "top5_weight": float(w.head(5).sum()) if len(w) else None,
    }


def portfolio_metrics(portfolio: pd.DataFrame, returns: pd.DataFrame, benchmark_symbol: str, confidence: float) -> dict[str, Any]:
    asset_cols = [c for c in portfolio["symbol"].unique() if c in returns.columns]
    if not asset_cols:
        return {"status": "insufficient_market_data", "portfolio_weight_coverage": 0.0}
    coverage = float(portfolio.loc[portfolio["symbol"].isin(asset_cols), "weight"].sum())
    asset_ret = returns[asset_cols]
    weights = _aligned_weights(asset_ret.columns, portfolio)
    port = portfolio_return_series(asset_ret, weights)
    benchmark = returns[benchmark_symbol] if benchmark_symbol in returns.columns else pd.Series(dtype=float)
    var, cvar = historical_var_cvar(port, confidence)
    ann_vol = float(port.std(ddof=1) * math.sqrt(252)) if len(port) >= 30 else None
    ann_ret = float((1 + port.mean()) ** 252 - 1) if len(port) >= 30 else None
    corr = asset_ret.corr(min_periods=60)
    upper = corr.where(np.triu(np.ones(corr.shape), 1).astype(bool)).stack()
    avg_corr = float(upper.mean()) if len(upper) else None
    risk_contrib = covariance_risk_contribution(asset_ret, weights)
    return {
        "status": "ok" if len(port) >= 30 and coverage >= 0.90 else "partial",
        "portfolio_weight_coverage": coverage,
        "observations": int(len(port)),
        "annualized_return_estimate": ann_ret,
        "annualized_volatility": ann_vol,
        "beta": beta_to_benchmark(port, benchmark),
        "var_1d": var,
        "cvar_1d": cvar,
        "max_drawdown": max_drawdown(port),
        "average_pairwise_correlation": avg_corr,
        "risk_contribution": risk_contrib,
        "weight_coverage_market_data": float(weights.sum()),
    }


def candidate_impact(base_portfolio: pd.DataFrame, returns: pd.DataFrame, candidate_symbol: str,
                     candidate_weight: float, benchmark_symbol: str, confidence: float) -> dict[str, Any]:
    if candidate_symbol not in returns.columns:
        return {"status": "market_data_missing"}
    base_symbols = [s for s in base_portfolio["symbol"].unique() if s in returns.columns]
    cols = list(dict.fromkeys(base_symbols + [candidate_symbol]))
    r = returns[cols]
    base_w = _aligned_weights(pd.Index(base_symbols), base_portfolio)
    before = portfolio_return_series(r[base_symbols], base_w) if base_symbols else pd.Series(dtype=float)
    new_w = base_w * (1.0 - candidate_weight)
    new_w.loc[candidate_symbol] = new_w.get(candidate_symbol, 0.0) + candidate_weight
    new_w = new_w.reindex(cols).fillna(0.0)
    new_w = new_w / new_w.sum()
    after = portfolio_return_series(r[cols], new_w)
    bvar, _ = historical_var_cvar(before, confidence)
    avar, _ = historical_var_cvar(after, confidence)
    bvol = float(before.std(ddof=1) * math.sqrt(252)) if len(before) >= 30 else None
    avol = float(after.std(ddof=1) * math.sqrt(252)) if len(after) >= 30 else None
    cand = r[candidate_symbol]
    corr = float(pd.concat([before.rename("p"), cand.rename("c")], axis=1).corr().loc["p", "c"]) if len(before) >= 30 else None
    old_conc = concentration_stats(base_w)
    new_conc = concentration_stats(new_w)
    delta_vol = (avol - bvol) if avol is not None and bvol is not None else None
    delta_var = (avar - bvar) if avar is not None and bvar is not None else None
    improves = 0
    worsens = 0
    if delta_vol is not None:
        improves += delta_vol < -0.002
        worsens += delta_vol > 0.002
    if delta_var is not None:
        improves += delta_var < -0.0002
        worsens += delta_var > 0.0002
    if new_conc["hhi"] < old_conc["hhi"] - 0.002: improves += 1
    if new_conc["hhi"] > old_conc["hhi"] + 0.002: worsens += 1
    verdict = "IMPROVES" if improves > worsens else "WORSENS" if worsens > improves else "NEUTRAL"
    return {
        "status": "ok",
        "candidate_weight": candidate_weight,
        "correlation_to_portfolio": corr,
        "before_annualized_volatility": bvol,
        "after_annualized_volatility": avol,
        "delta_annualized_volatility": delta_vol,
        "before_var_1d": bvar,
        "after_var_1d": avar,
        "delta_var_1d": delta_var,
        "before_hhi": old_conc["hhi"],
        "after_hhi": new_conc["hhi"],
        "verdict": verdict,
    }


def analyze(portfolio: pd.DataFrame, screen: pd.DataFrame, config: RiskConfig = RiskConfig(), fetcher=fetch_close,
            private_profile: dict[str, Any] | None = None, portfolio_source_as_of: str | None = None,
            now: datetime | None = None) -> dict[str, Any]:
    pf = normalize_portfolio(portfolio)
    candidates = screen.copy() if not screen.empty else pd.DataFrame()
    if not candidates.empty:
        candidates["symbol"] = candidates.apply(yahoo_symbol, axis=1)
        sort_col = "regime_adjusted_score" if "regime_adjusted_score" in candidates.columns else "total_score" if "total_score" in candidates.columns else None
        if sort_col:
            candidates[sort_col] = _num(candidates[sort_col])
            candidates = candidates.sort_values(sort_col, ascending=False, na_position="last")
        held_symbols = set(pf.loc[pf["symbol"].notna(), "symbol"])
        candidates = candidates[~candidates["symbol"].isin(held_symbols) & candidates["symbol"].notna()].head(config.candidate_top_n)
    else:
        candidates = pd.DataFrame(columns=["symbol"])
    symbols = list(pf.loc[pf["symbol"].notna(), "symbol"].unique()) + ([config.benchmark] if config.benchmark else []) + list(candidates.get("symbol", []))
    returns, fetch_errors = build_return_matrix(symbols, config, fetcher=fetcher)
    metrics = portfolio_metrics(pf, returns, config.benchmark, config.var_confidence)
    if "holding_id" in pf:
        concentration_key = pf["holding_id"].fillna("").astype(str)
    else:
        concentration_key = pf.apply(lambda r: yahoo_symbol(r) or str(r.get("name") or r.name), axis=1)
    weights = pf.assign(_concentration_key=concentration_key).groupby("_concentration_key")["weight"].sum()
    metadata = {
        "sector": weighted_group_exposure(pf, "sector"),
        "region": weighted_group_exposure(pf, "region"),
        "currency": weighted_group_exposure(pf, "currency"),
        "market_cap_bucket": weighted_group_exposure(pf, "market_cap_bucket"),
        "style": weighted_group_exposure(pf, "style"),
        "fx_sensitivity": weighted_numeric_exposure(pf, "fx_sensitivity"),
        "rate_sensitivity": weighted_numeric_exposure(pf, "rate_sensitivity"),
    }
    impacts = []
    for _, row in candidates.iterrows():
        symbol = row.get("symbol")
        impact = candidate_impact(pf, returns, symbol, config.candidate_weight, config.benchmark, config.var_confidence)
        impacts.append({"ticker": row.get("ticker"), "code": row.get("code"), "name": row.get("name"), "symbol": symbol,
                        "score": row.get("regime_adjusted_score", row.get("total_score")), **impact})
    impacts.sort(key=lambda x: ({"IMPROVES": 0, "NEUTRAL": 1, "WORSENS": 2}.get(x.get("verdict"), 3), x.get("delta_annualized_volatility") if x.get("delta_annualized_volatility") is not None else 999))
    invested_total = float(_num(pf["market_value"]).fillna(0).sum()) if "market_value" in pf else 0.0
    profile_audit = validate_private_profile(private_profile, invested_total, portfolio_source_as_of, now=now)
    report = {
        "version": VERSION,
        "generated_at": (now or datetime.now(timezone.utc)).astimezone(timezone.utc).isoformat(timespec="seconds"),
        "privacy": "PRIVATE_OUTPUT_ONLY",
        "portfolio": {
            "holdings": int(len(pf)),
            "concentration": concentration_stats(weights),
            "metrics": metrics,
            "metadata_exposures": metadata,
            "factor_tilts": factor_tilts(pf, screen),
            "market_resilience": {
                "score": None,
                "score_status": "not_scored_without_validated_rubric",
                "historical_metrics_status": metrics.get("status"),
                "note": "Market-price resilience is separate from investor financial capacity.",
            },
            "analysis_mode": profile_audit.get("analysis_mode"),
        },
        "private_input_audit": profile_audit,
        "macro_semantic_guardrails": {
            "us_treasury_buyback": classify_treasury_operation("us_treasury_buyback"),
            "generic_buyback": classify_treasury_operation("buyback"),
        },
        "candidate_impact": impacts,
        "data_quality": {
            "price_series_requested": int(len(set(symbols))),
            "price_series_available": int(len(returns.columns)),
            "fetch_errors": fetch_errors,
            "minimum_observations": config.min_observations,
            "portfolio_market_value_with_price_symbol_jpy": float(_num(pf.loc[pf["symbol"].notna(), "market_value"]).fillna(0).sum()) if "market_value" in pf else None,
            "portfolio_market_value_without_price_symbol_jpy": float(_num(pf.loc[pf["symbol"].isna(), "market_value"]).fillna(0).sum()) if "market_value" in pf else None,
            "portfolio_price_symbol_coverage_ratio": float(pf.loc[pf["symbol"].notna(), "weight"].sum()),
        },
        "rules": [
            "Risk estimates are historical estimates, not forecasts.",
            "Missing sector/currency/rate/FX metadata is reported as missing and never inferred.",
            "Candidate verdict describes portfolio-level risk diversification only; it is not a buy/sell signal.",
            "No order is ever placed by this module.",
            "EM and other currency baskets are never assigned USD beta 1 without look-through or validated evidence.",
            "Treasury buybacks are debt-management operations and are not classified as QE or monetization.",
            "Stale inputs reduce decision actionability but do not suppress usable reference calculations.",
        ],
    }
    profile = private_profile if isinstance(private_profile, dict) else {}
    base_fx = profile.get("base_usdjpy")
    total_assets = profile_audit.get("effective_total_assets_jpy")
    analysis_mode = str(profile_audit.get("analysis_mode") or "withheld")
    if profile_audit.get("fx_calculation_allowed") and base_fx is not None:
        fx_mode = "current" if profile_audit.get("fx_actionable") else "reference_only"
        fx = fx_sensitivity_matrix(
            pf, float(base_fx), tuple(profile.get("target_usdjpy", [156, 155, 153, 150])), total_assets
        )
        fx.update({
            "analysis_mode": fx_mode,
            "decision_actionable": bool(profile_audit.get("fx_actionable")),
            "input_warnings": (profile_audit.get("component_warnings") or {}).get("fx", []),
            "total_assets_basis": profile_audit.get("total_assets_basis"),
        })
        report["portfolio"]["fx_sensitivity"] = fx
    elif profile and profile.get("enabled") is not False:
        report["portfolio"]["fx_sensitivity"] = {
            "status": "withheld", "analysis_mode": "withheld",
            "reason": "required_numeric_fx_inputs_unavailable",
            "audit_errors": profile_audit.get("errors", []),
        }
    if profile_audit.get("scenario_calculation_allowed") and base_fx is not None:
        scenarios = cause_scenarios(
            pf, float(base_fx), profile.get("cause_scenarios", []), float(total_assets),
            float(profile.get("minimum_scenario_coverage", 0.90)),
        )
        if not profile_audit.get("scenario_actionable"):
            for scenario in scenarios:
                scenario["model_status"] = scenario.get("status")
                scenario["status"] = "reference_only"
                scenario["actionable"] = False
                scenario["estimated_total_impact_jpy"] = None
                scenario["impact_pct_total_assets"] = None
                scenario["input_warnings"] = (profile_audit.get("component_warnings") or {}).get("scenario", [])
        report["portfolio"]["cause_scenarios"] = scenarios
    else:
        report["portfolio"]["cause_scenarios"] = []
    resilience = profile.get("resilience")
    if profile_audit.get("capacity_calculation_allowed") and resilience and resilience.get("enabled", True):
        capacity_mode = "current" if profile_audit.get("capacity_actionable") else "reference_only"
        capacity = investor_capacity_metrics(
            float(total_assets), float(resilience["unrealized_gain_jpy"]),
            float(resilience["free_cash_jpy"]), float(resilience["defensive_cash_jpy"]),
            float(resilience["shock_loss_jpy"]),
        )
        capacity.update({
            "analysis_mode": capacity_mode,
            "decision_actionable": bool(profile_audit.get("capacity_actionable")),
            "input_warnings": (profile_audit.get("component_warnings") or {}).get("capacity", []),
            "total_assets_basis": profile_audit.get("total_assets_basis"),
        })
        report["portfolio"]["investor_financial_capacity"] = capacity
    elif resilience and resilience.get("enabled"):
        report["portfolio"]["investor_financial_capacity"] = {
            "status": "withheld", "analysis_mode": "withheld",
            "reason": "capacity_inputs_unavailable",
            "audit_errors": profile_audit.get("errors", []),
        }
    return report


def write_private_report(report: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    d = Path(out_dir); d.mkdir(parents=True, exist_ok=True)
    json_path = d / "portfolio_risk_latest.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    lines = ["# Portfolio Risk Report v1.9.1", "", f"Generated: {report.get('generated_at')}", ""]
    p = report.get("portfolio", {}); m = p.get("metrics", {}); c = p.get("concentration", {})
    audit = report.get("private_input_audit", {})
    lines += ["## Private input audit", f"- Status: {audit.get('status')}",
              f"- Analysis mode: {audit.get('analysis_mode')}",
              f"- Reference calculations allowed: {audit.get('calculation_allowed')}",
              f"- Trade-decision actionable: {audit.get('actionable')}",
              f"- Profile as-of: {audit.get('profile_as_of')}",
              f"- Portfolio source as-of: {audit.get('portfolio_source_as_of')}",
              f"- FX as-of: {audit.get('base_usdjpy_as_of')}",
              f"- Input age (days): {audit.get('age_days')}",
              f"- Total-assets basis: {audit.get('total_assets_basis')}",
              f"- Reconciliation difference: {audit.get('reconciliation_difference_jpy')}",
              f"- Warnings: {', '.join(audit.get('warnings', [])) or 'none'}",
              f"- Errors: {', '.join(audit.get('errors', [])) or 'none'}", "",
              "## Core risk", f"- Holdings: {p.get('holdings')}", f"- Beta: {m.get('beta')}",
              f"- Annualized volatility: {m.get('annualized_volatility')}", f"- 1-day VaR: {m.get('var_1d')}",
              f"- 1-day CVaR: {m.get('cvar_1d')}", f"- Max drawdown: {m.get('max_drawdown')}",
              f"- HHI: {c.get('hhi')}", f"- Effective holdings: {c.get('effective_holdings')}",
              "- Portfolio resilience score: not scored (no validated rubric)"]
    fx = p.get("fx_sensitivity", {})
    lines += ["", "## Direct FX sensitivity", f"- Status: {fx.get('status', 'not configured')}"]
    if fx.get("status") == "ok":
        lines += [f"- Analysis mode: {fx.get('analysis_mode')}",
                  f"- Trade-decision actionable: {fx.get('decision_actionable')}",
                  f"- Base USD/JPY: {fx.get('base_usdjpy')}",
                  f"- USDJPY beta-equivalent: {fx.get('usdjpy_beta_equivalent_jpy')}",
                  f"- Direct USD market value: {fx.get('direct_usd_market_value_jpy')}",
                  f"- One-yen-down impact: {fx.get('impact_per_one_yen_down_jpy')}",
                  f"- Explicit-beta coverage: {fx.get('explicit_beta_coverage_ratio')}"]
        lines += ["", "| Target USD/JPY | Direct FX impact | % total assets |", "|---:|---:|---:|"]
        for x in fx.get("scenarios", []):
            lines.append(f"| {x.get('target_usdjpy')} | {x.get('direct_fx_impact_jpy')} | {x.get('impact_pct_total_assets')} |")
    lines += ["", "## Cause-conditional scenarios",
              "Missing assumptions are not treated as zero. Reference-only or low-coverage inputs retain covered impacts but withhold trade-actionable totals.",
              "", "| Scenario | Status | Coverage | Covered impact | Total impact |", "|---|---|---:|---:|---:|"]
    for x in p.get("cause_scenarios", []):
        lines.append(f"| {x.get('label')} | {x.get('status')} | {x.get('assumption_coverage_ratio')} | {x.get('partial_covered_impact_jpy')} | {x.get('estimated_total_impact_jpy')} |")
    cap = p.get("investor_financial_capacity", {})
    lines += ["", "## Investor financial capacity", f"- Status: {cap.get('status', 'not configured')}",
              "- Numeric score: not assigned; this is separate from portfolio market resilience."]
    if cap.get("status") == "ok":
        lines += [f"- Analysis mode: {cap.get('analysis_mode')}",
                  f"- Trade-decision actionable: {cap.get('decision_actionable')}",
                  f"- Shock loss / total assets: {cap.get('shock_loss_pct_assets')}",
                  f"- Shock loss / unrealized gain: {cap.get('shock_loss_pct_unrealized_gain')}",
                  f"- Liquidity coverage: {cap.get('liquidity_coverage_ratio')}",
                  f"- Remaining unrealized gain: {cap.get('remaining_unrealized_gain_jpy')}"]
    lines += ["", "## Candidate impact"]
    for x in report.get("candidate_impact", []):
        lines.append(f"- {x.get('name') or x.get('ticker') or x.get('code')}: {x.get('verdict')} | corr={x.get('correlation_to_portfolio')} | Δvol={x.get('delta_annualized_volatility')} | ΔVaR={x.get('delta_var_1d')}")
    lines += ["", "## Governance"] + [f"- {r}" for r in report.get("rules", [])]
    md_path = d / "portfolio_risk_latest.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    portfolio_path = Path(os.getenv("PORTFOLIO_PATH", ".private/portfolio_latest.csv"))
    screen_path = Path(os.getenv("SCREEN_PATH", "data/decision_system/factor_scores_latest.csv"))
    if not screen_path.exists(): screen_path = Path("data/screening_latest.csv")
    out_dir = Path(os.getenv("PRIVATE_OUTPUT_DIR", ".private/portfolio_risk"))
    if not portfolio_path.exists():
        raise FileNotFoundError(f"Private portfolio input not found: {portfolio_path}")
    portfolio = pd.read_csv(portfolio_path)
    overlay_path = Path(os.getenv("PORTFOLIO_RISK_OVERLAY", ".private/portfolio_risk_overlay.csv"))
    overlay_secret = os.getenv("PORTFOLIO_RISK_OVERLAY_CSV")
    if overlay_secret or overlay_path.exists():
        overlay = pd.read_csv(io.StringIO(overlay_secret)) if overlay_secret else pd.read_csv(overlay_path)
        if "holding_id" in portfolio.columns and "holding_id" in overlay.columns:
            keys = ["holding_id"]
        elif all(k in portfolio.columns and k in overlay.columns for k in ("name", "account")):
            keys = ["name", "account"]
        elif "ticker" in portfolio.columns and "ticker" in overlay.columns:
            keys = ["ticker"]
        elif "code" in portfolio.columns and "code" in overlay.columns:
            keys = ["code"]
        else:
            raise ValueError("private risk overlay requires holding_id, name+account, ticker, or code")
        if overlay[keys].isna().any(axis=None) or overlay[keys].astype(str).apply(lambda s: s.str.strip().eq("")).any(axis=None):
            raise ValueError("private risk overlay keys must be non-empty")
        if overlay.duplicated(keys).any():
            raise ValueError("private risk overlay keys must be unique")
        # Private reviewed values override importer defaults without entering the public repository.
        portfolio = portfolio.merge(overlay, on=keys, how="left", suffixes=("", "_override"))
        for col in overlay.columns:
            override = f"{col}_override"
            if override in portfolio:
                portfolio[col] = portfolio[override].combine_first(portfolio.get(col))
                portfolio = portfolio.drop(columns=[override])
    profile_path = Path(os.getenv("PORTFOLIO_RISK_PROFILE", ".private/portfolio_risk_profile.json"))
    profile_secret = os.getenv("PORTFOLIO_RISK_PROFILE_JSON")
    profile = json.loads(profile_secret) if profile_secret else (
        json.loads(profile_path.read_text(encoding="utf-8")) if profile_path.exists() else None
    )
    portfolio_source_as_of = os.getenv("PORTFOLIO_SOURCE_AS_OF")
    profile = enrich_private_profile(
        profile,
        portfolio,
        portfolio_source_as_of,
        os.getenv("MARKET_DASHBOARD_PATH", "data/regime/market_dashboard_latest.csv"),
    )
    screen = pd.read_csv(screen_path) if screen_path.exists() else pd.DataFrame()
    config = RiskConfig(
        lookback_days=int(os.getenv("RISK_LOOKBACK_DAYS", "400")),
        min_observations=int(os.getenv("RISK_MIN_OBSERVATIONS", "120")),
        var_confidence=float(os.getenv("RISK_VAR_CONFIDENCE", "0.95")),
        candidate_weight=float(os.getenv("RISK_CANDIDATE_WEIGHT", "0.02")),
        candidate_top_n=int(os.getenv("RISK_CANDIDATE_TOP_N", "10")),
        benchmark=os.getenv("RISK_BENCHMARK", DEFAULT_BENCHMARK),
    )
    report = analyze(portfolio, screen, config=config, private_profile=profile,
                     portfolio_source_as_of=portfolio_source_as_of)
    paths = write_private_report(report, out_dir)
    # Deliberately print only non-sensitive execution metadata.
    print(json.dumps({"version": VERSION, "status": "ok", "private_outputs_written": len(paths),
                      "holdings_count": report.get("portfolio", {}).get("holdings"),
                      "candidate_count": len(report.get("candidate_impact", []))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
