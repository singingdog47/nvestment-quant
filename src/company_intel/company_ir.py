from __future__ import annotations
from pathlib import Path
import pandas as pd, requests
from bs4 import BeautifulSoup
from .common import Event, SourceHealth, now_iso, normalize_code, clean_text, stable_hash, load_json, save_json
from .classify import classify_event

STATE="data/state/company_ir_hashes.json"
UA="investment-quant-intelligence/1.6"

def fetch_company_ir(targets):
    fetched=now_iso(); events=[]; errors=[]; state=load_json(STATE,{})
    if not Path("config/company_sources_v1_6.csv").exists(): return events,SourceHealth("CompanyIR","ok",fetched,0,"","primary")
    try: cfg=pd.read_csv("config/company_sources_v1_6.csv",comment="#",dtype=str).fillna("")
    except Exception as e: return events,SourceHealth("CompanyIR","error",fetched,0,str(e),"primary")
    tmap={normalize_code(r.code):r for _,r in targets.iterrows()}
    changed=False
    for _,r in cfg.iterrows():
        code=normalize_code(r.get("code","")); url=str(r.get("ir_url","")).strip()
        if code not in tmap or not url: continue
        try:
            res=requests.get(url,headers={"User-Agent":UA},timeout=15); res.raise_for_status()
            soup=BeautifulSoup(res.text,"lxml")
            for x in soup(["script","style","nav","footer"]): x.decompose()
            text=clean_text(soup.get_text(" ",strip=True))[:50000]; h=stable_hash(text)
            old=state.get(code,{}).get("hash")
            if old and old!=h:
                title=f"Company IR page changed: {r.get('name') or tmap[code].get('name','')}"
                typ,sev=classify_event(text[:5000]); sev="high" if typ!="disclosure" else "normal"
                eid=stable_hash(f"ir|{code}|{h}")[:24]
                events.append(Event("JP",code,tmap[code].get("ticker",f"{code}.T"),tmap[code].get("name","") or "",fetched[:10],typ,title,"Official IR page content changed","Company IR",url,"primary","ok",sev,fetched,eid,text[:2500]))
            state[code]={"hash":h,"fetched_at":fetched,"url":url}; changed=True
        except Exception as e: errors.append(f"{code}:{type(e).__name__}:{e}")
    if changed: save_json(STATE,state)
    st="ok" if not errors else ("partial" if events else "error")
    return events,SourceHealth("CompanyIR",st,fetched,len(events)," | ".join(errors)[:1000],"primary")
