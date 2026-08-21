from company_intel.classify import classify_event

def test_earnings():
    assert classify_event("2026年3月期 決算短信")[0] == "earnings"

def test_guidance():
    assert classify_event("業績予想の上方修正に関するお知らせ")[0] == "guidance"

def test_regulatory():
    assert classify_event("情報漏えいに関するお知らせ")[0] == "regulatory"
