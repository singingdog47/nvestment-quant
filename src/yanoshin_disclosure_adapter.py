"""Free, unofficial Yanoshin Atom candidate feed (NOT primary-source verification).

Public per-code Atom endpoints documented by provider. Does not scrape JPX.
Network errors and missing entries never imply 'no earnings'.
"""
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from xml.etree import ElementTree
from datetime import datetime, timezone
import re

BASE = "https://webapi.yanoshin.jp/webapi/tdnet/list/"
ATOM = "{http://www.w3.org/2005/Atom}"

def fetch_candidate_atom(symbol, limit=100, opener=urlopen):
    symbol = str(symbol).strip().upper()
    if not re.fullmatch(r"[0-9A-Z]{4}", symbol):
        raise ValueError("Expected four-character Japanese security code")
    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise ValueError("limit must be 1..100")
    url = BASE + symbol + ".atom?" + urlencode({"limit": limit})
    req = Request(url, headers={"User-Agent": "investment-quant-disclosure-candidate/1.0"})
    with opener(req, timeout=15) as response:
        raw = response.read(2_000_001)
    if len(raw) > 2_000_000:
        raise RuntimeError("Oversized candidate feed; fail closed")
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError as exc:
        raise RuntimeError("Invalid Atom feed; fail closed") from exc
    if root.tag != ATOM + "feed":
        raise RuntimeError("Unexpected feed format; fail closed")
    records = []
    for entry in root.findall(ATOM + "entry"):
        title = entry.findtext(ATOM + "title", default="").strip()
        published = entry.findtext(ATOM + "published") or entry.findtext(ATOM + "updated")
        link = next((e.get("href") for e in entry.findall(ATOM + "link")
                     if e.get("href", "").startswith("https://")), None)
        if not title or not published:
            continue
        try:
            dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                continue
        except ValueError:
            continue
        records.append({"code": symbol, "title": title,
                        "published_at": dt.astimezone(timezone.utc).isoformat(),
                        "url": link, "source": "YANOSHIN_UNOFFICIAL_ATOM"})
    return {"symbol": symbol, "source_url": url, "candidate_disclosures": records,
            "complete": False, "primary_verified": False}
