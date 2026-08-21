import pandas as pd
from company_intel.common import SourceHealth
from company_intel.quality import quality_report

def test_quality_blocks_missing_fundamentals():
    t=pd.DataFrame([{"code":"5401","source":"portfolio"}])
    s=t.copy(); s["fundamental_status"]="missing"
    h=[SourceHealth("TDnet","ok","now",0,"","primary"),SourceHealth("EDINET","ok","now",0,"","primary")]
    q=quality_report(t,[],h,s,0.8)
    assert q["actionable"] is False
