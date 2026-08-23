from __future__ import annotations
from urllib.parse import quote
import feedparser
from .common import Event, SourceHealth, now_iso, stable_hash
from .classify import classify_event, is_low_value_news

BASE="https://news.google.com/rss/search?q={q}&hl=ja&gl=JP&ceid=JP:ja"

def fetch_news_rss(targets,max_items_per_company=5,priority_only=True):
    fetched=now_iso(); events=[]; errors=[]
    subset=targets
    if priority_only and len(targets): subset=targets[targets["priority"].str.lower().isin(["critical","high"])]
    for _,r in subset.iterrows():
        name=str(r.get("name","")).strip(); code=str(r.get("code","")).strip()
        if not name and not code: continue
        q=quote(f'"{name}" OR "{code}"')
        try:
            f=feedparser.parse(BASE.format(q=q))
            for e in f.entries[:max_items_per_company]:
                title=str(e.get("title","")); link=str(e.get("link","")); date=str(e.get("published",fetched[:10]))
                source=str(e.get("source",{}).get("title","") if isinstance(e.get("source",{}),dict) else e.get("source",""))
                if is_low_value_news(title,source):
                    continue
                typ,sev=classify_event(title)
                if typ=="disclosure": sev="normal"
                eid=stable_hash(f"rss|{code}|{link}|{title}")[:24]
                events.append(Event(str(r.get("market","JP")),code,str(r.get("ticker","")),name,date[:16],typ,title,"Secondary news detection only; verify with primary source before acting.","Google News RSS",link,"secondary","unverified",sev,fetched,eid,""))
        except Exception as ex: errors.append(f"{code}:{type(ex).__name__}:{ex}")
    st="ok" if not errors else ("partial" if events else "error")
    return events,SourceHealth("NewsRSS",st,fetched,len(events)," | ".join(errors)[:1000],"secondary")
