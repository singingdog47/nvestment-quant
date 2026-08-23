from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

VERSION = "1.7.0"
ROOT = Path("data")
OUT = ROOT / "decision_system"
LOG_DIR = ROOT / "decision_log"
STATE = ROOT / "state"


def _ensure() -> None:
    for p in (OUT, LOG_DIR, STATE):
        p.mkdir(parents=True, exist_ok=True)


def _json(path: str | Path, default: Any = None) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def _hash_file(path: str | Path) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _first(obj: Any, keys: tuple[str, ...], default: Any = None) -> Any:
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and obj[k] not in (None, ""):
                return obj[k]
        for v in obj.values():
            found = _first(v, keys, None)
            if found not in (None, ""):
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _first(v, keys, None)
            if found not in (None, ""):
                return found
    return default


def current_regime() -> tuple[str, str]:
    r = _json(ROOT / "regime" / "market_regime_latest.json", {})
    regime = str(_first(r, ("regime", "state", "label", "market_regime"), "UNKNOWN"))
    risk = str(_first(r, ("risk_level", "risk", "stress_level"), "UNKNOWN"))
    return regime, risk


def regime_weights(regime: str) -> dict[str, float]:
    base = {"value_score": .20, "quality_score": .20, "growth_score": .15,
            "momentum_score": .20, "risk_score": .15, "liquidity_score": .10}
    r = regime.upper().replace("_", "-")
    if "PANIC" in r or "RISK-OFF" in r:
        base.update({"value_score": .20, "quality_score": .28, "growth_score": .08,
                     "momentum_score": .08, "risk_score": .26, "liquidity_score": .10})
    elif "RECOVERY" in r:
        base.update({"value_score": .17, "quality_score": .18, "growth_score": .20,
                     "momentum_score": .25, "risk_score": .10, "liquidity_score": .10})
    elif "OVERHEAT" in r:
        base.update({"value_score": .24, "quality_score": .24, "growth_score": .10,
                     "momentum_score": .12, "risk_score": .20, "liquidity_score": .10})
    elif "RISK-ON" in r:
        base.update({"value_score": .16, "quality_score": .18, "growth_score": .20,
                     "momentum_score": .26, "risk_score": .10, "liquidity_score": .10})
    total = sum(base.values())
    return {k: v / total for k, v in base.items()}


def build_factor_table(screen: pd.DataFrame, regime: str) -> pd.DataFrame:
    if screen.empty:
        return screen.copy()
    w = regime_weights(regime)
    df = screen.copy()
    for c in w:
        if c not in df:
            df[c] = np.nan
        df[c] = pd.to_numeric(df[c], errors="coerce")
    available_weight = sum(weight for c, weight in w.items() if df[c].notna().any())
    if available_weight <= 0:
        df["regime_adjusted_score"] = np.nan
    else:
        num = sum(df[c].fillna(0) * weight for c, weight in w.items())
        den = sum(df[c].notna().astype(float) * weight for c, weight in w.items())
        df["regime_adjusted_score"] = num / den.replace(0, np.nan)
    df["regime"] = regime
    df["factor_model_version"] = VERSION
    sort_col = "regime_adjusted_score"
    df = df.sort_values(sort_col, ascending=False, na_position="last")
    df["regime_rank"] = np.arange(1, len(df) + 1)
    return df


def _deterministic_reason(row: pd.Series) -> str:
    pairs = []
    labels = {"value_score": "Value", "quality_score": "Quality", "growth_score": "Growth",
              "momentum_score": "Momentum", "risk_score": "Risk", "liquidity_score": "Liquidity"}
    for c, label in labels.items():
        v = pd.to_numeric(pd.Series([row.get(c)]), errors="coerce").iloc[0]
        if pd.notna(v):
            pairs.append((float(v), label))
    pairs.sort(reverse=True)
    top = ", ".join(f"{label}={score:.1f}" for score, label in pairs[:3])
    return f"Top factors: {top}" if top else "Factor data unavailable"


def _recommended_action(regime: str, risk: str) -> str:
    text = f"{regime} {risk}".upper()
    if "PANIC" in text or "CRITICAL" in text:
        return "REDUCE_RISK"
    if "RISK-OFF" in text or "HIGH" in text:
        return "WAIT_OR_REDUCE"
    if "OVERHEAT" in text:
        return "TAKE_PROFIT_OR_WAIT"
    if "RECOVERY" in text or "RISK-ON" in text:
        return "SELECTIVE_BUY"
    return "WAIT"


def append_decision_log(factors: pd.DataFrame, regime: str, risk: str) -> dict[str, Any]:
    _ensure()
    now = datetime.now(timezone.utc).replace(microsecond=0)
    inputs = {
        "screening_latest_sha256": _hash_file(ROOT / "screening_latest.csv"),
        "market_regime_sha256": _hash_file(ROOT / "regime" / "market_regime_latest.json"),
        "decision_context_sha256": _hash_file(ROOT / "decision_context_latest.json"),
        "quality_report_sha256": _hash_file(ROOT / "quality_report.json"),
    }
    top = []
    for _, row in factors.head(10).iterrows():
        top.append({
            "ticker": row.get("ticker"), "code": row.get("code"), "name": row.get("name"),
            "market": row.get("market"), "price": row.get("price"),
            "total_score": row.get("total_score"), "regime_adjusted_score": row.get("regime_adjusted_score"),
            "value_score": row.get("value_score"), "quality_score": row.get("quality_score"),
            "growth_score": row.get("growth_score"), "momentum_score": row.get("momentum_score"),
            "risk_score": row.get("risk_score"), "liquidity_score": row.get("liquidity_score"),
            "reason": _deterministic_reason(row), "flags": row.get("flags"),
        })
    decision = {
        "decision_id": f"{now.strftime('%Y%m%dT%H%M%SZ')}-{(inputs['screening_latest_sha256'] or 'na')[:10]}",
        "timestamp_utc": now.isoformat(), "system_version": VERSION,
        "market_regime": regime, "market_risk_level": risk,
        "recommended_action": _recommended_action(regime, risk),
        "input_snapshot": inputs, "factor_weights": regime_weights(regime),
        "top_candidates": top,
        "human_action": os.getenv("HUMAN_ACTION", "NOT_RECORDED"),
        "human_action_note": os.getenv("HUMAN_ACTION_NOTE", ""),
    }
    path = LOG_DIR / "decisions.jsonl"
    existing_ids = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try: existing_ids.add(json.loads(line).get("decision_id"))
            except Exception: pass
    if decision["decision_id"] not in existing_ids:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(decision, ensure_ascii=False, default=_json_default) + "\n")
    (OUT / "decision_latest.json").write_text(json.dumps(decision, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    return decision


def _json_default(v: Any) -> Any:
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating,)): return None if np.isnan(v) else float(v)
    if pd.isna(v): return None
    return str(v)


def _yahoo_symbol(item: dict[str, Any]) -> str | None:
    ticker = str(item.get("ticker") or "").strip()
    code = str(item.get("code") or "").strip()
    market = str(item.get("market") or "").upper()
    if market in {"JP", "JAPAN", "TSE", "TOKYO"} or (code.isdigit() and len(code) == 4):
        return f"{code}.T" if code else None
    return ticker or code or None


def _yahoo_prices(symbol: str, start: datetime, end: datetime) -> pd.Series:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"period1": int(start.timestamp()), "period2": int(end.timestamp()), "interval": "1d", "events": "history"}
    r = requests.get(url, params=params, timeout=15, headers={"User-Agent": "investment-quant/1.7"})
    r.raise_for_status()
    result = r.json().get("chart", {}).get("result", [])
    if not result: return pd.Series(dtype=float)
    x = result[0]; ts = x.get("timestamp", []); q = x.get("indicators", {}).get("quote", [{}])[0].get("close", [])
    s = pd.Series(q, index=pd.to_datetime(ts, unit="s", utc=True), dtype=float).dropna()
    return s


def evaluate_outcomes() -> pd.DataFrame:
    _ensure()
    log = LOG_DIR / "decisions.jsonl"
    cols = ["decision_id", "timestamp_utc", "horizon", "ticker", "code", "entry_price", "exit_price", "return_pct", "max_up_pct", "max_down_pct", "status"]
    if not log.exists():
        df = pd.DataFrame(columns=cols); df.to_csv(OUT / "outcomes_latest.csv", index=False); return df
    old_path = OUT / "outcomes_latest.csv"
    old = pd.read_csv(old_path) if old_path.exists() else pd.DataFrame(columns=cols)
    keys = set(zip(old.get("decision_id", []), old.get("horizon", []), old.get("ticker", [])))
    rows = old.to_dict("records")
    now = datetime.now(timezone.utc)
    horizons = {"1W": 7, "1M": 30, "3M": 90}
    for line in log.read_text(encoding="utf-8").splitlines():
        try: d = json.loads(line)
        except Exception: continue
        t0 = datetime.fromisoformat(d["timestamp_utc"].replace("Z", "+00:00"))
        for item in d.get("top_candidates", []):
            symbol = _yahoo_symbol(item)
            if not symbol: continue
            for label, days in horizons.items():
                key = (d["decision_id"], label, item.get("ticker"))
                if key in keys or now < t0 + timedelta(days=days): continue
                entry = pd.to_numeric(pd.Series([item.get("price")]), errors="coerce").iloc[0]
                try:
                    s = _yahoo_prices(symbol, t0 - timedelta(days=2), t0 + timedelta(days=days + 5))
                    target = s[s.index >= pd.Timestamp(t0 + timedelta(days=days))]
                    window = s[s.index >= pd.Timestamp(t0)]
                    exit_price = float(target.iloc[0]) if len(target) else np.nan
                    if pd.isna(entry) or entry == 0 or pd.isna(exit_price): raise ValueError("price unavailable")
                    rows.append({"decision_id": d["decision_id"], "timestamp_utc": d["timestamp_utc"], "horizon": label,
                                 "ticker": item.get("ticker"), "code": item.get("code"), "entry_price": float(entry),
                                 "exit_price": exit_price, "return_pct": (exit_price / float(entry) - 1) * 100,
                                 "max_up_pct": (window.max() / float(entry) - 1) * 100 if len(window) else np.nan,
                                 "max_down_pct": (window.min() / float(entry) - 1) * 100 if len(window) else np.nan,
                                 "status": "ok"})
                except Exception as e:
                    rows.append({"decision_id": d["decision_id"], "timestamp_utc": d["timestamp_utc"], "horizon": label,
                                 "ticker": item.get("ticker"), "code": item.get("code"), "entry_price": entry,
                                 "exit_price": np.nan, "return_pct": np.nan, "max_up_pct": np.nan, "max_down_pct": np.nan,
                                 "status": f"unavailable:{type(e).__name__}"})
                keys.add(key)
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(old_path, index=False)
    return df


def portfolio_risk(screen: pd.DataFrame) -> dict[str, Any]:
    # Portfolio data is intentionally not inferred from this public repository.
    if os.getenv("ALLOW_REPO_PORTFOLIO", "0") != "1":
        return {"status": "private_data_required", "rule": "Set ALLOW_REPO_PORTFOLIO=1 only when a safe portfolio_latest.csv is supplied."}
    p = ROOT / "portfolio_latest.csv"
    if not p.exists(): return {"status": "missing", "required_file": str(p)}
    pf = pd.read_csv(p)
    key = "ticker" if "ticker" in pf.columns else "code"
    if key not in pf.columns: return {"status": "invalid", "error": "ticker or code required"}
    if "weight" not in pf.columns:
        if "market_value" not in pf.columns: return {"status": "invalid", "error": "weight or market_value required"}
        mv = pd.to_numeric(pf["market_value"], errors="coerce").fillna(0)
        pf["weight"] = mv / mv.sum() if mv.sum() else 0
    pf["weight"] = pd.to_numeric(pf["weight"], errors="coerce").fillna(0)
    s_key = "ticker" if key == "ticker" and "ticker" in screen.columns else "code"
    m = pf.merge(screen, left_on=key, right_on=s_key, how="left", suffixes=("_pf", ""))
    beta = pd.to_numeric(m.get("beta_1y"), errors="coerce") if "beta_1y" in m else pd.Series(np.nan, index=m.index)
    hhi = float((m["weight"] ** 2).sum())
    theme = m.groupby("theme", dropna=False)["weight"].sum().sort_values(ascending=False) if "theme" in m else pd.Series(dtype=float)
    factor_cols = [c for c in ["value_score", "quality_score", "growth_score", "momentum_score", "risk_score"] if c in m]
    tilts = {c: float((pd.to_numeric(m[c], errors="coerce").fillna(0) * m["weight"]).sum()) for c in factor_cols}
    return {"status": "ok", "holdings": int(len(m)), "weight_sum": float(m["weight"].sum()),
            "portfolio_beta": float((beta.fillna(0) * m["weight"]).sum()) if beta.notna().any() else None,
            "concentration_hhi": hhi, "effective_holdings": (1 / hhi) if hhi > 0 else None,
            "top_theme_weights": {str(k): float(v) for k, v in theme.head(10).items()}, "factor_tilts": tilts}


def build_alerts(decision: dict[str, Any], factors: pd.DataFrame, risk_report: dict[str, Any]) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []
    regime = str(decision.get("market_regime", "UNKNOWN")).upper()
    risk = str(decision.get("market_risk_level", "UNKNOWN")).upper()
    if "PANIC" in regime or "CRITICAL" in risk:
        alerts.append({"severity": "CRITICAL", "type": "market_regime", "message": f"{regime} / risk={risk}"})
    elif "RISK-OFF" in regime or "HIGH" in risk:
        alerts.append({"severity": "WARNING", "type": "market_regime", "message": f"{regime} / risk={risk}"})
    if "rank_change" in factors:
        rc = pd.to_numeric(factors["rank_change"], errors="coerce")
        jumps = factors[rc >= 20].head(10)
        for _, r in jumps.iterrows():
            alerts.append({"severity": "WATCH", "type": "rank_jump", "ticker": r.get("ticker"), "message": f"rank_change={r.get('rank_change')}"})
    if risk_report.get("status") == "ok" and risk_report.get("concentration_hhi", 0) > .15:
        alerts.append({"severity": "WARNING", "type": "portfolio_concentration", "message": f"HHI={risk_report['concentration_hhi']:.3f}"})
    if not alerts:
        alerts.append({"severity": "INFO", "type": "system", "message": "No configured exception threshold breached."})
    return alerts


def validation_report(outcomes: pd.DataFrame) -> str:
    lines = ["# Decision Validation Report v1.7", "", "This report evaluates only matured observations. Missing outcomes are not imputed.", ""]
    ok = outcomes[outcomes["status"] == "ok"] if len(outcomes) else outcomes
    if ok.empty:
        lines.append("- No matured validated outcomes yet.")
        return "\n".join(lines)
    for h, g in ok.groupby("horizon"):
        r = pd.to_numeric(g["return_pct"], errors="coerce").dropna()
        if len(r): lines.append(f"- {h}: n={len(r)}, mean={r.mean():.2f}%, median={r.median():.2f}%, win_rate={(r.gt(0).mean()*100):.1f}%")
    lines += ["", "## Governance", "- Validation results do not auto-change factor weights.", "- Weight changes require explicit human review and a versioned code/config change."]
    return "\n".join(lines)


def main() -> None:
    _ensure()
    screen_path = ROOT / "screening_latest.csv"
    if not screen_path.exists():
        raise FileNotFoundError("data/screening_latest.csv is required")
    screen = pd.read_csv(screen_path)
    regime, risk = current_regime()
    factors = build_factor_table(screen, regime)
    factors.to_csv(OUT / "factor_scores_latest.csv", index=False)
    decision = append_decision_log(factors, regime, risk)
    outcomes = evaluate_outcomes()
    pr = portfolio_risk(screen)
    (OUT / "portfolio_risk_latest.json").write_text(json.dumps(pr, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    alerts = build_alerts(decision, factors, pr)
    (OUT / "alerts_latest.json").write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "alerts": alerts}, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    report = validation_report(outcomes)
    (OUT / "validation_report_latest.md").write_text(report, encoding="utf-8")
    summary = {"version": VERSION, "decision_id": decision["decision_id"], "regime": regime, "risk": risk,
               "top_candidates": len(decision.get("top_candidates", [])), "outcomes": int(len(outcomes)),
               "portfolio_risk_status": pr.get("status"), "alerts": len(alerts)}
    (OUT / "system_summary_latest.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
