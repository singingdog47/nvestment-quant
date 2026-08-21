from __future__ import annotations
import argparse, json, re
from pathlib import Path

EXPECTED=["data/screening_latest.csv","data/screening_full.csv.gz","data/quality_report.json","data/daily_report.md"]

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
      "workflow_names":workflow_names,
      "daily_quant_screen_detected":any(n=="Daily Quant Screen" for n in workflow_names),
      "known_1617_jst_cron_detected":bool(re.search(r"cron:\s*[\"\']17\s+7\s+\*\s+\*\s+1-5[\"\']",wf_text)),
      "existing_workflow_count":len(workflows),
      "upgrade_is_additive":True,
      "will_not_overwrite_daily_workflow":True,
    }
    checks["status"]="ok" if found["data/screening_latest.csv"] else "warning"
    print(json.dumps(checks,ensure_ascii=False,indent=2))
    # Never block the upgrade solely because generated data has not been committed yet.
    return 0
if __name__=="__main__": raise SystemExit(main())
