from __future__ import annotations
import os
from pathlib import Path
import pandas as pd
from .common import normalize_code

PRIVATE_CANDIDATES = [
    "config/portfolio.csv", "data/portfolio_latest.csv", "data/portfolio_snapshot_latest.csv"
]

def _read_csv(path):
    try: return pd.read_csv(path, dtype=str, low_memory=False)
    except Exception: return pd.DataFrame()

def _canonical(df: pd.DataFrame, source: str, default_priority="normal") -> pd.DataFrame:
    cols=["market","code","ticker","name","priority","source"]
    if df.empty: return pd.DataFrame(columns=cols)
    ren={}
    for c in df.columns:
        lc=str(c).strip().lower()
        if lc in ("銘柄コード","code","security_code"): ren[c]="code"
        elif lc in ("ticker","symbol","銘柄コード・ティッカー"): ren[c]="ticker"
        elif lc in ("銘柄名","銘柄","name","company"): ren[c]="name"
        elif lc in ("market","市場"): ren[c]="market"
        elif lc in ("priority","watch_priority"): ren[c]="priority"
    df=df.rename(columns=ren).copy()
    if "code" not in df and "ticker" in df:
        df["code"]=df["ticker"].astype(str).str.replace(r"\.T$","",regex=True)
    if "ticker" not in df and "code" in df:
        df["ticker"]=df["code"]
    if "code" not in df: return pd.DataFrame(columns=cols)
    df["code"]=df["code"].map(normalize_code)
    if "market" not in df:
        df["market"]=df["code"].map(lambda x:"JP" if str(x).isdigit() else "US")
    df["market"]=df["market"].astype(str).str.upper().replace({"JAPAN":"JP","USA":"US","UNITED STATES":"US"})
    if "ticker" not in df: df["ticker"]=df["code"]
    df["ticker"]=df.apply(lambda r: f"{r['code']}.T" if r["market"]=="JP" and str(r["code"]).isdigit() else str(r["ticker"]),axis=1)
    if "name" not in df: df["name"]=""
    if "priority" not in df: df["priority"]=default_priority
    df["source"]=source
    return df[cols]

def build_targets(screening_top_n=30, max_targets=80) -> pd.DataFrame:
    pieces=[]
    # v1.3 intentionally keeps portfolio quantities/costs out of the public repo.
    # Private repository portfolio files are read only when explicitly allowed.
    if os.getenv("ALLOW_REPO_PORTFOLIO","0")=="1":
        for p in PRIVATE_CANDIDATES:
            if Path(p).exists():
                x=_canonical(_read_csv(p),"portfolio","critical")
                if not x.empty: pieces.append(x)
    if Path("config/intelligence_watchlist.csv").exists():
        x=_canonical(_read_csv("config/intelligence_watchlist.csv"),"watchlist","high")
        if not x.empty: pieces.append(x)
    for p in ["data/screening_latest.csv","data/screening_full.csv.gz"]:
        if Path(p).exists():
            s=_read_csv(p).head(screening_top_n)
            x=_canonical(s,"screening","normal")
            if not x.empty: pieces.append(x)
            break
    if not pieces: return pd.DataFrame(columns=["market","code","ticker","name","priority","source"])
    out=pd.concat(pieces,ignore_index=True)
    rank={"critical":0,"high":1,"normal":2,"low":3}
    out["_r"]=out["priority"].astype(str).str.lower().map(rank).fillna(2)
    out=out.sort_values(["_r","source"]).drop_duplicates(["market","code"],keep="first")
    return out.head(max_targets).drop(columns="_r").reset_index(drop=True)
