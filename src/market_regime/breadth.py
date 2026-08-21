from __future__ import annotations
from pathlib import Path
import pandas as pd
from .common import now_iso

RET_CANDS=["return_1d","ret_1d","return_20d","ret_20d","momentum_1m","mom_1m","momentum_3m","mom_3m","momentum_6m","mom_6m"]
TURNOVER_CANDS=["turnover_20d","avg_turnover_20d","average_turnover_20d","turnover","avg_turnover","volume_20d","avg_volume_20d"]

def _read(p):
    return pd.read_csv(p,compression="infer",low_memory=False)

def compute_breadth(candidates, min_universe=100):
    fetched=now_iso(); source=""
    for p in candidates:
        if Path(p).exists():
            try: df=_read(p); source=p; break
            except Exception: continue
    else:
        return {"status":"missing","fetched_at":fetched,"source":"","n":0},[{"source":"v1.3 screening_full","status":"missing","records":0,"fetched_at":fetched,"error":"no readable screening file","source_tier":"internal"}]
    n=len(df)
    out={"status":"ok" if n>=min_universe else "partial","fetched_at":fetched,"source":source,"n":n}
    # Use only columns that really exist. Missing metrics stay missing; no guessing.
    pos_metrics=[]
    for c in RET_CANDS:
        if c in df.columns:
            s=pd.to_numeric(df[c],errors="coerce")
            valid=s.notna().sum()
            if valid>=min_universe:
                pct=float((s>0).sum()/valid)
                out[f"pct_positive_{c}"]=pct; pos_metrics.append(pct)
    # 52w proximity if available
    price=next((c for c in ["price","close","last","current_price"] if c in df.columns),None)
    hi=next((c for c in ["high_52w","52w_high","high52"] if c in df.columns),None)
    lo=next((c for c in ["low_52w","52w_low","low52"] if c in df.columns),None)
    if price and hi:
        p=pd.to_numeric(df[price],errors="coerce"); h=pd.to_numeric(df[hi],errors="coerce"); valid=(p.notna()&h.notna()&(h>0))
        if valid.sum()>=min_universe: out["pct_within_5pct_52w_high"]=float((p[valid]>=0.95*h[valid]).mean())
    if price and lo:
        p=pd.to_numeric(df[price],errors="coerce"); l=pd.to_numeric(df[lo],errors="coerce"); valid=(p.notna()&l.notna()&(l>0))
        if valid.sum()>=min_universe: out["pct_within_5pct_52w_low"]=float((p[valid]<=1.05*l[valid]).mean())
    out["participation_proxy"]=(sum(pos_metrics)/len(pos_metrics)) if pos_metrics else None
    turnover_col=next((c for c in TURNOVER_CANDS if c in df.columns),None)
    if turnover_col:
        tv=pd.to_numeric(df[turnover_col],errors="coerce").dropna()
        if len(tv)>=min_universe:
            out["turnover_metric_column"]=turnover_col
            out["turnover_universe_sum"]=float(tv.sum())
            out["turnover_universe_median"]=float(tv.median())
            out["turnover_coverage"]=float(len(tv)/max(len(df),1))
    health=[{"source":"v1.3 breadth adapter","status":out["status"],"records":n,"fetched_at":fetched,"error":"" if pos_metrics else "no compatible return/momentum column; participation missing","source_tier":"internal"}]
    return out,health
