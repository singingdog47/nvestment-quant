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
    return float(x.iloc[-1]["value"]) if len(x) else None


def score_regime(market_df, fred_df, breadth, jpx_health, cftc_df, weights):
    components={}; evidence={}
    trends=[]
    for n in ("JP_NIKKEI","JP_TOPIX_PROXY","US_SP500","US_NASDAQ"):
        s=trend_score(_row(market_df,n))
        if s is not None: trends.append(s)
    components["trend"]=sum(trends)/len(trends) if trends else None
    evidence["trend_series"]=len(trends)

    vix=_row(market_df,"VIX").get("close")
    hy=_fred(fred_df,"HY_OAS"); ig=_fred(fred_df,"IG_OAS")
    stress=[]
    if vix is not None: stress.append(clamp(100-(float(vix)-10)*3.0))
    if hy is not None: stress.append(clamp(100-(float(hy)-2.5)*14.0))
    if ig is not None: stress.append(clamp(100-(float(ig)-0.8)*35.0))
    components["stress"]=sum(stress)/len(stress) if stress else None
    evidence.update({"vix":vix,"hy_oas":hy,"ig_oas":ig})

    part=breadth.get("participation_proxy") if isinstance(breadth,dict) else None
    components["participation"]=clamp(float(part)*100) if part is not None else None
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
    evidence["positioning_sources"]={"jpx_raw_healthy":healthy_jpx,"cftc_normalized_values":len(pos_values)}

    avail={k:v for k,v in components.items() if v is not None and not (isinstance(v,float) and math.isnan(v))}
    den=sum(float(weights.get(k,0)) for k in avail)
    score=sum(float(weights.get(k,0))*float(v) for k,v in avail.items())/den if den else None
    score=round(score,2) if score is not None else None
    confidence=round(den/sum(float(x) for x in weights.values()),3) if weights else 0.0
    return components,evidence,score,confidence


def regime_label(score, labels):
    if score is None: return "UNKNOWN"
    if score>=labels.get("risk_on",70): return "RISK_ON"
    if score>=labels.get("constructive",58): return "CONSTRUCTIVE"
    if score>=labels.get("neutral",42): return "NEUTRAL"
    if score>=labels.get("defensive",30): return "DEFENSIVE"
    return "RISK_OFF"
