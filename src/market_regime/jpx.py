from __future__ import annotations
import io, re
from urllib.parse import urljoin
import pandas as pd, requests
from bs4 import BeautifulSoup
from .common import now_iso

UA="investment-quant/1.6 (+research)"

def _candidate_links(page, keywords):
    r=requests.get(page,timeout=20,headers={"User-Agent":UA}); r.raise_for_status()
    soup=BeautifulSoup(r.text,"lxml"); links=[]
    for a in soup.find_all("a",href=True):
        href=urljoin(page,a["href"]); text=(a.get_text(" ",strip=True)+" "+href).lower()
        if any(k.lower() in text for k in keywords) and re.search(r"\.(xlsx?|csv)(\?|$)",href,re.I): links.append(href)
    return list(dict.fromkeys(links))

def _read_url(url):
    r=requests.get(url,timeout=30,headers={"User-Agent":UA}); r.raise_for_status()
    if ".csv" in url.lower():
        for enc in ("utf-8-sig","cp932","utf-8"):
            try: return pd.read_csv(io.BytesIO(r.content),encoding=enc)
            except Exception: pass
        raise ValueError("csv decode failed")
    return pd.read_excel(io.BytesIO(r.content))

def fetch_jpx_sources(cfg: dict):
    fetched=now_iso(); frames={}; health=[]; index_rows=[]
    for name,s in cfg.items():
        if not s.get("enabled",True): continue
        pages=s.get("pages") or [s.get("page","")]
        try:
            page=""; links=[]
            last_error=None
            for candidate_page in pages:
                if not candidate_page: continue
                try:
                    candidate_links=_candidate_links(candidate_page,s.get("keywords",["xls","xlsx","csv"]))
                    if candidate_links:
                        page=candidate_page; links=candidate_links; break
                except Exception as ex:
                    last_error=ex
            if not links: raise ValueError(f"no downloadable table link found; last_error={last_error}")
            # Prefer filenames that contain a newer-looking YYYYMMDD/YYMMDD token; otherwise preserve page order.
            def key(u):
                nums=re.findall(r"(?<!\d)(20\d{6}|\d{6})(?!\d)",u)
                return max(nums) if nums else ""
            links=sorted(links,key=key,reverse=True)
            url=links[0]; df=_read_url(url); df=df.dropna(how="all")
            frames[name]=df.tail(80).copy()
            index_rows.append({"dataset":name,"page_url":page,"download_url":url,"rows":len(df),"fetched_at":fetched})
            health.append({"source":f"JPX:{name}","status":"ok","records":len(df),"fetched_at":fetched,"error":"","source_tier":"primary"})
        except Exception as e:
            health.append({"source":f"JPX:{name}","status":"error","records":0,"fetched_at":fetched,"error":f"{type(e).__name__}: {e}","source_tier":"primary"})
    return frames,pd.DataFrame(index_rows),health
