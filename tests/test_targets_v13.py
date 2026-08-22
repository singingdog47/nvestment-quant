import pandas as pd
from company_intel.targets import _canonical


def test_v13_ticker_only_schema_is_accepted():
    df=pd.DataFrame([{"ticker":"9432","market":"JP","price_date":"2026-08-21","total_score":"82.4","flags":"ok"}])
    out=_canonical(df,"screening","normal")
    assert len(out)==1
    assert out.iloc[0]["code"]=="9432"
    assert out.iloc[0]["ticker"]=="9432.T"
