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


def test_available_sources_missing_pdf_keeps_forecast():
    from src.advisory_continuity import assess_available_sources
    result = assess_available_sources({
        "account_summary": "verified",
        "buying_power": "verified",
        "orders_domestic_cash": "missing",
        "orders_mutual_funds": "duplicate_verified",
        "orders_foreign": "stale",
    })
    assert result["analysis_allowed"]
    assert result["analysis_mode"] == "CONDITIONAL_FORECAST"
    assert result["verified_source_count"] == 3
    assert result["execution_ready"] is False
    assert result["forecast_is_conditional"] is True


def test_available_sources_conflict_isolated():
    from src.advisory_continuity import assess_available_sources
    result = assess_available_sources({
        "account_summary": "verified", "buying_power": "conflict",
    })
    assert result["analysis_mode"] == "PARTIAL_WITH_CONFLICTS"
    assert "buying_power" not in result["verified_scopes"]


def test_available_sources_unknown_status_rejected():
    import pytest
    from src.advisory_continuity import assess_available_sources
    with pytest.raises(ValueError, match="Unknown source"):
        assess_available_sources({"account_summary": "probably_verified"})
