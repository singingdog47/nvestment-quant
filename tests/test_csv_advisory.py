import json
from datetime import datetime, timezone

import pytest

from src.csv_advisory import build_csv_advisory, DECLARATION_NAME
from src.run_portfolio_risk import _build_latest_account_inputs

NOW = datetime(2026, 1, 5, 4, 30, tzinfo=timezone.utc)
STAMP = "2026-01-05T13:00:00+09:00"


def inputs():
    return {"inputs": {"account_summary": {
        "total_assets_jpy": 1500, "invested_assets_jpy": 1000,
        "deposits_total_jpy": 400, "cash_deposit_jpy": 300,
        "foreign_cash_jpy": 0, "margin_collateral_jpy": 100,
        "fx_margin_net_assets_jpy": 100, "rakuten_bank_jpy": 700,
        "source_as_of": STAMP,
    }}}


def declaration(tmp_path, stamp=STAMP):
    p = tmp_path / DECLARATION_NAME
    p.write_text(json.dumps({"source": "user_statement", "scope": "all_open_orders",
                             "count": 0, "observed_at": stamp}))
    return [(p, {"name": p.name})]


def test_csv_and_zero_statement_do_not_require_pdf(tmp_path):
    r = build_csv_advisory(inputs(), declaration(tmp_path), now=NOW, reserve_jpy=200)
    assert r["capital_planning_ready"]
    assert r["cash_and_bank_jpy"] == 1000
    assert r["planning_cash_after_reserve_jpy"] == 800
    assert not r["execution_ready"] and not r["orders"]["broker_verified"]


@pytest.mark.parametrize("stamp", ["2026-01-04T13:00:00+09:00", "2026-01-05T14:00:00+09:00", "2026-01-05T13:00:00"])
def test_old_future_or_naive_statement_not_reused(tmp_path, stamp):
    r = build_csv_advisory(inputs(), declaration(tmp_path, stamp), now=NOW)
    assert r["analysis_ready"] and not r["capital_planning_ready"]
    assert r["orders"]["count"] is None


def test_missing_bank_and_reconciliation_failure_do_not_guess(tmp_path):
    data = inputs()
    del data["inputs"]["account_summary"]["rakuten_bank_jpy"]
    assert not build_csv_advisory(data, now=NOW)["analysis_ready"]
    data = inputs()
    data["inputs"]["account_summary"]["total_assets_jpy"] = 9999
    assert not build_csv_advisory(data, now=NOW)["analysis_ready"]


def test_current_pdf_disagreement_blocks_cash_plan(tmp_path):
    data = inputs()
    data["inputs"]["buying_power"] = {"source_as_of": STAMP, "cash_buying_power_jpy": 900}
    r = build_csv_advisory(data, declaration(tmp_path), now=NOW)
    assert not r["capital_planning_ready"]
    assert r["broker_buying_power_comparison"] == "DIFFERENT_REQUIRES_REVIEW"


def test_current_open_order_cannot_be_overwritten(tmp_path):
    data = inputs()
    data["order_documents"] = {"domestic": {"source_as_of": STAMP, "items": [{"status": "受付済"}]}}
    r = build_csv_advisory(data, declaration(tmp_path), now=NOW)
    assert not r["capital_planning_ready"] and r["orders"]["count"] is None


def test_both_order_document_scopes_survive_selection(tmp_path, monkeypatch):
    import src.run_portfolio_risk as mod
    def fail(*args):
        raise ValueError("unrelated document")
    monkeypatch.setattr(mod, "parse_account_summary_bytes", fail)
    monkeypatch.setattr(mod, "parse_buying_power_pdf", fail)
    monkeypatch.setattr(mod, "parse_orders_file", lambda p: {
        "scope": p.stem, "source_as_of": STAMP, "status": "partial", "items": None})
    files = []
    for name in ("domestic", "fund"):
        p = tmp_path / (name + ".pdf")
        p.write_bytes(b"test")
        files.append((p, {"name": p.name}))
    for sequence in (files, files[::-1]):
        r = _build_latest_account_inputs(tmp_path, sequence)
        assert set(r["order_documents"]) == {"domestic", "fund"}
