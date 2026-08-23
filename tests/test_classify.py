from company_intel.classify import classify_event, is_low_value_news


def test_earnings():
    assert classify_event("2026年3月期 決算短信")[0] == "earnings"


def test_guidance():
    assert classify_event("業績予想の上方修正に関するお知らせ")[0] == "guidance"


def test_regulatory():
    assert classify_event("情報漏えいに関するお知らせ")[0] == "regulatory"


def test_yahoo_quote_page_is_noise():
    assert is_low_value_news("ＫＤＤＩ(株)【9433】：株価・株式情報（夜間PTS含む） - Yahoo!ファイナンス")


def test_real_news_with_stock_price_word_is_not_noise():
    assert not is_low_value_news("KDDI、増益決算を受け株価上昇　通信事業が堅調 - Reuters")


def test_material_yahoo_article_is_not_filtered_only_by_publisher():
    assert not is_low_value_news("KDDIが業績予想を上方修正 - Yahoo!ファイナンス")
