from __future__ import annotations
from pathlib import Path
import yaml

def _label(regime):
    if not isinstance(regime,dict): return "unknown"
    for k in ("regime","label","state","market_regime","regime_label"):
        v=regime.get(k)
        if isinstance(v,str) and v.strip(): return v.strip().lower()
    return "unknown"

def build_policy_guardrails(regime, quality):
    cfg=yaml.safe_load(Path("config/policy_v1_6.yml").read_text(encoding="utf-8"))
    label=_label(regime)
    flags=set(str(x).lower() for x in (regime.get("regime_flags",[]) if isinstance(regime,dict) else []))
    elevated=any(k in label for k in ("overheat","euphoria","risk_off","risk-off","stress","panic_wait","caution","defensive")) or bool(flags & {"overheated","stress","thin_liquidity"})
    cash=cfg["cash_target_overheated_or_waiting"] if elevated else cfg["cash_target_normal"]
    blocked=(not quality.get("actionable",False))
    return {
      "regime_label":label,
      "absolute_defense_cash_jpy":cfg["absolute_defense_cash_jpy"],
      "cash_target_range":cash,
      "max_single_stock_weight":cfg["max_single_stock_weight"],
      "lifestyle_bucket_max_weight":cfg["lifestyle_bucket_max_weight"],
      "exploration_bucket_max_weight":cfg["exploration_bucket_max_weight"],
      "new_capital_top_rank_only":cfg["new_capital_top_rank_only"],
      "decision_gate":"BLOCK_DATA_QUALITY" if blocked else "OPEN_FOR_ANALYSIS",
      "note":"Guardrail only. This file never places orders."
    }
