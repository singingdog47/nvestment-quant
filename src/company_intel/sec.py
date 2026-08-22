from __future__ import annotations
import os, requests
from datetime import datetime, timezone, timedelta
from .common import Event, SourceHealth, now_iso, stable_hash
from .classify import classify_event

MAP="https://www.sec.gov/files/company_tickers.json"
BASE="https://data.sec.gov/submissions/CIK{cik}.json"

def fetch_sec(targets, forms, lookback_days=45):
    fetched=now_iso(); events=[]; errors=[]
    ua=os.getenv("SEC_USER_AGENT","").strip()
    if not ua: return events, SourceHealth("SEC","missing",fetched,0,"SEC_USER_AGENT not set","primary")
    us=targets[targets["market"].str.upper().isin(["US","USA"])] if len(targets) else targets
    if us.empty: return events, SourceHealth("SEC","ok",fetched,0,"","primary")
    headers={"User-Agent":ua,"Accept-Encoding":"gzip, deflate"}
    try:
        m=requests.get(MAP,headers=headers,timeout=20); m.raise_for_status()
        mp={str(v["ticker"]).upper(): str(v["cik_str"]).zfill(10) for v in m.json().values()}
    except Exception as e:
        return events, SourceHealth("SEC","error",fetched,0,f"ticker map: {e}","primary")
    cutoff=(datetime.now(timezone.utc)-timedelta(days=lookback_days)).date()
    for _,row in us.iterrows():
        ticker=str(row.get("ticker","")).upper(); cik=mp.get(ticker)
        if not cik: errors.append(f"{ticker}:CIK missing"); continue
        try:
            r=requests.get(BASE.format(cik=cik),headers=headers,timeout=20); r.raise_for_status()
            recent=r.json().get("filings",{}).get("recent",{})
            n=len(recent.get("form",[]))
            for i in range(n):
                form=recent["form"][i]
                if form not in forms: continue
                fd=datetime.fromisoformat(recent["filingDate"][i]).date()
                if fd<cutoff: continue
                acc=recent["accessionNumber"][i].replace("-","")
                doc=recent.get("primaryDocument",[""]*n)[i]
                url=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{doc}"
                title=f"SEC {form} filing"
                typ,sev=classify_event(title); typ="earnings" if form in ("10-Q","10-K","20-F") else "filing"; sev="high"
                eid=stable_hash(f"sec|{ticker}|{recent['accessionNumber'][i]}")[:24]
                events.append(Event("US",str(row.get("code",ticker)),ticker,row.get("name","") or "",fd.isoformat(),typ,title,"","SEC EDGAR",url,"primary","ok",sev,fetched,eid,""))
        except Exception as e: errors.append(f"{ticker}:{type(e).__name__}:{e}")
    st="ok" if not errors else ("partial" if events else "error")
    return events, SourceHealth("SEC",st,fetched,len(events)," | ".join(errors)[:1000],"primary")
