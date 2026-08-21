from __future__ import annotations
import math
import pandas as pd
from .common import now_iso, clamp


def _metrics(s: pd.DataFrame) -> dict:
    if s is None or s.empty or "Close" not in s: return {}
    x=s.dropna(subset=["Close"]).copy()
    if len(x)<2: return {}
    close=x["Close"].astype(float)
    vol=x["Volume"].astype(float) if "Volume" in x else pd.Series(index=x.index,dtype=float)
    last=float(close.iloc[-1])
    def ret(n):
        return float(last/close.iloc[-1-n]-1) if len(close)>n and close.iloc[-1-n] else None
    def ma(n): return float(close.tail(n).mean()) if len(close)>=n else None
    r20=close.pct_change().tail(20)
    vol20=float(r20.std()*math.sqrt(252)) if r20.notna().sum()>=10 else None
    high52=float(close.tail(252).max()) if len(close) else None
    volume_ratio=None
    if len(vol)>=21 and vol.tail(20).mean() and pd.notna(vol.iloc[-1]): volume_ratio=float(vol.iloc[-1]/vol.tail(20).mean())
    return {
      "date":str(x.index[-1].date()),"close":last,"ret_1d":ret(1),"ret_5d":ret(5),"ret_20d":ret(20),"ret_60d":ret(60),
      "ma20":ma(20),"ma50":ma(50),"ma200":ma(200),"vol20_ann":vol20,"high_52w":high52,
      "drawdown_52w":float(last/high52-1) if high52 else None,"volume_ratio20":volume_ratio
    }


def fetch_market_history(symbols: dict, period="1y", interval="1d"):
    fetched=now_iso(); rows=[]; health=[]; hist={}
    try: import yfinance as yf
    except Exception as e:
        return pd.DataFrame(),{},[{"source":"yfinance_market","status":"missing","records":0,"fetched_at":fetched,"error":str(e),"source_tier":"secondary"}]
    for name,ticker in symbols.items():
        try:
            df=yf.download(ticker,period=period,interval=interval,auto_adjust=False,progress=False,threads=False)
            if isinstance(df.columns,pd.MultiIndex):
                df.columns=[c[0] for c in df.columns]
            m=_metrics(df)
            if not m: raise ValueError("insufficient history")
            m.update({"series":name,"ticker":ticker,"fetched_at":fetched,"data_status":"ok","source":"yfinance"})
            rows.append(m); hist[name]=df
            health.append({"source":f"yfinance:{ticker}","status":"ok","records":len(df),"fetched_at":fetched,"error":"","source_tier":"secondary"})
        except Exception as e:
            health.append({"source":f"yfinance:{ticker}","status":"error","records":0,"fetched_at":fetched,"error":f"{type(e).__name__}: {e}","source_tier":"secondary"})
    return pd.DataFrame(rows),hist,health


def trend_score(row: dict) -> float | None:
    if not row: return None
    score=50.0; parts=0
    for k,w in (("ret_20d",18),("ret_60d",18)):
        v=row.get(k)
        if v is not None:
            score += max(-w,min(w,float(v)*100*w/10)); parts+=1
    c=row.get("close")
    for k,w in (("ma20",8),("ma50",10),("ma200",12)):
        m=row.get(k)
        if c is not None and m:
            score += w if c>=m else -w; parts+=1
    return clamp(score) if parts else None
