"""Optional licensed J-Quants TDnet adapter.

No credentials, no automatic polling, no fallback to scraping. Fails closed.
Use only with an authorized TimelyDisclosure add-on and explicit operator action.
"""
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.jquants.com/v2/td/list"

def fetch_tdnet_list(code, start, end, api_key=None, opener=urlopen):
    key = os.environ.get("JQUANTS_API_KEY") if api_key is None else api_key
    if not key:
        raise RuntimeError("J-Quants API key missing; no disclosure coverage can be asserted")
    if not (str(code).isdigit() and len(str(code)) in (4, 5)):
        raise ValueError("Invalid JP stock code")
    if not (len(start) == len(end) == 10 and start <= end):
        raise ValueError("Invalid date range")
    url = API + "?" + urlencode({"code": code, "from": start, "to": end})
    req = Request(url, headers={"x-api-key": key, "Accept": "application/json"})
    with opener(req, timeout=15) as response:
        data = json.load(response)
    if not isinstance(data, dict) or "data" not in data or not isinstance(data["data"], list):
        raise RuntimeError("Unexpected J-Quants disclosure schema; fail closed")
    if data.get("pagination_key") or data.get("cursor"):
        raise RuntimeError("Incomplete paginated response; fail closed")
    return data["data"]
