from __future__ import annotations
import math
from .common import clamp
from .market_data import trend_score


def _row(df,name):
    if df is None or df.empty or "series" not in df: return {}
    x=df[df["series"]==name]
    return x.iloc[-1].to_dict() if len(x) else {}


def _fred(df,name):
    if df is None or df.empty or "series" not in df: return None
    x=df[df["series"]==name]
    # Cached values remain visible for audit/reporting but never masquerade as
    # current inputs to the regime score.
    if "data_status" in x.columns:
        x=x[x["data_status"].astype(str).str.lower()=="ok"]
    if not len(x): return None
    try:
        value=float(x.iloc[-1]["value"])
        return value if math.isfinite(value) else None
    except (TypeError, ValueError):
        return None


def score_regime(market_df, fred_df, breadth, jpx_health, cftc_df, weights, treasury_volatility=None):
    components={}; evidence={}; coverage={}
    trends=[]
    for n in ("JP_NIKKEI","JP_TOPIX_PROXY","US_SP500","US_NASDAQ"):
        s=trend_score(_row(market_df,n))
        if s is not None: trends.append(s)
    components["trend"]=sum(trends)/len(trends) if trends else None
    coverage["trend"]=len(trends)/4
    evidence["trend_series"]=len(trends)

    vix=_row(market_df,"VIX").get("close")
    hy=_fred(fred_df,"HY_OAS"); ig=_fred(fred_df,"IG_OAS")
    stress=[]
    if vix is not None: stress.append(clamp(100-(float(vix)-10)*3.0))
    if hy is not None: stress.append(clamp(100-(float(hy)-2.5)*14.0))
    if ig is not None: stress.append(clamp(100-(float(ig)-0.8)*35.0))
    treasury_expected=treasury_volatility is not None
    treasury_status=treasury_volatility.get("data_status") if isinstance(treasury_volatility,dict) else None
    treasury_score=treasury_volatility.get("stress_score") if isinstance(treasury_volatility,dict) else None
    if treasury_status == "ok" and treasury_score is not None:
        try:
            treasury_score=float(treasury_score)
            if math.isfinite(treasury_score): stress.append(clamp(treasury_score))
            else: treasury_score=None
        except (TypeError,ValueError): treasury_score=None
    else:
        treasury_score=None
    components["stress"]=sum(stress)/len(stress) if stress else None
    coverage["stress"]=len(stress)/(4 if treasury_expected else 3)
    evidence.update({
        "vix":vix,"hy_oas":hy,"ig_oas":ig,
        "treasury_volatility_proxy": treasury_volatility.get("curve_realized_vol_20d_bps_ann") if isinstance(treasury_volatility,dict) else None,
        "treasury_volatility_percentile_rank": treasury_volatility.get("percentile_rank") if isinstance(treasury_volatility,dict) else None,
        "treasury_volatility_stress_score": treasury_score,
        "treasury_volatility_as_of_date": treasury_volatility.get("as_of_date") if isinstance(treasury_volatility,dict) else None,
        "treasury_volatility_status": treasury_status,
        "treasury_volatility_is_ice_move": False,
    })

    part=breadth.get("participation_proxy") if isinstance(breadth,dict) else None
    components["participation"]=clamp(float(part)*100) if part is not None else None
    coverage["participation"]=1.0 if part is not None else 0.0
    evidence["breadth_n"]=breadth.get("n") if isinstance(breadth,dict) else None

    nfci=_fred(fred_df,"NFCI")
    # NFCI > 0 means tighter-than-average conditions. Market-volume proxies supplement it.
    liq=[]
    if nfci is not None: liq.append(clamp(50-float(nfci)*35))
    volume_ratios=[]
    for n in ("JP_TOPIX_PROXY","US_SP500","HYG","LQD"):
        vr=_row(market_df,n).get("volume_ratio20")
        if vr is not None:
            volume_ratios.append(float(vr)); liq.append(clamp(50+(float(vr)-1.0)*50))
    components["liquidity"]=sum(liq)/len(liq) if liq else None
    coverage["liquidity"]=len(liq)/5
    evidence["nfci"]=nfci
    evidence["volume_ratio20_mean"]=sum(volume_ratios)/len(volume_ratios) if volume_ratios else None

    # Positioning is scored only from normalized values. Merely fetching a source never creates a signal.
    healthy_jpx=sum(1 for h in jpx_health if h.get("status")=="ok") if jpx_health else 0
    pos_values=[]
    if cftc_df is not None and len(cftc_df):
        for c in ("asset_mgr_net_pct_oi","lev_money_net_pct_oi"):
            if c in cftc_df.columns:
                vals=cftc_df[c].dropna().astype(float)
                # ±20% net/open-interest maps approximately to 0..100, 0 maps to neutral 50.
                pos_values += [clamp(50+v*250) for v in vals.tolist()]
    components["positioning"]=sum(pos_values)/len(pos_values) if pos_values else None
    coverage["positioning"]=1.0 if pos_values else 0.0
    evidence["positioning_sources"]={"jpx_raw_healthy":healthy_jpx,"cftc_normalized_values":len(pos_values)}

    avail={k:v for k,v in components.items() if v is not None and not (isinstance(v,float) and math.isnan(v))}
    den=sum(float(weights.get(k,0)) for k in avail)
    score=sum(float(weights.get(k,0))*float(v) for k,v in avail.items())/den if den else None
    score=round(score,2) if score is not None else None

    total_weight=sum(float(x) for x in weights.values()) if weights else 0.0
    base_confidence=(
        sum(float(weights.get(k,0))*float(coverage.get(k,0)) for k in weights)
        / total_weight
        if total_weight
        else 0.0
    )
    # Credit and financial-conditions context is critical. If all three FRED
    # inputs are absent/stale, a superficially complete set of other components
    # must not yield confidence=1.0 or actionable=true.
    fred_core_present=sum(x is not None for x in (hy,ig,nfci))
    fred_core_coverage=fred_core_present/3
    critical_context_multiplier=0.70+0.30*fred_core_coverage
    confidence=round(base_confidence*critical_context_multiplier,3)
    evidence["component_coverage"]={k:round(v,3) for k,v in coverage.items()}
    evidence["critical_context_coverage"]={
        "fred_credit_financial_conditions":round(fred_core_coverage,3),
        "available":fred_core_present,
        "expected":3,
        "multiplier":round(critical_context_multiplier,3),
    }
    evidence["base_weighted_coverage"]=round(base_confidence,3)
    evidence["confidence_method"]="weighted subcomponent coverage x critical FRED context multiplier"
    return components,evidence,score,confidence


def regime_label(score, labels):
    if score is None: return "UNKNOWN"
    if score>=labels.get("risk_on",70): return "RISK_ON"
    if score>=labels.get("constructive",58): return "CONSTRUCTIVE"
    if score>=labels.get("neutral",42): return "NEUTRAL"
    if score>=labels.get("defensive",30): return "DEFENSIVE"
    return "RISK_OFF"
