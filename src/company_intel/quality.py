from __future__ import annotations
from datetime import datetime, timezone

def quality_report(targets, events, health, snapshot, minimum=0.80):
    total=max(len(targets),1)
    primary_sources=[h for h in health if h.source_tier=="primary"]
    healthy=sum(h.status in ("ok","partial") for h in primary_sources)
    source_score=healthy/max(len(primary_sources),1)
    f_score=0.0
    if len(snapshot): f_score=float((snapshot.get("fundamental_status")=="ok").sum())/total
    portfolio=targets[targets["source"]=="portfolio"] if len(targets) and "source" in targets else targets.iloc[0:0]
    p_codes=set(portfolio["code"]) if len(portfolio) else set()
    primary_event_codes={e.code for e in events if e.source_tier=="primary"}
    # Event coverage is not the same as source coverage; no event can be valid. Keep small weight.
    p_event=min(1.0,len(primary_event_codes & p_codes)/max(len(p_codes),1)) if p_codes else 1.0
    score=round(0.55*source_score+0.40*f_score+0.05*p_event,3)
    return {
      "generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
      "targets":len(targets),"portfolio_targets":len(p_codes),"events":len(events),
      "primary_source_health":round(source_score,3),"fundamental_coverage":round(f_score,3),
      "portfolio_primary_event_presence":round(p_event,3),
      "quality_score":score,"actionable":bool(score>=minimum),
      "rule":"If actionable=false, AI must not turn missing data into a buy/sell conclusion."
    }
