from import_newer_verified_snapshot import import_newer_verified_snapshot
from investment_state import build_investment_state


def test_private_history_integrates_without_execution_authorization(tmp_path):
    ledger = tmp_path / "private.jsonl"
    base = {
        "verification_status": "verified",
        "evidence_ref": "private:synthetic-export",
        "quality": {"source_verified": True, "coherence_verified": True,
                    "source_scope": "bank"},
        "facts": [{"key": "bank:balance", "value": 100, "scope": "bank"}],
    }
    import_newer_verified_snapshot(
        {**base, "observed_at": "2099-01-01T10:00:00+09:00"}, str(ledger)
    )
    import_newer_verified_snapshot(
        {**base, "observed_at": "2099-01-02T10:00:00+09:00",
         "evidence_ref": "private:synthetic-export-day-two",
         "facts": [{"key": "bank:balance", "value": 120, "scope": "bank"}]}, str(ledger)
    )
    state = build_investment_state(
        {"status": "ok", "inputs": {"buying_power": {"cash_buying_power_jpy": 999999},
                                  "orders": {"data_status": "ok", "items": []}}},
        {"source_as_of": "2099-01-02T10:00:00+09:00"}, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
        verified_ledger_path=ledger,
        now="2099-01-02T12:00:00+09:00",
    )
    assert state["verified_asset_history"]["facts"]["bank:balance"]["value"] == 120
    assert state["verified_asset_history"]["status"] == "VERIFIED_HISTORY"
    assert state["capital"]["deployable_cash_jpy"] is None
    assert state["execution_ready"] is False


def test_empty_ledger_never_claims_verified_history(tmp_path):
    state = build_investment_state(
        {"status": "missing", "inputs": {}}, {}, {},
        decision_context_path=tmp_path / "missing.json",
        watchlist_path=tmp_path / "missing.csv",
        verified_ledger_path=tmp_path / "absent.jsonl",
        now="2099-01-02T12:00:00+09:00",
    )
    assert state["verified_asset_history"]["status"] == "PARTIAL"
    assert state["execution_ready"] is False
