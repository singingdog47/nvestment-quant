"""Parse third-party TDnet feed as candidate disclosures, never as verified absence.

Feed records require confirmation against JPX/issuer IR before event gate clearance.
"""
import json
from datetime import datetime, timezone

EARNINGS_TERMS = ("決算短信", "四半期決算", "業績予想", "業績修正", "配当予想", "決算説明")

def parse_disclosure_candidates(payload, symbols):
    """Accept normalized JSON array of {code,title,published_at,url}; fail closed."""
    if isinstance(payload, str):
        payload = json.loads(payload)
    if not isinstance(payload, list):
        raise ValueError("feed must be a list")
    wanted = set(str(x) for x in symbols)
    matches = {x: [] for x in wanted}
    for row in payload:
        if not isinstance(row, dict):
            continue
        code = str(row.get("code", "")).strip()
        if code not in wanted:
            continue
        title = str(row.get("title", "")).strip()
        if not title:
            continue
        matches[code].append({
            "title": title,
            "published_at": row.get("published_at"),
            "url": row.get("url"),
            "category": "EARNINGS_OR_FORECAST" if any(t in title for t in EARNINGS_TERMS) else "OTHER_DISCLOSURE",
            "source_state": "THIRD_PARTY_UNVERIFIED"
        })
    return matches

def candidate_manifest(matches, checked_at_utc):
    """Never produce NO_EVENT_CONFIRMED from an unverified third-party feed."""
    return [
        {"symbol": code, "checked_at_utc": checked_at_utc,
         "status": "UNKNOWN", "reviewed": False,
         "candidate_count": len(items),
         "candidate_disclosures": items}
        for code, items in sorted(matches.items())
    ]
