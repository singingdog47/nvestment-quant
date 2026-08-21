from __future__ import annotations
import io, re
from datetime import date, timedelta
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from .common import Event, SourceHealth, now_iso, normalize_code, clean_text, stable_hash
from .classify import classify_event

BASE="https://www.release.tdnet.info/inbs/"
UA="investment-quant-intelligence/1.6 (+research; contact via repository)"

def _pdf_excerpt(url, max_pages=5):
    try:
        r=requests.get(url, timeout=20, headers={"User-Agent":UA}); r.raise_for_status()
        reader=PdfReader(io.BytesIO(r.content)); texts=[]
        for p in reader.pages[:max_pages]: texts.append(p.extract_text() or "")
        text=clean_text(" ".join(texts))
        keys=["業績予想","配当","自己株式","売上高","営業利益","経常利益","親会社株主に帰属","M&A","買収"]
        positions=[text.find(k) for k in keys if text.find(k)>=0]
        if positions:
            i=max(0,min(positions)-500); return text[i:i+3500]
        return text[:3000]
    except Exception:
        return ""

def fetch_tdnet(targets, lookback_days=7, pdf_extract=True, max_pdf_pages=5):
    fetched=now_iso(); events=[]; err=[]
    codes={normalize_code(x): row for x,row in targets.set_index("code").iterrows()} if len(targets) else {}
    seen=set()
    for d in [date.today()-timedelta(days=i) for i in range(lookback_days)]:
        ds=d.strftime("%Y%m%d")
        first=urljoin(BASE,f"I_list_001_{ds}.html")
        try:
            r=requests.get(first, timeout=15, headers={"User-Agent":UA})
            if r.status_code!=200: continue
            soup=BeautifulSoup(r.text,"lxml")
            page_urls={first}
            for a in soup.find_all("a", href=True):
                href=a["href"]
                if re.search(rf"I_list_\d+_{ds}\.html",href): page_urls.add(urljoin(BASE,href))
            for page in sorted(page_urls):
                rr=requests.get(page, timeout=15, headers={"User-Agent":UA}); rr.raise_for_status()
                ss=BeautifulSoup(rr.text,"lxml")
                for tr in ss.find_all("tr"):
                    cells=[clean_text(c.get_text(" ",strip=True)) for c in tr.find_all(["td","th"])]
                    if len(cells)<3: continue
                    code=""
                    for c in cells:
                        m=re.search(r"\b(\d{4})\b",c)
                        if m: code=m.group(1); break
                    if code not in codes: continue
                    pdf=""
                    for a in tr.find_all("a",href=True):
                        if ".pdf" in a["href"].lower(): pdf=urljoin(BASE,a["href"]); break
                    title=max(cells, key=len) if cells else ""
                    if not title: continue
                    row=codes[code]; typ,sev=classify_event(title)
                    eid=stable_hash(f"tdnet|{ds}|{code}|{title}|{pdf}")[:24]
                    if eid in seen: continue
                    seen.add(eid)
                    excerpt=_pdf_excerpt(pdf,max_pdf_pages) if (pdf_extract and pdf and sev in ("critical","high")) else ""
                    events.append(Event("JP",code,row.get("ticker",f"{code}.T"),row.get("name","") or "",d.isoformat(),typ,title,"", "TDnet",pdf or page,"primary", "ok",sev,fetched,eid,excerpt))
        except Exception as e: err.append(f"{ds}:{type(e).__name__}:{e}")
    status="ok" if not err else ("partial" if events else "error")
    return events, SourceHealth("TDnet",status,fetched,len(events)," | ".join(err)[:1000],"primary")
