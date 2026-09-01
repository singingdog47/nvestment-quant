"""Investment-policy controls derived from the August 2026 validation cycle.

Policy values are guardrails, not trade instructions. Dynamic brokerage data must
replace state variables whenever available.
"""
from __future__ import annotations

DEFENSIVE_RESERVE_JPY = 500_000


def deployable_cash(cash_total: float, bank_cash: float, cash_reserved_for_orders: float,
                    defensive_reserve: float = DEFENSIVE_RESERVE_JPY) -> float:
    """Cash available for new risk after live order reservations and defense reserve."""
    return max(0.0, float(cash_total) + float(bank_cash) - float(cash_reserved_for_orders) - float(defensive_reserve))


def account_tax_friction(account_type: str, unrealized_gain_jpy: float | None = None,
                         estimated_tax_jpy: float | None = None,
                         nisa_opportunity_cost_jpy: float | None = None,
                         switching_cost_jpy: float | None = None) -> dict:
    """Expose tax friction without hard-coding NISA/Taxable holding counts."""
    return {
        "account_type": account_type,
        "unrealized_gain_jpy": unrealized_gain_jpy,
        "estimated_tax_jpy": estimated_tax_jpy,
        "nisa_opportunity_cost_jpy": nisa_opportunity_cost_jpy,
        "switching_cost_jpy": switching_cost_jpy,
        "rule": "NISA status is a friction input, never an automatic hold decision",
    }


def order_change_policy(*, after_close: bool, thesis_changed: bool, expected_return_improved: bool,
                        premise_broken: bool, change_kind: str) -> dict:
    """Anti-FOMO execution discipline for a part-time investor.

    Intraday cancellation is always allowed when the premise is broken. New orders
    or price increases require after-close review plus a thesis/expected-return
    improvement; price movement alone never qualifies.
    """
    kind = change_kind.strip().lower()
    if kind == "cancel" and premise_broken:
        return {"allowed": True, "reason": "risk_reduction_exception"}
    if kind in {"new", "raise_limit", "replace"}:
        allowed = bool(after_close and thesis_changed and expected_return_improved)
        return {"allowed": allowed, "reason": "fundamental_revaluation" if allowed else "anti_fomo_timelock"}
    return {"allowed": bool(after_close), "reason": "after_close_maintenance_required" if not after_close else "maintenance_window"}


MACRO_RISK_LAYERS = (
    "rates_and_monetary_policy",
    "equity_valuation_and_forward_earnings_yield_spread",
    "flows_and_calendar_seasonality",
    "commodities_fx_and_geopolitical_triggers",
)

ERP_LABEL_POLICY = {
    "preferred_metric": "forward_earnings_yield_spread",
    "formula": "1 / sp500_forward_pe - us10y_nominal_yield",
    "warning": "This simple spread is not a complete estimate of the true equity risk premium.",
    "same_as_of_date_required": True,
}
