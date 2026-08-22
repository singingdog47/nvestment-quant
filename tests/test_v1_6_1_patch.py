import pandas as pd

from src.market_regime.breadth import compute_breadth


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
