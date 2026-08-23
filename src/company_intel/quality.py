from __future__ import annotations
from datetime import datetime, timezone


def _ok_ratio(snapshot, column, total):
    if not len(snapshot) or column not in snapshot:
        return 0.0
    return float((snapshot[column] == "ok").sum()) / total


def _is_unconfigured_optional_source(h):
    err=str(h.error or "").lower()
    return h.status in ("missing","error") and "not set" in err


def quality_report(targets, events, health, snapshot, minimum=0.80):
    total=max(len(targets),1)
    primary_sources=[h for h in health if h.source_tier=="primary"]
    optional_unconfigured=[h for h in primary_sources if _is_unconfigured_optional_source(h)]
    configured_primary=[h for h in primary_sources if h not in optional_unconfigured]
    healthy=sum(h.status in ("ok","partial") for h in configured_primary)
    source_score=healthy/max(len(configured_primary),1)

    primary_f=_ok_ratio(snapshot,"fundamental_status",total)
    secondary_f=max(
        _ok_ratio(snapshot,"secondary_fundamental_status",total),
        _ok_ratio(snapshot,"secondary_snapshot_status",total),
    )
    effective_f=min(1.0, primary_f + 0.65*secondary_f)

    portfolio=targets[targets["source"]=="portfolio"] if len(targets) and "source" in targets else targets.iloc[0:0]
    p_codes=set(portfolio["code"]) if len(portfolio) else set()
    primary_event_codes={e.code for e in events if e.source_tier=="primary"}
    p_event=min(1.0,len(primary_event_codes & p_codes)/max(len(p_codes),1)) if p_codes else 1.0

    optional_primary=[]
    for h in optional_unconfigured:
        optional_primary.append({"source":h.source,"reason":str(h.error or "")})

    score=round(0.50*source_score+0.15*primary_f+0.30*effective_f+0.05*p_event,3)
    tier="primary" if primary_f>=0.8 else "mixed" if primary_f>0 else "secondary_only" if secondary_f>0 else "missing"
    return {
      "generated_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
      "targets":len(targets),"portfolio_targets":len(p_codes),"events":len(events),
      "primary_source_health":round(source_score,3),
      "configured_primary_sources":len(configured_primary),
      "optional_primary_sources_unconfigured":optional_primary,
      "fundamental_coverage":round(primary_f,3),
      "primary_fundamental_coverage":round(primary_f,3),
      "secondary_fundamental_coverage":round(secondary_f,3),
      "effective_fundamental_coverage":round(effective_f,3),
      "fundamental_evidence_tier":tier,
      # Backward-compatible alias. These are advisory, not hard blockers.
      "missing_primary_configuration":optional_primary,
      "portfolio_primary_event_presence":round(p_event,3),
      "quality_score":score,
      "actionable":bool(score>=minimum),
      "rule":"Optional primary feeds improve confidence but their absence alone must not block conclusions. Missing data still must not be converted into unsupported buy/sell conclusions."
    }
