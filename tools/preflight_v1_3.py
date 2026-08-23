from __future__ import annotations
import argparse, json, re
from pathlib import Path

EXPECTED=["data/screening_latest.csv","data/screening_full.csv.gz","data/quality_report.json","data/daily_report.md"]
REQUIRED_V1_3_SOURCES = [
    "src/main.py",
    "src/config.py",
    "src/reporting.py",
    "src/scoring.py",
    "src/tradingview.py",
    "src/universe.py",
]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--ci",action="store_true"); args=ap.parse_args()
    found={p:Path(p).exists() for p in EXPECTED}
    workflows=list(Path(".github/workflows").glob("*.yml"))+list(Path(".github/workflows").glob("*.yaml")) if Path(".github/workflows").exists() else []
    wf_text="\n".join(p.read_text(encoding="utf-8",errors="ignore") for p in workflows)
    workflow_names=[]
    for p in workflows:
        text=p.read_text(encoding="utf-8",errors="ignore")
        m=re.search(r"(?m)^name:\s*[\"\']?([^\n\"\']+)",text)
        if m: workflow_names.append(m.group(1).strip())
    checks={
      "v1_3_outputs":found,
      "v1_3_sources": {p: Path(p).exists() for p in REQUIRED_V1_3_SOURCES},
      "workflow_names":workflow_names,
      "daily_quant_screen_detected":any(n=="Daily Quant Screen" for n in workflow_names),
      "known_1617_jst_cron_detected":bool(re.search(r"cron:\s*[\"\']17\s+7\s+\*\s+\*\s+1-5[\"\']",wf_text)),
      "existing_workflow_count":len(workflows),
    }
    compatibility_ok = (
        checks["daily_quant_screen_detected"]
        and checks["known_1617_jst_cron_detected"]
        and all(checks["v1_3_sources"].values())
    )
    checks["upgrade_is_additive"] = compatibility_ok
    checks["will_not_overwrite_daily_workflow"] = checks["daily_quant_screen_detected"]
    checks["status"] = "ok" if compatibility_ok else "error"
    print(json.dumps(checks,ensure_ascii=False,indent=2))
    # Generated data may legitimately be absent on a fresh checkout, but CI must
    # stop if the workflow or implementation it claims to preserve is missing.
    return 1 if args.ci and not compatibility_ok else 0
if __name__=="__main__": raise SystemExit(main())
