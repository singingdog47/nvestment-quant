from __future__ import annotations
import json
from pathlib import Path

REQUIRED=[
 "data/regime/market_regime_latest.json",
 "data/regime/market_source_health_latest.csv",
 "data/data_coverage_latest.json",
 "data/intelligence/company_events_latest.csv",
 "data/intelligence/data_quality_latest.json",
 "data/intelligence/ai_context_latest.md",
 "data/intelligence/system_health_latest.json",
]

def main():
    result={p:Path(p).exists() for p in REQUIRED}
    result["all_required_present"]=all(result.values())
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["all_required_present"] else 1
if __name__=="__main__": raise SystemExit(main())
