from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path


def _age_hours(p: Path):
    return round((datetime.now(timezone.utc).timestamp()-p.stat().st_mtime)/3600,2)


def _find(candidates):
    return next((Path(x) for x in candidates if Path(x).exists()),None)


def integration_health():
    groups={
      "market_regime":["data/regime/market_regime_latest.json"],
      "v1_3_screening":["data/screening_latest.csv"],
      "v1_3_screening_full":["data/screening_full.csv.gz"],
      "v1_3_quality":["data/quality_report.json"],
      "v1_3_daily_report":["data/daily_report.md"],
      "fundamentals":["data/fundamentals_latest.csv","data/intelligence/fundamentals_latest.csv"],
    }
    limits={
      "market_regime":36,"v1_3_screening":36,"v1_3_screening_full":36,"v1_3_quality":36,"v1_3_daily_report":36,
      "fundamentals":24*150,
    }
    out={"generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),"components":{}}
    for name,candidates in groups.items():
        found=_find(candidates)
        if found:
            age=_age_hours(found); limit=limits[name]
            out["components"][name]={"status":"ok" if age<=limit else "stale","path":str(found),"age_hours":age,"stale_limit_hours":limit}
        else:
            out["components"][name]={"status":"missing","path":"","age_hours":None,"stale_limit_hours":limits[name]}
    critical=["market_regime","v1_3_screening","v1_3_quality"]
    out["system_status"]="ok" if all(out["components"][x]["status"]=="ok" for x in critical) else "degraded"
    return out


def read_v1_3_daily_report(max_chars=6000):
    p=Path("data/daily_report.md")
    if not p.exists(): return ""
    try: return p.read_text(encoding="utf-8",errors="ignore")[:max_chars]
    except Exception: return ""
