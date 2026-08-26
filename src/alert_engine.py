from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any

import pandas as pd

VERSION = "1.9.0"
SEVERITY_ORDER = {"INFO": 0, "WATCH": 1, "WARNING": 2, "CRITICAL": 3}


@dataclass(frozen=True)
class Alert:
    severity: str
    category: str
    code: str
    title: str
    message: str
    value: Any = None
    threshold: Any = None
    entity: str | None = None
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _float(v: Any) -> float | None:
    try:
        if v is None or pd.isna(v):
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def _severity_max(alerts: list[Alert]) -> str:
    if not alerts:
        return "INFO"
    return max((a.severity for a in alerts), key=lambda s: SEVERITY_ORDER.get(s, -1))


def _add(alerts: list[Alert], severity: str, category: str, code: str, title: str,
         message: str, value: Any = None, threshold: Any = None,
         entity: str | None = None, source: str | None = None) -> None:
    alerts.append(Alert(severity, category, code, title, message, value, threshold, entity, source))


def detect_public_alerts(
    regime: dict[str, Any] | None,
    quality: dict[str, Any] | None,
    snapshot: pd.DataFrame | None,
    events: pd.DataFrame | None,
    previous_state: dict[str, Any] | None = None,
    *,
    rank_jump_threshold: float = 15.0,
    vix_watch: float = 20.0,
    vix_warning: float = 30.0,
    vix_critical: float = 35.0,
) -> dict[str, Any]:
    """Create deterministic public-safe exception alerts.

    These alerts describe changes/exceptions in already-public market/company data.
    They are not trade signals and never use private portfolio holdings.
    """
    regime = regime or {}
    quality = quality or {}
    previous_state = previous_state or {}
    snapshot = snapshot if snapshot is not None else pd.DataFrame()
    events = events if events is not None else pd.DataFrame()
    alerts: list[Alert] = []

    label = str(regime.get("regime_label") or "UNKNOWN")
    previous_label = str(previous_state.get("regime_label") or "")
    if previous_label and label != "UNKNOWN" and label != previous_label:
        _add(alerts, "WARNING" if label in {"RISK_OFF", "PANIC"} else "WATCH",
             "REGIME", "REGIME_CHANGE", "Market regime changed",
             f"Market regime changed from {previous_label} to {label}.",
             value=label, threshold=previous_label, source="market_regime_latest.json")

    evidence = regime.get("evidence") or {}
    vix = _float(evidence.get("vix"))
    treasury_vol_percentile = _float(evidence.get("treasury_volatility_percentile_rank"))
    previous_vix = _float(previous_state.get("vix"))
    if vix is not None:
        if vix >= vix_critical:
            _add(alerts, "CRITICAL", "VOLATILITY", "VIX_CRITICAL", "VIX at critical level",
                 "VIX exceeded the critical threshold.", vix, vix_critical, source="market_regime_latest.json")
        elif vix >= vix_warning:
            _add(alerts, "WARNING", "VOLATILITY", "VIX_WARNING", "VIX elevated",
                 "VIX exceeded the warning threshold.", vix, vix_warning, source="market_regime_latest.json")
        elif vix >= vix_watch:
            _add(alerts, "WATCH", "VOLATILITY", "VIX_WATCH", "VIX requires monitoring",
                 "VIX exceeded the watch threshold.", vix, vix_watch, source="market_regime_latest.json")
        if previous_vix is not None and previous_vix > 0:
            jump = vix / previous_vix - 1.0
            if jump >= 0.50:
                _add(alerts, "WARNING", "VOLATILITY", "VIX_JUMP", "VIX jumped sharply",
                     "VIX rose at least 50% from the previous stored observation.", jump, 0.50,
                     source="alert_state_latest.json")
            elif jump >= 0.25:
                _add(alerts, "WATCH", "VOLATILITY", "VIX_JUMP", "VIX rose quickly",
                     "VIX rose at least 25% from the previous stored observation.", jump, 0.25,
                     source="alert_state_latest.json")

    if treasury_vol_percentile is not None and treasury_vol_percentile >= 0.90:
        _add(alerts, "WARNING", "VOLATILITY", "TREASURY_VOLATILITY_SHOCK",
             "Treasury yield volatility is unusually high",
             "The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.",
             treasury_vol_percentile, 0.90, source="market_regime_latest.json")

    if bool(regime.get("stress_flag")):
        _add(alerts, "WARNING", "REGIME", "STRESS_FLAG", "Market stress flag active",
             "Market Regime Engine reports stress_flag=true.", True, True, source="market_regime_latest.json")
    if bool(regime.get("overheated_flag")):
        _add(alerts, "WATCH", "REGIME", "OVERHEATED_FLAG", "Overheated market flag active",
             "Market Regime Engine reports overheated_flag=true.", True, True, source="market_regime_latest.json")
    if bool(regime.get("thin_liquidity_flag")):
        _add(alerts, "WARNING", "LIQUIDITY", "THIN_LIQUIDITY", "Thin liquidity flag active",
             "Market Regime Engine reports thin_liquidity_flag=true.", True, True, source="market_regime_latest.json")

    components = regime.get("components") or {}
    liquidity = _float(components.get("liquidity"))
    participation = _float(components.get("participation"))
    if liquidity is not None and liquidity < 25:
        _add(alerts, "WARNING", "LIQUIDITY", "LIQUIDITY_WEAK", "Market liquidity is weak",
             "Liquidity component fell below 25/100.", liquidity, 25, source="market_regime_latest.json")
    elif liquidity is not None and liquidity < 40:
        _add(alerts, "WATCH", "LIQUIDITY", "LIQUIDITY_SOFT", "Market liquidity is soft",
             "Liquidity component fell below 40/100.", liquidity, 40, source="market_regime_latest.json")
    if participation is not None and participation < 30:
        _add(alerts, "WARNING", "BREADTH", "PARTICIPATION_WEAK", "Market participation is weak",
             "Participation/breadth component fell below 30/100.", participation, 30,
             source="market_regime_latest.json")

    actionable = quality.get("actionable")
    quality_score = _float(quality.get("quality_score"))
    primary_health = _float(quality.get("primary_source_health"))
    if actionable is False:
        sev = "CRITICAL" if quality_score is not None and quality_score < 0.25 else "WARNING"
        _add(alerts, sev, "DATA_QUALITY", "NOT_ACTIONABLE", "Data quality blocks investment conclusions",
             "Data quality is not actionable; missing data must not be converted into buy/sell conclusions.",
             quality_score, 0.25 if sev == "CRITICAL" else None, source="data_quality_latest.json")
    if primary_health is not None and primary_health < 0.5:
        _add(alerts, "WARNING", "DATA_QUALITY", "PRIMARY_SOURCE_HEALTH", "Primary-source health is low",
             "Primary-source health fell below 0.5.", primary_health, 0.5, source="data_quality_latest.json")

    if not snapshot.empty and "rank_change" in snapshot.columns:
        rank_change = pd.to_numeric(snapshot["rank_change"], errors="coerce")
        jump_rows = snapshot[rank_change >= rank_jump_threshold].copy()
        jump_rows["_rank_change_num"] = rank_change[rank_change >= rank_jump_threshold]
        for _, row in jump_rows.sort_values("_rank_change_num", ascending=False).head(20).iterrows():
            entity = str(row.get("name") or row.get("ticker") or row.get("code") or "unknown")
            change = _float(row.get("_rank_change_num"))
            _add(alerts, "WATCH", "SCREENING", "RANK_JUMP", "Screening rank jumped",
                 f"{entity} improved by at least {rank_jump_threshold:g} ranks.", change,
                 rank_jump_threshold, entity=entity, source="company_snapshot_latest.csv")

    if not events.empty:
        for _, row in events.head(50).iterrows():
            entity = str(row.get("name") or row.get("ticker") or row.get("code") or "unknown")
            priority = str(row.get("priority") or "normal").lower()
            event_type = str(row.get("event_type") or "company_event")
            title = str(row.get("title") or event_type)
            sev = "WARNING" if priority in {"high", "critical"} else "WATCH"
            _add(alerts, sev, "COMPANY_EVENT", f"EVENT_{event_type.upper()[:40]}", title,
                 f"New company event detected for {entity}.", entity=entity,
                 source=str(row.get("source") or "company_events_new.csv"))

    alerts.sort(key=lambda a: (-SEVERITY_ORDER.get(a.severity, -1), a.category, a.code, a.entity or ""))
    counts = {s: sum(a.severity == s for a in alerts) for s in SEVERITY_ORDER}
    state = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "regime_label": label,
        "vix": vix,
        "regime_score": _float(regime.get("regime_score")),
        "quality_score": quality_score,
        "primary_source_health": primary_health,
    }
    return {
        "version": VERSION,
        "generated_at": state["generated_at"],
        "highest_severity": _severity_max(alerts),
        "counts": counts,
        "alerts": [a.to_dict() for a in alerts],
        "state": state,
        "rules": [
            "Alerts are deterministic exception flags, not buy/sell signals.",
            "Missing values are never inferred.",
            "Only public-safe market/company data may be persisted by this module.",
        ],
    }


def detect_private_portfolio_alerts(
    report: dict[str, Any],
    previous: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create private portfolio-risk alerts for ephemeral/private use only."""
    previous = previous or {}
    alerts: list[Alert] = []
    p = report.get("portfolio") or {}
    metrics = p.get("metrics") or {}
    concentration = p.get("concentration") or {}
    var = _float(metrics.get("var_1d"))
    vol = _float(metrics.get("annualized_volatility"))
    beta = _float(metrics.get("beta"))
    largest = _float(concentration.get("largest_weight"))
    top5 = _float(concentration.get("top5_weight"))
    hhi = _float(concentration.get("hhi"))
    input_audit = report.get("private_input_audit") or {}
    risk_coverage = _float(metrics.get("portfolio_weight_coverage"))

    if input_audit.get("status") == "invalid_or_stale":
        _add(alerts, "WARNING", "DATA_QUALITY", "PRIVATE_INPUT_INVALID_OR_STALE",
             "Private portfolio inputs are invalid or stale",
             "Optional FX, scenario, and investor-capacity outputs were withheld; refresh or reconcile private inputs.")
    if risk_coverage is not None and risk_coverage < 0.90:
        _add(alerts, "WARNING", "DATA_QUALITY", "PORTFOLIO_RISK_COVERAGE_LOW",
             "Historical portfolio-risk coverage is incomplete",
             "Price history covers less than 90% of portfolio weight; beta, VaR, and volatility are partial estimates.",
             risk_coverage, 0.90)

    if var is not None and var >= 0.035:
        _add(alerts, "CRITICAL", "PORTFOLIO_RISK", "VAR_CRITICAL", "Portfolio VaR is high",
             "1-day historical VaR exceeded 3.5%.", var, 0.035)
    elif var is not None and var >= 0.025:
        _add(alerts, "WARNING", "PORTFOLIO_RISK", "VAR_HIGH", "Portfolio VaR is elevated",
             "1-day historical VaR exceeded 2.5%.", var, 0.025)
    prev_var = _float(previous.get("var_1d"))
    if var is not None and prev_var is not None and prev_var > 0 and var / prev_var - 1 >= 0.25:
        _add(alerts, "WARNING", "PORTFOLIO_RISK", "VAR_JUMP", "Portfolio VaR increased sharply",
             "1-day historical VaR rose at least 25% versus the previous private observation.",
             var / prev_var - 1, 0.25)
    if largest is not None and largest >= 0.10:
        _add(alerts, "WARNING", "CONCENTRATION", "SINGLE_NAME_CONCENTRATION", "Single-name concentration is high",
             "Largest portfolio weight is at least 10%.", largest, 0.10)
    if top5 is not None and top5 >= 0.50:
        _add(alerts, "WARNING", "CONCENTRATION", "TOP5_CONCENTRATION", "Top-5 concentration is high",
             "Top five holdings represent at least 50% of the analyzed portfolio.", top5, 0.50)
    if beta is not None and abs(beta) >= 1.30:
        _add(alerts, "WATCH", "PORTFOLIO_RISK", "BETA_EXTREME", "Portfolio beta is elevated",
             "Absolute portfolio beta is at least 1.30.", beta, 1.30)

    alerts.sort(key=lambda a: -SEVERITY_ORDER.get(a.severity, -1))
    state = {"var_1d": var, "annualized_volatility": vol, "beta": beta,
             "largest_weight": largest, "top5_weight": top5, "hhi": hhi}
    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "privacy": "PRIVATE_EPHEMERAL_ONLY",
        "highest_severity": _severity_max(alerts),
        "counts": {s: sum(a.severity == s for a in alerts) for s in SEVERITY_ORDER},
        "alerts": [a.to_dict() for a in alerts],
        "state": state,
        "rule": "Private portfolio alerts must never be committed to the public repository.",
    }
