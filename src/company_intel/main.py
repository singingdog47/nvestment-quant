from __future__ import annotations
import json, os
from pathlib import Path
import pandas as pd, yaml
from .common import ensure_dir, save_json, load_json
from .targets import build_targets
from .tdnet import fetch_tdnet
from .edinet import fetch_edinet
from .sec import fetch_sec
from .company_ir import fetch_company_ir
from .news_rss import fetch_news_rss
from .snapshot import build_snapshot
from .quality import quality_report
from .brief import build_brief, load_market_regime
from .drive_publish import publish_directory
from .integration import integration_health
from .policy import build_policy_guardrails

CFG=yaml.safe_load(Path("config/intelligence_v1_6.yml").read_text(encoding="utf-8"))
OUT=ensure_dir(CFG["outputs"]["directory"]); STATE=ensure_dir(CFG["outputs"]["state_directory"])

def main():
    u=CFG["universe"]; s=CFG["sources"]; qcfg=CFG["quality"]
    targets=build_targets(u.get("screening_top_n",30),u.get("max_targets",80))
    targets.to_csv(OUT/"intelligence_targets_latest.csv",index=False,encoding="utf-8-sig")
    events=[]; health=[]
    if s["tdnet"].get("enabled"):
        e,h=fetch_tdnet(targets,s["tdnet"].get("lookback_days",7),s["tdnet"].get("pdf_extract",True),s["tdnet"].get("max_pdf_pages",5)); events+=e; health.append(h)
    if s["edinet"].get("enabled"):
        e,h=fetch_edinet(targets,s["edinet"].get("lookback_days",7)); events+=e; health.append(h)
    if s["sec"].get("enabled"):
        e,h=fetch_sec(targets,s["sec"].get("forms",[]),s["sec"].get("lookback_days",45)); events+=e; health.append(h)
    if s["company_ir"].get("enabled"):
        e,h=fetch_company_ir(targets); events+=e; health.append(h)
    if s["news_rss"].get("enabled"):
        e,h=fetch_news_rss(targets,s["news_rss"].get("max_items_per_company",5),s["news_rss"].get("priority_only",True)); events+=e; health.append(h)

    dedup={e.event_id:e for e in events}; events=list(dedup.values())
    order={"critical":0,"high":1,"normal":2,"low":3}; events.sort(key=lambda e:(order.get(e.priority,2),e.event_date),reverse=False)
    cols=["market","code","ticker","name","event_date","event_type","title","summary","source","source_url","source_tier","data_status","priority","fetched_at","event_id","raw_excerpt"]
    pd.DataFrame([e.asdict() for e in events],columns=cols).to_csv(OUT/"company_events_latest.csv",index=False,encoding="utf-8-sig")
    snapshot,yfh=build_snapshot(targets,s.get("yfinance",{}).get("enabled",True),s.get("yfinance",{}).get("max_targets",40)); health.append(yfh); snapshot.to_csv(OUT/"company_snapshot_latest.csv",index=False,encoding="utf-8-sig")
    pd.DataFrame([h.__dict__ for h in health]).to_csv(OUT/"source_health_latest.csv",index=False,encoding="utf-8-sig")
    quality=quality_report(targets,events,health,snapshot,qcfg.get("minimum_actionable_score",0.72)); save_json(OUT/"data_quality_latest.json",quality)

    old=load_json(STATE/"seen_events.json",{})
    new=[e for e in events if e.event_id not in old]
    pd.DataFrame([e.asdict() for e in new],columns=cols).to_csv(OUT/"company_events_new.csv",index=False,encoding="utf-8-sig")
    save_json(STATE/"seen_events.json",{e.event_id:e.fetched_at for e in events})

    regime=load_market_regime(); syshealth=integration_health(); policy=build_policy_guardrails(regime,quality); save_json(OUT/"system_health_latest.json",syshealth); save_json(OUT/"policy_guardrails_latest.json",policy); brief=build_brief(targets,events,health,quality,snapshot,regime,policy,syshealth)
    (OUT/"ai_context_latest.md").write_text(brief,encoding="utf-8")
    Path("data/ai_context_latest.md").write_text(brief,encoding="utf-8")
    context={"quality":quality,"market_regime":regime,"policy_guardrails":policy,"system_health":syshealth,"events":[e.asdict() for e in events[:100]],"source_health":[h.__dict__ for h in health]}
    save_json(OUT/"decision_context_latest.json",context)
    save_json("data/decision_context_latest.json",context)
    result=publish_directory(str(OUT)); save_json(OUT/"drive_publish_status.json",result)
    print(json.dumps({"targets":len(targets),"events":len(events),"new_events":len(new),"quality":quality,"drive":result},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
