from src.advisory_continuity import classify_advisory_continuity as decide


def test_partial_coverage_keeps_advisory_open():
    result = decide(verified_scopes=["account_summary", "orders_domestic_cash"],
                    missing_scopes=["orders_foreign_equities"],
                    conflicting_scopes=[], stale_scopes=[])
    assert result["analysis_allowed"] is True
    assert result["analysis_mode"] == "CONDITIONAL_FORECAST"
    assert result["execution_ready"] is False
    assert result["deployable_cash_jpy"] is None


def test_conflict_is_isolated_without_silent_reconciliation():
    result = decide(verified_scopes=["account_summary", "buying_power"],
                    missing_scopes=[], conflicting_scopes=["buying_power"],
                    stale_scopes=[])
    assert result["verified_scopes"] == ["account_summary"]
    assert result["conflicting_scopes_excluded"] == ["buying_power"]
    assert result["analysis_mode"] == "PARTIAL_WITH_CONFLICTS"
    assert result["confidence_tier"] == "LOW"


def test_no_verified_data_still_allows_scenario_only():
    result = decide(verified_scopes=[], missing_scopes=["account_summary"],
                    conflicting_scopes=[], stale_scopes=[])
    assert result["analysis_mode"] == "SCENARIO_ONLY"
    assert result["assumptions_required"] is True
    assert result["trade_execution_authorized"] is False


def test_duplicates_do_not_raise_confidence():
    result = decide(verified_scopes=["account_summary"],
                    missing_scopes=["orders_foreign_equities"],
                    conflicting_scopes=[], stale_scopes=[],
                    duplicate_scopes=["account_summary"])
    assert result["analysis_mode"] == "CONDITIONAL_FORECAST"
    assert result["confidence_tier"] == "MEDIUM"
