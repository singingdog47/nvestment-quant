import pandas as pd
from company_intel.common import SourceHealth
from company_intel.quality import quality_report


def test_quality_blocks_missing_fundamentals():
    t=pd.DataFrame([{"code":"5401","source":"portfolio"}])
    s=t.copy(); s["fundamental_status"]="missing"
    h=[SourceHealth("TDnet","ok","now",0,"","primary"),SourceHealth("EDINET","ok","now",0,"","primary")]
    q=quality_report(t,[],h,s,0.8)
    assert q["actionable"] is False
    assert q["primary_fundamental_coverage"] == 0.0
    assert q["secondary_fundamental_coverage"] == 0.0


def test_quality_reports_secondary_coverage_without_calling_it_primary():
    t=pd.DataFrame([{"code":"5401","source":"screening"}])
    s=t.copy()
    s["fundamental_status"]="missing"
    s["secondary_snapshot_status"]="ok"
    s["secondary_fundamental_status"]="missing"
    h=[SourceHealth("TDnet","ok","now",0,"","primary"),SourceHealth("EDINET","ok","now",0,"","primary")]
    q=quality_report(t,[],h,s,0.0)
    assert q["primary_fundamental_coverage"] == 0.0
    assert q["secondary_fundamental_coverage"] == 1.0
    assert q["effective_fundamental_coverage"] == 0.65
    assert q["fundamental_evidence_tier"] == "secondary_only"


def test_unconfigured_optional_primary_feed_is_advisory_not_hard_block():
    t=pd.DataFrame([{"code":"5401","source":"screening"}])
    s=t.copy()
    s["fundamental_status"]="missing"
    s["secondary_snapshot_status"]="ok"
    s["secondary_fundamental_status"]="missing"
    h=[
        SourceHealth("TDnet","ok","now",0,"","primary"),
        SourceHealth("CompanyIR","ok","now",0,"","primary"),
        SourceHealth("EDINET","missing","now",0,"EDINET_API_KEY not set","primary"),
        SourceHealth("SEC","missing","now",0,"SEC_USER_AGENT not set","primary"),
    ]
    q=quality_report(t,[],h,s,0.72)
    assert q["primary_source_health"] == 1.0
    assert q["quality_score"] >= 0.72
    assert q["actionable"] is True
    assert len(q["optional_primary_sources_unconfigured"]) == 2
    assert q["optional_primary_sources_unconfigured"][0]["source"] == "EDINET"
