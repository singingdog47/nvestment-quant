from __future__ import annotations

import io
import re
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from .common import now_iso

UA = "investment-quant/1.6.1 (+research)"


def _get(url, timeout=25):
    r = requests.get(
        url,
        timeout=timeout,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/vnd.ms-excel,"
                      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,"
                      "text/csv,*/*;q=0.8",
        },
    )
    r.raise_for_status()
    return r


def _candidate_links(page, keywords):
    r = _get(page, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")
    links = []

    for a in soup.find_all("a", href=True):
        href = urljoin(page, a["href"])
        text = (a.get_text(" ", strip=True) + " " + href).lower()
        is_table_file = bool(re.search(r"\.(xlsx?|csv)(?:\?|#|$)", href, re.I))
        keyword_hit = any(k.lower() in text for k in keywords)

        # Prefer actual downloadable spreadsheet/csv links.  Do not require
        # anchor text to literally contain "xls", because JPX changes labels.
        if is_table_file and (keyword_hit or True):
            links.append(href)

    return list(dict.fromkeys(links))


def _topic_tokens(page):
    path = urlparse(page).path.lower()
    known = ["short-selling", "investor-type", "margin"]
    return [k for k in known if k in path]


def _related_pages(page, limit=12):
    """One-level discovery for JPX pages whose download link moved to a subpage."""
    r = _get(page, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")
    host = urlparse(page).netloc
    tokens = _topic_tokens(page)
    out = []

    for a in soup.find_all("a", href=True):
        href = urljoin(page, a["href"])
        parsed = urlparse(href)
        if parsed.netloc != host:
            continue
        low = href.lower()
        if tokens and not any(t in low for t in tokens):
            continue
        if href == page:
            continue
        out.append(href)
        if len(out) >= limit:
            break

    return list(dict.fromkeys(out))


def _read_url(url):
    r = _get(url, timeout=30)

    if ".csv" in url.lower():
        for enc in ("utf-8-sig", "cp932", "utf-8"):
            try:
                return pd.read_csv(io.BytesIO(r.content), encoding=enc)
            except Exception:
                pass
        raise ValueError("csv decode failed")

    return pd.read_excel(io.BytesIO(r.content))


def _read_html_table(page):
    """Fallback for JPX datasets published as HTML rather than a file."""
    r = _get(page, timeout=25)
    tables = pd.read_html(io.StringIO(r.text))
    if not tables:
        raise ValueError("no HTML table found")

    usable = [
        t.dropna(how="all").dropna(axis=1, how="all")
        for t in tables
        if len(t) >= 2 and len(t.columns) >= 2
    ]
    if not usable:
        raise ValueError("no usable HTML table found")

    return max(usable, key=lambda t: len(t) * len(t.columns))


def _newest_link(links):
    def key(u):
        nums = re.findall(r"(?<!\d)(20\d{6}|\d{6})(?!\d)", u)
        return max(nums) if nums else ""
    return sorted(links, key=key, reverse=True)[0]


def fetch_jpx_sources(cfg: dict):
    fetched = now_iso()
    frames = {}
    health = []
    index_rows = []

    for name, s in cfg.items():
        if not s.get("enabled", True):
            continue

        pages = s.get("pages") or [s.get("page", "")]
        try:
            chosen_page = ""
            chosen_url = ""
            df = None
            errors = []

            for page in [p for p in pages if p]:
                # 1) Direct downloadable table on landing page.
                try:
                    links = _candidate_links(
                        page, s.get("keywords", ["xls", "xlsx", "csv"])
                    )
                    if links:
                        chosen_page = page
                        chosen_url = _newest_link(links)
                        df = _read_url(chosen_url)
                        break
                except Exception as ex:
                    errors.append(f"{page}:direct:{type(ex).__name__}:{ex}")

                # 2) Static HTML table fallback.
                try:
                    candidate = _read_html_table(page)
                    if len(candidate):
                        chosen_page = page
                        chosen_url = page + "#html-table"
                        df = candidate
                        break
                except Exception as ex:
                    errors.append(f"{page}:html:{type(ex).__name__}:{ex}")

                # 3) One-level related-page discovery.
                try:
                    for sub in _related_pages(page):
                        try:
                            links = _candidate_links(
                                sub, s.get("keywords", ["xls", "xlsx", "csv"])
                            )
                            if links:
                                chosen_page = sub
                                chosen_url = _newest_link(links)
                                df = _read_url(chosen_url)
                                break
                        except Exception as ex:
                            errors.append(
                                f"{sub}:sub:{type(ex).__name__}:{ex}"
                            )
                    if df is not None:
                        break
                except Exception as ex:
                    errors.append(f"{page}:discover:{type(ex).__name__}:{ex}")

            if df is None:
                raise ValueError(
                    "no downloadable or HTML table found; "
                    + " | ".join(errors[-6:])
                )

            df = df.dropna(how="all")
            frames[name] = df.tail(80).copy()
            index_rows.append(
                {
                    "dataset": name,
                    "page_url": chosen_page,
                    "download_url": chosen_url,
                    "rows": len(df),
                    "fetched_at": fetched,
                }
            )
            health.append(
                {
                    "source": f"JPX:{name}",
                    "status": "ok",
                    "records": len(df),
                    "fetched_at": fetched,
                    "error": "",
                    "source_tier": "primary",
                }
            )
        except Exception as e:
            health.append(
                {
                    "source": f"JPX:{name}",
                    "status": "error",
                    "records": 0,
                    "fetched_at": fetched,
                    "error": f"{type(e).__name__}: {e}",
                    "source_tier": "primary",
                }
            )

    return frames, pd.DataFrame(index_rows), health
