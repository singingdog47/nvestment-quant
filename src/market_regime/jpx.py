from __future__ import annotations

import io
import re
from datetime import date
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
        extensions = ["xlsx?", "csv"]
        if any(str(k).lower() == "pdf" for k in keywords):
            extensions.append("pdf")
        is_table_file = bool(
            re.search(rf"\.({'|'.join(extensions)})(?:\?|#|$)", href, re.I)
        )
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

    if ".pdf" in url.lower():
        from pypdf import PdfReader

        text = "\n".join(page.extract_text() or "" for page in PdfReader(io.BytesIO(r.content)).pages)
        return _parse_short_selling_pdf_text(text)

    if ".csv" in url.lower():
        for enc in ("utf-8-sig", "cp932", "utf-8"):
            try:
                return pd.read_csv(io.BytesIO(r.content), encoding=enc)
            except Exception:
                pass
        raise ValueError("csv decode failed")

    return pd.read_excel(io.BytesIO(r.content))


def _parse_short_selling_pdf_text(text):
    """Parse JPX's official daily short-selling summary PDF.

    The same table also contains the official approximate TSE turnover total,
    allowing the engine to expose it without substituting an ETF proxy.
    """
    normalized = " ".join(str(text).replace("▲", "-").split())
    pattern = re.compile(
        r"(?P<year>20\d{2})年\s*(?P<month>\d{1,2})月\s*(?P<day>\d{1,2})日\s*"
        r"(?P<actual>[\d,]+)\s*(?P<actual_pct>[\d.]+)%\s*"
        r"(?P<regulated>[\d,]+)\s*(?P<regulated_pct>[\d.]+)%\s*"
        r"(?P<unregulated>[\d,]+)\s*(?P<unregulated_pct>[\d.]+)%\s*"
        r"(?P<total>[\d,]+)"
    )
    match = pattern.search(normalized)
    if not match:
        raise ValueError("JPX short-selling summary row not found in PDF")

    values = match.groupdict()
    as_of = date(int(values["year"]), int(values["month"]), int(values["day"]))
    actual = int(values["actual"].replace(",", ""))
    regulated = int(values["regulated"].replace(",", ""))
    unregulated = int(values["unregulated"].replace(",", ""))
    total = int(values["total"].replace(",", ""))
    short_total = regulated + unregulated
    return pd.DataFrame(
        [
            {
                "date": as_of.isoformat(),
                "actual_order_turnover_million_jpy": actual,
                "actual_order_ratio_pct": float(values["actual_pct"]),
                "short_regulated_turnover_million_jpy": regulated,
                "short_regulated_ratio_pct": float(values["regulated_pct"]),
                "short_unregulated_turnover_million_jpy": unregulated,
                "short_unregulated_ratio_pct": float(values["unregulated_pct"]),
                "short_turnover_million_jpy": short_total,
                "short_ratio_pct": round(100 * short_total / total, 3) if total else None,
                "total_turnover_million_jpy": total,
            }
        ]
    )


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


def _flatten_columns(df):
    out = df.copy()
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [
            " ".join(str(x) for x in col if str(x) != "nan").strip()
            for col in out.columns
        ]
    else:
        out.columns = [str(c).strip() for c in out.columns]
    return out


def _validate_frame(name, df, rules=None):
    """Validate payload structure separately from HTTP/download success."""
    rules = rules or {}
    min_rows = int(rules.get("min_rows", 2))
    min_columns = int(rules.get("min_columns", 2))
    min_numeric_values = int(rules.get("min_numeric_values", 1))
    if not isinstance(df, pd.DataFrame):
        return pd.DataFrame(), {
            "valid": False,
            "rows": 0,
            "columns": 0,
            "numeric_values": 0,
            "issues": ["payload is not a DataFrame"],
        }

    clean = _flatten_columns(df).dropna(how="all").dropna(axis=1, how="all")
    numeric_values = 0
    for column in clean.columns:
        norm = re.sub(r"[\s_\-]+", "", str(column).lower())
        if any(token in norm for token in ("date", "日付", "年月", "期間")):
            continue
        values = (
            clean[column]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.replace("−", "-", regex=False)
            .str.strip()
            .replace({"": pd.NA, "-": pd.NA, "—": pd.NA, "nan": pd.NA})
        )
        numeric_values += int(pd.to_numeric(values, errors="coerce").notna().sum())

    issues = []
    if len(clean) < min_rows:
        issues.append(f"rows<{min_rows}")
    if len(clean.columns) < min_columns:
        issues.append(f"columns<{min_columns}")
    if numeric_values < min_numeric_values:
        issues.append(f"numeric_values<{min_numeric_values}")
    return clean, {
        "dataset": name,
        "valid": not issues,
        "rows": len(clean),
        "columns": len(clean.columns),
        "numeric_values": numeric_values,
        "issues": issues,
    }


def fetch_jpx_sources(cfg: dict):
    fetched = now_iso()
    frames = {}
    health = []
    index_rows = []

    for name, s in cfg.items():
        if not s.get("enabled", True):
            health.append(
                {
                    "source": f"JPX:{name}",
                    "status": "not_implemented",
                    "transport_status": "not_attempted",
                    "content_status": "not_checked",
                    "records": 0,
                    "fetched_at": fetched,
                    "error": "source disabled by configuration",
                    "source_tier": "primary",
                }
            )
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

            df, validation = _validate_frame(name, df, s.get("validation"))
            frames[name] = df.tail(80).copy()
            overall_status = "ok" if validation["valid"] else "partial"
            validation_error = "; ".join(validation["issues"])
            index_rows.append(
                {
                    "dataset": name,
                    "page_url": chosen_page,
                    "download_url": chosen_url,
                    "rows": len(df),
                    "columns": validation["columns"],
                    "numeric_values": validation["numeric_values"],
                    "data_status": overall_status,
                    "validation_error": validation_error,
                    "fetched_at": fetched,
                }
            )
            health.append(
                {
                    "source": f"JPX:{name}",
                    "status": overall_status,
                    "transport_status": "ok",
                    "content_status": "valid" if validation["valid"] else "invalid",
                    "records": len(df),
                    "columns": validation["columns"],
                    "numeric_values": validation["numeric_values"],
                    "fetched_at": fetched,
                    "error": validation_error,
                    "source_tier": "primary",
                }
            )
        except Exception as e:
            health.append(
                {
                    "source": f"JPX:{name}",
                    "status": "missing",
                    "transport_status": "error",
                    "content_status": "not_checked",
                    "records": 0,
                    "fetched_at": fetched,
                    "error": f"{type(e).__name__}: {e}",
                    "source_tier": "primary",
                }
            )

    short_frame = frames.get("short_selling")
    if short_frame is not None and not short_frame.empty and "total_turnover_million_jpy" in short_frame.columns:
        frames["official_turnover"] = short_frame[["date", "total_turnover_million_jpy"]].copy()
        health.append(
            {
                "source": "JPX:official_turnover",
                "status": "ok",
                "transport_status": "ok",
                "content_status": "valid",
                "records": len(frames["official_turnover"]),
                "fetched_at": fetched,
                "error": "",
                "source_tier": "primary",
            }
        )

    return frames, pd.DataFrame(index_rows), health
