import pandas as pd

from src.portfolio_import import parse_rakuten_csv_bytes


def _sample() -> bytes:
    text = '''■資産合計\n\n■ 保有商品詳細 (すべて)\n\n種別,銘柄コード・ティッカー,銘柄,口座,保有数量,【単位】,平均取得価額,【単位】,現在値,【単位】,現在値(更新日),(参考為替),前日比,【単位】,時価評価額[円],時価評価額[外貨],評価損益[円],評価損益[％]\n国内株式,1605,ＩＮＰＥＸ,NISA成長投資枠,100,株,"1,696.50",円,"3,954.0",円,,,85,円,"395,400",-,"225,750",133.06\n国内株式,3923,ラクス,特定,200,株,977.25,円,"1,113.0",円,,,-12.5,円,"222,600",-,"27,150",13.89\n'''
    return text.encode("cp932")


def test_parse_rakuten_cp932_holdings():
    r = parse_rakuten_csv_bytes(_sample())
    assert r.source_encoding in {"cp932", "shift_jis"}
    assert list(r.portfolio["code"]) == ["1605", "3923"]
    assert list(r.portfolio["ticker"]) == ["1605.T", "3923.T"]
    assert r.portfolio["market_value"].sum() == 618000
    assert abs(r.portfolio["weight"].sum() - 1.0) < 1e-12


def test_parser_ignores_summary_rows():
    r = parse_rakuten_csv_bytes(_sample())
    assert len(r.portfolio) == 2
    assert set(r.portfolio["currency"]) == {"JPY"}
