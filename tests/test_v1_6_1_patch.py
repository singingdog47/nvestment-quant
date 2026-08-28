import pandas as pd

from src.market_regime.breadth import compute_breadth
from src.market_regime.jpx import _parse_short_selling_pdf_text


def test_v13_breadth_columns_are_recognized(tmp_path):
    n = 120
    df = pd.DataFrame(
        {
            "price": [100.0] * n,
            "return_1m": [1.0] * 80 + [-1.0] * 40,
            "return_3m": [2.0] * 60 + [-2.0] * 60,
            "avg_turnover_30d": [1_000_000.0] * n,
        }
    )
    p = tmp_path / "screening.csv"
    df.to_csv(p, index=False)

    out, health = compute_breadth([str(p)], min_universe=100)

    assert out["status"] == "ok"
    assert out["pct_positive_return_1m"] == 80 / 120
    assert out["pct_positive_return_3m"] == 60 / 120
    assert out["turnover_metric_column"] == "avg_turnover_30d"
    assert out["participation_proxy"] is not None
    assert health[0]["error"] == ""


def test_stale_screening_is_not_presented_as_current_breadth(tmp_path):
    p = tmp_path / "screening.csv"
    n = 100
    source_as_of = (
        pd.Timestamp.now(tz="Asia/Tokyo") - pd.offsets.BDay(4)
    ).tz_convert("UTC").isoformat()
    pd.DataFrame(
        {
            "return_1m": [1.0] * n,
            "avg_turnover_30d": [1_000_000.0] * n,
            "data_retrieved_at_utc": [source_as_of] * n,
        }
    ).to_csv(p, index=False)
    out, health = compute_breadth([str(p)], min_universe=100, max_business_age_days=1)
    assert out["status"] == "stale"
    assert out["business_age_days"] > 1
    assert health[0]["status"] == "stale"


def test_jpx_short_selling_pdf_parser_exposes_official_turnover():
    text = """空売り集計（日次） 2026/8/28 【単位：百万円】
    2026年8月28日 5,140,754 56.5% 3,201,367 35.2% 751,240 8.3% 9,093,361
    """
    out = _parse_short_selling_pdf_text(text)
    assert out.iloc[0]["short_ratio_pct"] == 43.467
    assert out.iloc[0]["total_turnover_million_jpy"] == 9_093_361
