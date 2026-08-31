from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

VERSION = "1.0"
PRIMARY_SOURCE_TOKENS = ("edinet", "tdnet", "sec", "company ir", "company_ir", "official")


def _num(value: Any) -> float | None:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _series_num(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(index=df.index, dtype=float)
    return pd.to_numeric(df[column], errors="coerce")


def _join_key(df: pd.DataFrame) -> pd.Series:
    ticker = df.get("ticker", pd.Series("", index=df.index)).fillna("").astype(str).str.strip().str.upper()
    code = df.get("code", pd.Series("", index=df.index)).fillna("").astype(str).str.strip().str.upper()
    # Prefer ticker because US symbols are not numeric. Japanese importers already
    # normalize four-digit codes to <code>.T.
    return ticker.where(ticker.ne(""), code)


def _weighted_average(values: pd.Series, weights: pd.Series) -> tuple[float | None, float]:
    x = pd.to_numeric(values, errors="coerce")
    w = pd.to_numeric(weights, errors="coerce").fillna(0.0)
    valid = x.notna() & w.gt(0)
    coverage = float(w[valid].sum())
    if coverage <= 0:
        return None, 0.0
    return float((x[valid] * w[valid]).sum() / coverage), coverage


def _aggregate_multiple(values: pd.Series, weights: pd.Series) -> tuple[float | None, float]:
    """Aggregate P/E or P/B through the reciprocal yield, not arithmetic mean.

    For P/E this is equivalent to portfolio price / portfolio earnings when the
    supplied weights represent market-value weights and all included earnings are
    positive. Negative or zero denominators are excluded and their coverage is
    reported explicitly.
    """
    x = pd.to_numeric(values, errors="coerce")
    w = pd.to_numeric(weights, errors="coerce").fillna(0.0)
    valid = x.notna() & x.gt(0) & w.gt(0)
    coverage = float(w[valid].sum())
    if coverage <= 0:
        return None, 0.0
    reciprocal = float(((1.0 / x[valid]) * w[valid]).sum() / coverage)
    return (1.0 / reciprocal if reciprocal > 0 else None), coverage


def _source_tier(sources: list[str]) -> str:
    cleaned = [str(x).strip().lower() for x in sources if str(x).strip()]
    if not cleaned:
        return "unknown"
    return "primary" if all(any(token in x for token in PRIMARY_SOURCE_TOKENS) for x in cleaned) else "secondary_or_mixed"


def _valuation_label(score: float | None) -> str:
    if score is None:
        return "判断不能"
    if score >= 70:
        return "相対的に割安"
    if score >= 55:
        return "やや割安"
    if score >= 45:
        return "中立"
    if score >= 30:
        return "やや割高"
    return "相対的に割高"


def build_portfolio_valuation(
    portfolio: pd.DataFrame,
    screening: pd.DataFrame,
    generated_at: datetime | None = None,
) -> dict[str, Any]:
    now = (generated_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    if portfolio.empty:
        return {"version": VERSION, "status": "withheld", "reason": "portfolio_empty"}
    if screening.empty:
        return {"version": VERSION, "status": "withheld", "reason": "screening_empty"}
    pf = portfolio.copy()
    sc = screening.copy()
    if "market_value" not in pf.columns:
        return {"version": VERSION, "status": "withheld", "reason": "market_value_missing"}
    mv = pd.to_numeric(pf["market_value"], errors="coerce").fillna(0.0)
    total_mv = float(mv.sum())
    if total_mv <= 0:
        return {"version": VERSION, "status": "withheld", "reason": "market_value_nonpositive"}
    pf["_portfolio_weight"] = mv / total_mv
    pf["_valuation_key"] = _join_key(pf)
    sc["_valuation_key"] = _join_key(sc)
    # Screening should have one row per instrument, but deduplicate defensively.
    sc = sc.loc[sc["_valuation_key"].ne("")].drop_duplicates("_valuation_key", keep="first")
    merged = pf.merge(sc, on="_valuation_key", how="left", suffixes=("_pf", ""))
    matched = merged.get("price", pd.Series(index=merged.index, dtype=float)).notna()
    matched_weight = float(merged.loc[matched, "_portfolio_weight"].sum())

    pe, pe_cov = _aggregate_multiple(_series_num(merged, "pe"), merged["_portfolio_weight"])
    pb, pb_cov = _aggregate_multiple(_series_num(merged, "pb"), merged["_portfolio_weight"])
    dividend_yield, div_cov = _weighted_average(_series_num(merged, "dividend_yield"), merged["_portfolio_weight"])
    roe, roe_cov = _weighted_average(_series_num(merged, "roe"), merged["_portfolio_weight"])
    earnings_growth, eg_cov = _weighted_average(_series_num(merged, "earnings_growth"), merged["_portfolio_weight"])
    revenue_growth, rg_cov = _weighted_average(_series_num(merged, "revenue_growth"), merged["_portfolio_weight"])
    value_score, value_cov = _weighted_average(_series_num(merged, "value_score"), merged["_portfolio_weight"])
    quality_score, quality_cov = _weighted_average(_series_num(merged, "quality_score"), merged["_portfolio_weight"])
    growth_score, growth_cov = _weighted_average(_series_num(merged, "growth_score"), merged["_portfolio_weight"])
    earnings_yield = None if pe is None or pe <= 0 else 100.0 / pe

    score_inputs = []
    score_weights = []
    if value_score is not None:
        score_inputs.append(value_score); score_weights.append(0.75)
    if quality_score is not None:
        score_inputs.append(quality_score); score_weights.append(0.15)
    if growth_score is not None:
        score_inputs.append(growth_score); score_weights.append(0.10)
    guard_score = None
    if score_inputs:
        guard_score = float(sum(x * w for x, w in zip(score_inputs, score_weights)) / sum(score_weights))

    sources = sorted({str(x) for x in merged.get("fundamental_source", pd.Series(dtype=str)).dropna().tolist() if str(x).strip()})
    evidence_tier = _source_tier(sources)
    fundamental_ok = merged.get("fundamental_status", pd.Series(index=merged.index, dtype=str)).astype(str).str.lower().eq("ok")
    fundamental_coverage = float(merged.loc[fundamental_ok, "_portfolio_weight"].sum())
    min_core_coverage = min(pe_cov, pb_cov, value_cov) if all(x > 0 for x in (pe_cov, pb_cov, value_cov)) else 0.0

    if min_core_coverage >= 0.70:
        calculation_status = "current"
    elif matched_weight >= 0.30:
        calculation_status = "reference_only"
    else:
        calculation_status = "withheld"
    # Secondary/undocumented market fundamentals are useful for screening and
    # relative review, but primary confirmation is required before an actionable
    # valuation conclusion or coefficient change.
    decision_actionable = calculation_status == "current" and evidence_tier == "primary" and fundamental_coverage >= 0.70
    analysis_mode = "current" if decision_actionable else "reference_only" if calculation_status != "withheld" else "withheld"

    value_trap_flags: list[str] = []
    if value_score is not None and value_score >= 60 and quality_score is not None and quality_score < 40:
        value_trap_flags.append("cheap_but_low_quality")
    if value_score is not None and value_score >= 60 and growth_score is not None and growth_score < 35:
        value_trap_flags.append("cheap_but_low_growth")
    if earnings_growth is not None and earnings_growth < 0:
        value_trap_flags.append("weighted_earnings_growth_negative")
    if roe is not None and roe < 8:
        value_trap_flags.append("weighted_roe_below_8pct")

    per_holding = []
    for _, row in merged.iterrows():
        w = _num(row.get("_portfolio_weight")) or 0.0
        if w <= 0:
            continue
        per_holding.append({
            "ticker": row.get("ticker_pf", row.get("ticker")),
            "code": row.get("code_pf", row.get("code")),
            "name": row.get("name_pf", row.get("name")),
            "portfolio_weight": w,
            "market_value": _num(row.get("market_value")),
            "pe": _num(row.get("pe")),
            "pb": _num(row.get("pb")),
            "dividend_yield": _num(row.get("dividend_yield")),
            "roe": _num(row.get("roe")),
            "earnings_growth": _num(row.get("earnings_growth")),
            "value_score": _num(row.get("value_score")),
            "quality_score": _num(row.get("quality_score")),
            "growth_score": _num(row.get("growth_score")),
            "fundamental_status": row.get("fundamental_status"),
            "fundamental_source": row.get("fundamental_source"),
        })
    per_holding.sort(key=lambda x: x["portfolio_weight"], reverse=True)

    return {
        "version": VERSION,
        "generated_at": now.isoformat(timespec="seconds"),
        "status": calculation_status,
        "analysis_mode": analysis_mode,
        "decision_actionable": decision_actionable,
        "privacy": "PRIVATE_OUTPUT_ONLY",
        "evidence_tier": evidence_tier,
        "fundamental_sources": sources,
        "portfolio_market_value_jpy": total_mv,
        "coverage": {
            "screening_match": matched_weight,
            "fundamental_ok": fundamental_coverage,
            "pe": pe_cov,
            "pb": pb_cov,
            "dividend_yield": div_cov,
            "roe": roe_cov,
            "earnings_growth": eg_cov,
            "revenue_growth": rg_cov,
            "value_score": value_cov,
            "quality_score": quality_cov,
            "growth_score": growth_cov,
        },
        "metrics": {
            "aggregate_pe": pe,
            "aggregate_pb": pb,
            "earnings_yield_pct": earnings_yield,
            "weighted_dividend_yield_pct": dividend_yield,
            "weighted_roe_pct": roe,
            "weighted_earnings_growth_pct": earnings_growth,
            "weighted_revenue_growth_pct": revenue_growth,
            "relative_value_score": value_score,
            "quality_context_score": quality_score,
            "growth_context_score": growth_score,
            "value_trap_guard_score": guard_score,
            "valuation_label": _valuation_label(value_score),
        },
        "value_trap_flags": value_trap_flags,
        "limitations": [
            "relative_value_score is a cross-sectional screening measure, not a fair-value price target",
            "historical self-comparison requires persisted prior valuation snapshots",
            "fundamental inputs from secondary or undocumented sources are reference-only until primary IR/EDINET/TDnet/SEC confirmation",
            "funds without look-through fundamentals reduce coverage and are not imputed",
        ],
        "holdings": per_holding,
    }


def write_valuation_report(report: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    d = Path(out_dir); d.mkdir(parents=True, exist_ok=True)
    json_path = d / "portfolio_valuation_latest.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    m = report.get("metrics", {}); c = report.get("coverage", {})
    lines = [
        "# Private Portfolio Valuation v1.0", "",
        f"- Status: {report.get('status')}",
        f"- Analysis mode: {report.get('analysis_mode')}",
        f"- Trade-decision actionable: {report.get('decision_actionable')}",
        f"- Evidence tier: {report.get('evidence_tier')}",
        f"- Screening match coverage: {c.get('screening_match')}",
        f"- Fundamental OK coverage: {c.get('fundamental_ok')}", "",
        "## Portfolio valuation", 
        f"- Aggregate P/E: {m.get('aggregate_pe')}",
        f"- Aggregate P/B: {m.get('aggregate_pb')}",
        f"- Earnings yield: {m.get('earnings_yield_pct')}%",
        f"- Dividend yield: {m.get('weighted_dividend_yield_pct')}%",
        f"- Weighted ROE: {m.get('weighted_roe_pct')}%",
        f"- Weighted earnings growth: {m.get('weighted_earnings_growth_pct')}%",
        f"- Relative Value Score: {m.get('relative_value_score')}",
        f"- Quality context: {m.get('quality_context_score')}",
        f"- Growth context: {m.get('growth_context_score')}",
        f"- Value-trap guard: {m.get('value_trap_guard_score')}",
        f"- Label: **{m.get('valuation_label')}**", "",
        "## Value-trap checks",
    ]
    flags = report.get("value_trap_flags") or []
    lines += [f"- {x}" for x in flags] if flags else ["- No automatic value-trap flag detected."]
    lines += ["", "## Governance"] + [f"- {x}" for x in report.get("limitations", [])]
    lines += ["- Missing metrics are never imputed as zero.", "- Valuation does not directly trigger buy/sell orders.", "- PRIVATE: never commit or upload to public Actions artifacts."]
    md_path = d / "portfolio_valuation_latest.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
