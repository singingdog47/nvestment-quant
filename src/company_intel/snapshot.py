from __future__ import annotations
from pathlib import Path
import pandas as pd
from .common import now_iso, SourceHealth

POSSIBLE=["data/fundamentals_latest.csv","data/intelligence/fundamentals_latest.csv","data/screening_latest.csv","data/intelligence/screening_latest.csv"]

def _merge_existing(base):
    for p in POSSIBLE:
        if not Path(p).exists(): continue
        try: df=pd.read_csv(p,dtype=str)
        except Exception: continue
        code_col=next((c for c in df.columns if str(c).lower() in ("code","ticker","銘柄コード","symbol")),None)
        if not code_col: continue
        tmp=df.copy(); tmp["_code"]=tmp[code_col].astype(str).str.extract(r"(\d{4})",expand=False).fillna(tmp[code_col].astype(str))
        merged=base.merge(tmp.drop_duplicates("_code"),left_on="code",right_on="_code",how="left",suffixes=("","_src"))
        src_cols=[c for c in tmp.columns if c not in (code_col,"_code")]
        if src_cols:
            available=merged[src_cols].notna().any(axis=1)
            merged.loc[available,"fundamental_status"]="ok"
        merged["fundamental_source_file"]=p
        return merged
    base["fundamental_source_file"]=""
    return base

def _yf_fallback(df,max_targets=40):
    try: import yfinance as yf
    except Exception as e: return df, SourceHealth("yfinance","missing",now_iso(),0,str(e),"secondary")
    rows=0; errors=[]
    wanted=df[df["fundamental_status"]!="ok"].head(max_targets)
    for idx,r in wanted.iterrows():
        ticker=str(r.get("ticker","")).strip()
        if not ticker: continue
        try:
            t=yf.Ticker(ticker); info=t.info or {}
            fields={
              "yf_price": info.get("currentPrice") or info.get("regularMarketPrice"),
              "yf_market_cap":info.get("marketCap"),"yf_trailing_pe":info.get("trailingPE"),"yf_forward_pe":info.get("forwardPE"),
              "yf_pbr":info.get("priceToBook"),"yf_roe":info.get("returnOnEquity"),"yf_profit_margin":info.get("profitMargins"),
              "yf_revenue_growth":info.get("revenueGrowth"),"yf_earnings_growth":info.get("earningsGrowth"),"yf_dividend_yield":info.get("dividendYield"),"yf_beta":info.get("beta")
            }
            for k,v in fields.items(): df.loc[idx,k]=v
            if any(v is not None for v in fields.values()):
                df.loc[idx,"secondary_snapshot_status"]="ok"; df.loc[idx,"secondary_snapshot_source"]="yfinance"; rows+=1
        except Exception as e: errors.append(f"{ticker}:{type(e).__name__}")
    st="ok" if not errors else ("partial" if rows else "error")
    return df, SourceHealth("yfinance",st,now_iso(),rows," | ".join(errors)[:1000],"secondary")

def build_snapshot(targets,yfinance_enabled=True,yfinance_max_targets=40):
    base=targets.copy(); base["fetched_at"]=now_iso(); base["fundamental_status"]="missing"
    base["secondary_snapshot_status"]="missing"; base["secondary_snapshot_source"]=""
    merged=_merge_existing(base)
    if yfinance_enabled: return _yf_fallback(merged,yfinance_max_targets)
    return merged, SourceHealth("yfinance","disabled",now_iso(),0,"","secondary")
