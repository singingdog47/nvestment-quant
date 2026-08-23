from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

VERSION = "1.8.0"
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
    ticker = str(row.get("ticker") or "").strip()
    code = str(row.get("code") or "").strip()
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
    if "ticker" not in out.columns and "code" not in out.columns:
        raise ValueError("portfolio requires ticker or code")
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
    out = out[out["symbol"].notna()].copy()
    if out.empty:
        raise ValueError("no valid symbols")
    return out.reset_index(drop=True)


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
        return {"status": "insufficient_market_data"}
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
        "status": "ok" if len(port) >= 30 else "partial",
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


def analyze(portfolio: pd.DataFrame, screen: pd.DataFrame, config: RiskConfig = RiskConfig(), fetcher=fetch_close) -> dict[str, Any]:
    pf = normalize_portfolio(portfolio)
    candidates = screen.copy() if not screen.empty else pd.DataFrame()
    if not candidates.empty:
        candidates["symbol"] = candidates.apply(yahoo_symbol, axis=1)
        sort_col = "regime_adjusted_score" if "regime_adjusted_score" in candidates.columns else "total_score" if "total_score" in candidates.columns else None
        if sort_col:
            candidates[sort_col] = _num(candidates[sort_col])
            candidates = candidates.sort_values(sort_col, ascending=False, na_position="last")
        candidates = candidates[~candidates["symbol"].isin(set(pf["symbol"])) & candidates["symbol"].notna()].head(config.candidate_top_n)
    symbols = list(pf["symbol"].unique()) + ([config.benchmark] if config.benchmark else []) + list(candidates.get("symbol", []))
    returns, fetch_errors = build_return_matrix(symbols, config, fetcher=fetcher)
    metrics = portfolio_metrics(pf, returns, config.benchmark, config.var_confidence)
    weights = pf.groupby("symbol")["weight"].sum()
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
    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "privacy": "PRIVATE_OUTPUT_ONLY",
        "portfolio": {
            "holdings": int(len(pf)),
            "concentration": concentration_stats(weights),
            "metrics": metrics,
            "metadata_exposures": metadata,
            "factor_tilts": factor_tilts(pf, screen),
        },
        "candidate_impact": impacts,
        "data_quality": {
            "price_series_requested": int(len(set(symbols))),
            "price_series_available": int(len(returns.columns)),
            "fetch_errors": fetch_errors,
            "minimum_observations": config.min_observations,
        },
        "rules": [
            "Risk estimates are historical estimates, not forecasts.",
            "Missing sector/currency/rate/FX metadata is reported as missing and never inferred.",
            "Candidate verdict describes portfolio-level risk diversification only; it is not a buy/sell signal.",
            "No order is ever placed by this module.",
        ],
    }


def write_private_report(report: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    d = Path(out_dir); d.mkdir(parents=True, exist_ok=True)
    json_path = d / "portfolio_risk_latest.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=_json_default), encoding="utf-8")
    lines = ["# Portfolio Risk Report v1.8", "", f"Generated: {report.get('generated_at')}", ""]
    p = report.get("portfolio", {}); m = p.get("metrics", {}); c = p.get("concentration", {})
    lines += ["## Core risk", f"- Holdings: {p.get('holdings')}", f"- Beta: {m.get('beta')}",
              f"- Annualized volatility: {m.get('annualized_volatility')}", f"- 1-day VaR: {m.get('var_1d')}",
              f"- 1-day CVaR: {m.get('cvar_1d')}", f"- Max drawdown: {m.get('max_drawdown')}",
              f"- HHI: {c.get('hhi')}", f"- Effective holdings: {c.get('effective_holdings')}", "", "## Candidate impact"]
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
    screen = pd.read_csv(screen_path) if screen_path.exists() else pd.DataFrame()
    config = RiskConfig(
        lookback_days=int(os.getenv("RISK_LOOKBACK_DAYS", "400")),
        min_observations=int(os.getenv("RISK_MIN_OBSERVATIONS", "120")),
        var_confidence=float(os.getenv("RISK_VAR_CONFIDENCE", "0.95")),
        candidate_weight=float(os.getenv("RISK_CANDIDATE_WEIGHT", "0.02")),
        candidate_top_n=int(os.getenv("RISK_CANDIDATE_TOP_N", "10")),
        benchmark=os.getenv("RISK_BENCHMARK", DEFAULT_BENCHMARK),
    )
    report = analyze(portfolio, screen, config=config)
    paths = write_private_report(report, out_dir)
    # Deliberately print only non-sensitive execution metadata.
    print(json.dumps({"version": VERSION, "status": "ok", "private_outputs_written": len(paths),
                      "holdings_count": report.get("portfolio", {}).get("holdings"),
                      "candidate_count": len(report.get("candidate_impact", []))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
