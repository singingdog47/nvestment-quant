from __future__ import annotations
import io
import pandas as pd, requests
from .common import now_iso

BASE="https://fred.stlouisfed.org/graph/fredgraph.csv"

def fetch_fred(series: dict):
    rows=[]; health=[]; fetched=now_iso()
    for name,sid in series.items():
        try:
            r=requests.get(BASE,params={"id":sid},timeout=20,headers={"User-Agent":"investment-quant/1.6"}); r.raise_for_status()
            df=pd.read_csv(io.StringIO(r.text))
            valcol=[c for c in df.columns if c!="DATE"][0]
            df[valcol]=pd.to_numeric(df[valcol],errors="coerce")
            x=df.dropna(subset=[valcol])
            if x.empty: raise ValueError("no observations")
            latest=x.iloc[-1]; prev=x.iloc[-2] if len(x)>1 else latest
            rows.append({"series":name,"fred_id":sid,"date":str(latest["DATE"]),"value":float(latest[valcol]),"previous":float(prev[valcol]),"change":float(latest[valcol]-prev[valcol]),"source":"FRED","source_url":r.url,"fetched_at":fetched,"data_status":"ok"})
            health.append({"source":f"FRED:{sid}","status":"ok","records":len(x),"fetched_at":fetched,"error":"","source_tier":"primary"})
        except Exception as e:
            health.append({"source":f"FRED:{sid}","status":"error","records":0,"fetched_at":fetched,"error":f"{type(e).__name__}: {e}","source_tier":"primary"})
    return pd.DataFrame(rows),health
