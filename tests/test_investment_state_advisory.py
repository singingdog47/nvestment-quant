from src.investment_state import build_investment_state


def test_partial_inputs_produce_conditional_advisory_without_execution(tmp_path):
    state = build_investment_state(
        account_inputs={"status": "PARTIAL", "inputs": {
            "account_summary": {
                "source_as_of": "2026-11-06T22:51:14+09:00",
                "source_as_of_method": "filename_embedded_export_time",
                "total_assets_jpy": 19643918,
            },
            "buying_power": {},
        }},
        portfolio_manifest={"source_as_of": "2026-11-06T22:51:14+09:00"},
        policy_payload={"status": "active"},
        decision_context_path=tmp_path / "absent.json",
        watchlist_path=tmp_path / "absent.csv",
    )
    advisory = state["advisory_continuity"]
    assert advisory["analysis_allowed"] is True
    assert advisory["analysis_mode"] == "CONDITIONAL_FORECAST"
    assert advisory["recommendations_are_hypothetical"] is True
    assert "buying_power" in advisory["missing_scopes"]
    assert state["portfolio"]["total_assets_jpy"] == 19643918
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["execution_ready"] is False
    assert "deployable_cash_not_verified" in state["execution_blockers"]


def test_conflicting_inputs_excluded_from_advisory(tmp_path):
    state = build_investment_state(
        account_inputs={"status": "PARTIAL", "inputs": {
            "account_summary": {
                "source_as_of": "2026-11-06T22:51:14+09:00",
                "source_as_of_method": "filename_embedded_export_time",
            },
            "buying_power": {"data_status": "conflict"},
        }},
        portfolio_manifest={},
        policy_payload={},
        decision_context_path=tmp_path / "none.json",
        watchlist_path=tmp_path / "none.csv",
    )
    assert state["advisory_continuity"]["analysis_mode"] == "PARTIAL_WITH_CONFLICTS"
    assert "buying_power" in state["advisory_continuity"]["conflicting_scopes_excluded"]
    assert state["execution_ready"] is False


def test_stale_account_values_are_scenario_only(tmp_path):
    state = build_investment_state(
        account_inputs={"status": "PARTIAL", "inputs": {
            "account_summary": {"data_status": "stale", "total_assets_jpy": 12345},
        }},
        portfolio_manifest={}, policy_payload={},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
    )
    assert state["portfolio"]["total_assets_jpy"] is None
    assert state["advisory_source_values"]["account_summary"]["total_assets_jpy"] == 12345
    assert state["advisory_continuity"]["analysis_mode"] == "SCENARIO_ONLY"
    assert state["execution_ready"] is False
