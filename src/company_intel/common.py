from __future__ import annotations
import hashlib, json, os, re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

JST = timezone(timedelta(hours=9))

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def ensure_dir(path: str | Path) -> Path:
    p = Path(path); p.mkdir(parents=True, exist_ok=True); return p

def load_json(path: str | Path, default: Any=None) -> Any:
    p = Path(path)
    if not p.exists(): return {} if default is None else default
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {} if default is None else default

def save_json(path: str | Path, obj: Any) -> None:
    p = Path(path); ensure_dir(p.parent)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

def stable_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8", "ignore")).hexdigest()

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()

def normalize_code(code: Any) -> str:
    s = str(code or "").strip()
    s = re.sub(r"\.0$", "", s)
    if s.isdigit() and len(s) >= 4: return s[:4]
    return s.upper()

@dataclass
class SourceHealth:
    source: str
    status: str
    fetched_at: str
    records: int = 0
    error: str = ""
    source_tier: str = "primary"

@dataclass
class Event:
    market: str
    code: str
    ticker: str
    name: str
    event_date: str
    event_type: str
    title: str
    summary: str
    source: str
    source_url: str
    source_tier: str
    data_status: str
    priority: str
    fetched_at: str
    event_id: str
    raw_excerpt: str = ""

    def asdict(self): return asdict(self)
