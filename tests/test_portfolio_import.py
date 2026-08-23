from src.portfolio_import import parse_rakuten_csv_bytes


def _sample() -> bytes:
    text = '''■資産合計\n\n■ 保有商品詳細 (すべて)\n\n種別,銘柄コード・ティッカー,銘柄,口座,保有数量,【単位】,平均取得価額,【単位】,現在値,【単位】,現在値(更新日),(参考為替),前日比,【単位】,時価評価額[円],時価評価額[外貨],評価損益[円],評価損益[％]\n国内株式,1605,ＩＮＰＥＸ,NISA成長投資枠,100,株,"1,696.50",円,"3,954.0",円,,,85,円,"395,400",-,"225,750",133.06\n国内株式,3923,ラクス,特定,200,株,977.25,円,"1,113.0",円,,,-12.5,円,"222,600",-,"27,150",13.89\n'''
    return text.encode("cp932")


def test_parse_cp932_rakuten_export():
    r = parse_rakuten_csv_bytes(_sample())
    assert r.rows_kept == 2
    assert r.portfolio["code"].tolist() == ["1605", "3923"]
    assert r.portfolio["ticker"].tolist() == ["1605.T", "3923.T"]
    assert r.portfolio["name"].tolist() == ["ＩＮＰＥＸ", "ラクス"]
    assert r.portfolio["market_value"].sum() == 618000
    assert abs(float(r.portfolio["weight"].sum()) - 1.0) < 1e-12


def test_values_and_accounts_preserved():
    r = parse_rakuten_csv_bytes(_sample())
    row = r.portfolio.iloc[0]
    assert row["quantity"] == 100
    assert row["avg_cost"] == 1696.50
    assert row["current_price"] == 3954.0
    assert row["account"] == "NISA成長投資枠"
    assert row["currency"] == "JPY"
