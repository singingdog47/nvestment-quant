from __future__ import annotations
import os
from datetime import date,timedelta
import requests
from .common import Event, SourceHealth, now_iso, normalize_code, stable_hash
from .classify import classify_event

BASE="https://api.edinet-fsa.go.jp/api/v2/documents.json"

def fetch_edinet(targets, lookback_days=7):
    fetched=now_iso(); events=[]; errors=[]
    key=os.getenv("EDINET_API_KEY","")
    if not key: return events, SourceHealth("EDINET","missing",fetched,0,"EDINET_API_KEY not set","primary")
    codes={normalize_code(x): row for x,row in targets.set_index("code").iterrows()} if len(targets) else {}
    for i in range(lookback_days):
        d=(date.today()-timedelta(days=i)).isoformat()
        try:
            r=requests.get(BASE,params={"date":d,"type":2,"Subscription-Key":key},timeout=20); r.raise_for_status()
            for x in (r.json().get("results") or []):
                sec=normalize_code(x.get("secCode"))
                if sec not in codes: continue
                desc=x.get("docDescription") or x.get("formCode") or "EDINET filing"
                typ,sev=classify_event(desc)
                if typ=="disclosure":
                    typ="filing"; sev="high" if str(x.get("ordinanceCode","")).strip() else "normal"
                docid=x.get("docID","")
                url=f"https://disclosure2.edinet-fsa.go.jp/WEEK0010.aspx?docID={docid}" if docid else "https://disclosure2.edinet-fsa.go.jp/"
                row=codes[sec]; eid=stable_hash(f"edinet|{docid}|{sec}|{desc}")[:24]
                events.append(Event("JP",sec,row.get("ticker",f"{sec}.T"),row.get("name","") or "",str(x.get("submitDateTime",d))[:10],typ,desc,"","EDINET",url,"primary","ok",sev,fetched,eid,""))
        except Exception as e: errors.append(f"{d}:{type(e).__name__}:{e}")
    st="ok" if not errors else ("partial" if events else "error")
    return events, SourceHealth("EDINET",st,fetched,len(events)," | ".join(errors)[:1000],"primary")
