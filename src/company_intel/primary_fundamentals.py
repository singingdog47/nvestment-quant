"""Conservative EDINET primary fundamentals ingestion (official type=5 CSV ZIP).

Only standard, unambiguous consolidated/current-year JPY facts are accepted.
Missing and non-comparable facts remain missing; no estimates or fallback promotion.
"""
from __future__ import annotations

import csv
import io
import os
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests

from .common import now_iso

DOCUMENT_URL = "https://api.edinet-fsa.go.jp/api/v2/documents/{docid}"
COLUMNS = [
    "code", "ticker", "source_tier", "source", "document_id", "source_url",
    "filed_date", "period_context", "currency_unit", "extracted_at",
    "net_sales_jpy", "operating_income_jpy", "net_income_jpy",
    "operating_cash_flow_jpy", "assets_jpy", "liabilities_jpy",
]
DURATION = {
    "NetSales": "net_sales_jpy",
    "Revenue": "net_sales_jpy",
    "OperatingIncome": "operating_income_jpy",
    "ProfitLossAttributableToOwnersOfParent": "net_income_jpy",
    "NetCashProvidedByUsedInOperatingActivities": "operating_cash_flow_jpy",
}
INSTANT = {"Assets": "assets_jpy", "Liabilities": "liabilities_jpy"}


def _field_index(header: list[str], *candidates: str) -> int | None:
    normalized = [s.strip().replace(" ", "").lower() for s in header]
    for target in candidates:
        target = target.strip().lower()
        if target in normalized:
            return normalized.index(target)
    return None


def _csv_rows(raw: bytes):
    for encoding in ("utf-16", "utf-16-le", "utf-8-sig", "cp932"):
        try:
            text = raw.decode(encoding)
            if "\t" not in text[:1500]:
                continue
            yield from csv.reader(io.StringIO(text), delimiter="\t")
            return
        except (UnicodeError, csv.Error):
            continue


def extract_csv_zip(content: bytes) -> dict:
    """Return confirmed current-year consolidated facts, never ambiguous segment values."""
    candidates: dict[str, float] = {}
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        members = [
            n for n in archive.namelist()
            if "XBRL_TO_CSV/" in n.upper() and n.lower().endswith(".csv")
            and not n.startswith("/") and ".." not in Path(n).parts
        ]
        if len(members) > 100:
            raise ValueError("unexpectedly large EDINET CSV ZIP")
        for name in members:
            if archive.getinfo(name).file_size > 20_000_000:
                continue
            rows = _csv_rows(archive.read(name))
            header = next(rows, [])
            element_i = _field_index(header, "要素ID", "elementid")
            context_i = _field_index(header, "コンテキストID", "contextid")
            value_i = _field_index(header, "値", "value")
            unit_i = _field_index(header, "ユニットID", "単位ID", "unitid")
            if None in (element_i, context_i, value_i, unit_i):
                continue
            for row in rows:
                if max(element_i, context_i, value_i, unit_i) >= len(row):
                    continue
                context = row[context_i].strip()
                # Exclude standalone, segment, restated and quarterly comparisons.
                if context not in ("CurrentYearDuration", "CurrentYearInstant"):
                    continue
                unit = row[unit_i].strip().lower()
                if unit not in ("jpy", "iso4217:jpy"):
                    continue
                element = row[element_i].strip().split(":")[-1]
                mapping = DURATION if context == "CurrentYearDuration" else INSTANT
                metric = mapping.get(element)
                if not metric:
                    continue
                raw_value = row[value_i].strip().replace(",", "")
                if not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", raw_value):
                    continue
                value = float(raw_value)
                if metric in candidates and candidates[metric] != value:
                    # Contradictory duplicate tags invalidate the metric.
                    candidates[metric] = float("nan")
                elif metric not in candidates:
                    candidates[metric] = value
    return {key: value for key, value in candidates.items() if pd.notna(value)}


def document_id(event) -> str | None:
    if getattr(event, "source", None) != "EDINET":
        return None
    values = parse_qs(urlparse(str(getattr(event, "source_url", ""))).query).get("docID", [])
    docid = values[0] if values else ""
    return docid if re.fullmatch(r"[A-Za-z0-9]{6,20}", docid) else None


def collect_primary_fundamentals(events, previous_path: str | Path, *, session=None,
                                 max_documents: int = 12, max_age_days: int = 450) -> tuple[pd.DataFrame, dict]:
    path = Path(previous_path)
    old = pd.read_csv(path, dtype={"code": str}) if path.exists() and path.stat().st_size else pd.DataFrame(columns=COLUMNS)
    if "filed_date" in old:
        old["filed_date"] = pd.to_datetime(old["filed_date"], errors="coerce", utc=True)
        age = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=max_age_days)
        old = old[old["filed_date"] >= age].copy()
        old["filed_date"] = old["filed_date"].dt.strftime("%Y-%m-%d")
    old = old.reindex(columns=COLUMNS)
    existing = set(old["document_id"].dropna().astype(str))
    eligible = []
    for e in events:
        docid = document_id(e)
        if not docid or docid in existing:
            continue
        title = str(getattr(e, "title", ""))
        # Use actual financial filings only. Material events remain event-only.
        if not any(x in title for x in ("有価証券報告書", "半期報告書", "四半期報告書")):
            continue
        eligible.append((str(getattr(e, "event_date", "")), docid, e))
    eligible.sort(reverse=True)
    http = session or requests.Session()
    added = []
    errors = []
    seen = set()
    resolved = []
    for _, docid, e in eligible:
        if docid in seen or len(seen) >= max_documents:
            continue
        seen.add(docid)
        try:
            key = os.getenv("EDINET_API_KEY", "")
            if not key:
                break
            response = http.get(
                DOCUMENT_URL.format(docid=docid),
                params={"type": 5, "Subscription-Key": key},
                timeout=35,
            )
            response.raise_for_status()
            facts = extract_csv_zip(response.content)
            resolved.append(docid)
            if not facts:
                continue
            added.append({
                "code": str(e.code), "ticker": str(e.ticker),
                "source_tier": "primary", "source": "EDINET",
                "document_id": docid, "source_url": str(e.source_url),
                "filed_date": str(e.event_date), "period_context": "CurrentYear",
                "currency_unit": "JPY", "extracted_at": now_iso(), **facts,
            })
        except Exception as exc:
            errors.append(f"{docid}:{type(exc).__name__}")
    fresh = pd.DataFrame(added, columns=COLUMNS)
    all_rows = pd.concat([old, fresh], ignore_index=True).reindex(columns=COLUMNS)
    if len(all_rows):
        all_rows = all_rows.sort_values(["filed_date", "document_id"], ascending=False)
        all_rows = all_rows.drop_duplicates("document_id", keep="first")
        # Keep document lineage for audit elsewhere; snapshot uses latest per company.
        all_rows = all_rows.drop_duplicates("code", keep="first").reset_index(drop=True)
    return all_rows, {"checked": len(seen), "resolved_document_ids": resolved,
                      "new_companies": len(fresh), "errors": errors,
                      "primary_companies": len(all_rows), "status": "partial" if errors else "ok"}


def write_primary_fundamentals(frame: pd.DataFrame, output: str | Path) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.reindex(columns=COLUMNS).to_csv(path, index=False, encoding="utf-8")
