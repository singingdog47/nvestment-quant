from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ensure_dir(path: str | Path) -> Path:
    p=Path(path); p.mkdir(parents=True, exist_ok=True); return p


def save_json(path: str | Path, obj: Any) -> None:
    p=Path(path); ensure_dir(p.parent)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def load_json(path: str | Path, default=None):
    p=Path(path)
    if not p.exists(): return {} if default is None else default
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {} if default is None else default


def clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, float(v)))
