from src.portfolio_import import classify_fx_exposure, infer_portfolio_source_as_of, parse_rakuten_csv_bytes


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


def test_fx_classification_does_not_treat_em_fund_as_usd():
    em = classify_fx_exposure("投資信託", "", "新興国株式インデックス")
    assert em["currency"] == "EM_BASKET"
    assert em["fx_beta_usdjpy"] is None
    assert em["classification_status"] == "lookthrough_required"
    vti = classify_fx_exposure("投資信託", "", "楽天・全米株式インデックス・ファンド（VTI）")
    assert vti["currency"] == "USD"
    assert vti["fx_beta_usdjpy"] == 1.0
    assert vti["classification_status"] == "name_rule_inferred"
    hedged = classify_fx_exposure("投資信託", "", "米国債券 為替ヘッジあり")
    assert hedged["currency"] == "HEDGED"
    assert hedged["fx_beta_usdjpy"] == 0.0
    unknown = classify_fx_exposure("投資信託", "ABC", "判定不能ファンド")
    assert unknown["currency"] == "UNKNOWN"
    assert unknown["fx_beta_usdjpy"] is None


def test_funds_without_security_codes_are_retained():
    text = '''種別,銘柄コード・ティッカー,銘柄,口座,保有数量,平均取得価額,現在値,時価評価額[円]
投資信託,,楽天・全米株式インデックス・ファンド（VTI）,NISA,100,10000,15000,"1,500,000"
投資信託,,新興国株式インデックス,特定,100,10000,12000,"1,200,000"
外貨預り金,,米ドル,特定,1000,150,159,"159,000"
'''
    r = parse_rakuten_csv_bytes(text.encode("utf-8"))
    assert r.rows_kept == 3
    assert r.portfolio["ticker"].tolist() == ["", "", ""]
    assert r.portfolio["currency"].tolist() == ["USD", "EM_BASKET", "USD"]
    assert r.portfolio["holding_id"].nunique() == 3


def test_source_timestamp_prefers_export_filename_over_drive_reupload_time():
    value, method = infer_portfolio_source_as_of(
        "assetbalance(all)_20260819_093331.csv", "2026-08-26T09:00:00Z"
    )
    assert value == "2026-08-19T09:33:31+09:00"
    assert method == "filename_embedded_export_time"
