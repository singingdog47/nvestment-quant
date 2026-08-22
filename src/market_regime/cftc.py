from __future__ import annotations
import io, zipfile
from datetime import datetime, timezone
import pandas as pd, requests
from .common import now_iso


def _find_col(cols, needles):
    for c in cols:
        norm=str(c).lower().replace(" ","_")
        if all(n.lower() in norm for n in needles): return c
    return None


def _normalize(df, market_col):
    if df.empty: return df
    cols=list(df.columns)
    oi=_find_col(cols,["open_interest","all"])
    am_l=_find_col(cols,["asset_mgr","long"]); am_s=_find_col(cols,["asset_mgr","short"])
    lm_l=_find_col(cols,["lev_money","long"]); lm_s=_find_col(cols,["lev_money","short"])
    out=pd.DataFrame({"contract":df[market_col].astype(str)})
    date_col=next((c for c in cols if "report_date" in str(c).lower().replace(" ","_")),None)
    if date_col: out["report_date"]=df[date_col].astype(str)
    if oi:
        o=pd.to_numeric(df[oi],errors="coerce")
        out["open_interest"]=o
        if am_l and am_s:
            net=pd.to_numeric(df[am_l],errors="coerce")-pd.to_numeric(df[am_s],errors="coerce")
            out["asset_mgr_net"]=net; out["asset_mgr_net_pct_oi"]=net/o.replace(0,pd.NA)
        if lm_l and lm_s:
            net=pd.to_numeric(df[lm_l],errors="coerce")-pd.to_numeric(df[lm_s],errors="coerce")
            out["lev_money_net"]=net; out["lev_money_net_pct_oi"]=net/o.replace(0,pd.NA)
    return out


def fetch_cftc(contracts):
    fetched=now_iso(); year=datetime.now(timezone.utc).year
    url=f"https://www.cftc.gov/files/dea/history/fut_fin_txt_{year}.zip"
    try:
        r=requests.get(url,timeout=30,headers={"User-Agent":"investment-quant/1.6"}); r.raise_for_status()
        z=zipfile.ZipFile(io.BytesIO(r.content)); name=z.namelist()[0]
        df=pd.read_csv(z.open(name),low_memory=False)
        market_col=next((c for c in df.columns if "market_and_exchange_names" in str(c).lower().replace(" ","_")),None)
        if not market_col: raise ValueError("market name column not found")
        mask=pd.Series(False,index=df.index)
        for k in contracts: mask |= df[market_col].astype(str).str.contains(k,case=False,na=False)
        out=df[mask].copy()
        date_col=next((c for c in out.columns if "report_date" in str(c).lower().replace(" ","_")),None)
        if date_col:
            out["_d"]=pd.to_datetime(out[date_col],errors="coerce")
            out=out.sort_values("_d").groupby(market_col,as_index=False).tail(1).drop(columns="_d")
        norm=_normalize(out,market_col)
        norm["source_url"]=url; norm["fetched_at"]=fetched; norm["data_status"]="ok"
        return norm,[{"source":"CFTC:COT","status":"ok","records":len(norm),"fetched_at":fetched,"error":"","source_tier":"primary"}],url
    except Exception as e:
        return pd.DataFrame(),[{"source":"CFTC:COT","status":"error","records":0,"fetched_at":fetched,"error":f"{type(e).__name__}: {e}","source_tier":"primary"}],url
