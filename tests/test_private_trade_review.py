import json
from datetime import datetime

import pytest

from src.private_trade_review import append_rows, build_review, rakuten_csv_rows, read_rows

STAMP = "2026-01-16T16:00:00+09:00"
NOW = "2026-01-16T20:00:00+09:00"


def order(**changes):
    return dict({
        "schema_version": 1, "asset": "JP_CASH_EQUITY", "broker": "RAKUTEN",
        "account_alias": "example", "account_type": "特定", "order_id": "100",
        "order_at": "2026-01-16T14:00:00+09:00", "symbol": "1234.T", "side": "SELL",
        "status": "FILLED", "quantity": 100, "filled_quantity": 100,
        "fill_price_jpy": "1000.2", "fill_value_jpy": "100020",
        "execution_date": "2026-01-16", "limit_price_jpy": "1000",
        "observed_at": STAMP, "recorded_at": NOW, "evidence_ref": "example:source",
        "decision": {"reason": "example", "evidence_ref": "example:advice",
                     "timing_basis": "prior_message"},
    }, **changes)


def test_readback_review_keeps_an_open_buy_out_of_sale_comparison():
    raw = append_rows(b"", [order(), order(order_id="101", side="BUY", status="OPEN",
                                           filled_quantity=0, fill_price_jpy=None,
                                           fill_value_jpy=None, execution_date=None)])
    report = build_review(raw, datetime.fromisoformat(NOW), lambda *_: {
        "status": "AVAILABLE", "close_jpy": "980", "evidence_ref": "example:close"})
    sale, pending = report["orders"]
    assert sale["review"][0]["sale_minus_hold_jpy"] == "2020"
    assert sale["review"][1]["session"] == "2026-01-19"
    assert sale["review"][1]["status"] == "PENDING_SESSION"
    assert pending["review"] == [] and pending["filled_quantity"] == 0
    assert not report["account_wide_coverage"]
    assert build_review(raw, datetime.fromisoformat(STAMP))["orders"] == []


def test_append_is_idempotent_and_rejects_conflicts_or_regressions():
    raw = append_rows(b"", [order()])
    assert append_rows(raw, [order(recorded_at="2026-01-16T21:00:00+09:00")]) == raw
    with pytest.raises(ValueError, match="conflicting"):
        append_rows(raw, [order(limit_price_jpy="1001")])
    with pytest.raises(ValueError, match="regressed"):
        append_rows(raw, [order(status="OPEN", filled_quantity=0, fill_price_jpy=None,
                                fill_value_jpy=None, execution_date=None,
                                observed_at="2026-01-16T17:00:00+09:00")])
    assert len(read_rows(raw)) == 1


@pytest.mark.parametrize("changes", [
    {"fill_price_jpy": "NaN"}, {"fill_value_jpy": "123"},
    {"execution_date": "2026-01-17"}, {"status": "OPEN"},
    {"observed_at": "2026-01-16T14:20:00"}, {"quantity": True},
])
def test_invalid_rows_are_never_saved(changes):
    with pytest.raises(ValueError):
        append_rows(b"", [order(**changes)])


def test_partial_cancel_preserves_executed_quantity_and_no_fake_dates():
    partial = order(status="PARTIALLY_FILLED", filled_quantity=50, fill_value_jpy="50010",
                    execution_date=None)
    cancel = dict(partial, status="CANCELLED", observed_at="2026-01-16T18:00:00+09:00")
    raw = append_rows(b"", [partial, cancel])
    row = build_review(raw, datetime.fromisoformat(NOW))["orders"][0]
    assert row["filled_quantity"] == 50
    assert row["review_status"] == "EXECUTION_DATE_UNVERIFIED"


def test_expiry_is_not_a_verified_terminal_state_and_missing_price_stays_missing():
    pending = order(order_id="101", side="BUY", status="OPEN", filled_quantity=0,
                    fill_price_jpy=None, fill_value_jpy=None, execution_date=None, good_until="2026-01-16")
    sale, buy = build_review(append_rows(b"", [order(), pending]),
                             datetime.fromisoformat("2026-01-17T20:00:00+09:00"))["orders"]
    assert sale["review"][0]["status"] == "NO_VERIFIED_CLOSE"
    assert buy["status"] == "OPEN"
    assert buy["current_state"] == "LAST_OBSERVATION_EXPIRED_CHECK_BROKER"


def test_execution_day_close_is_used_only_if_available_after_session():
    mark = {"close_jpy": "1010", "observed_at": STAMP, "evidence_ref": "example:mark"}
    raw = append_rows(b"", [order(execution_day_close=mark)])
    assert build_review(raw, datetime.fromisoformat(NOW))["orders"][0]["review"][0]["sale_minus_hold_jpy"] == "-980"
    mark["observed_at"] = "2026-01-16T14:00:00+09:00"
    with pytest.raises(ValueError, match="not yet known"):
        append_rows(b"", [order(execution_day_close=mark)])


def test_rakuten_export_uses_executed_price_and_does_not_infer_execution_date():
    csv = ("注文番号,状況,銘柄コード,市場,取引,売買,口座,注文日時,注文期限,"
           "注文数量[株/口],約定数量[株/口],注文単価[円],約定単価[円],約定代金[円]\n"
           '100,約定,1234,東証(SOR),現物,売付,特定,01/16 14:00:00,2026/01/16,100,100,1000,1000.2,"100,020"\n'
           "101,執行中,2345,東証(SOR),現物,買付,特定,01/16 14:02:00,2026/01/23,100,0,1500,-,0\n")
    rows = rakuten_csv_rows(csv.encode("cp932"), observed_at=datetime.fromisoformat(STAMP),
                           recorded_at=datetime.fromisoformat(NOW), account_alias="example",
                           evidence_ref="example:broker")
    assert len(read_rows(append_rows(b"", rows))) == 2
    assert rows[0]["fill_price_jpy"] != rows[0]["limit_price_jpy"]
    assert rows[0]["execution_date"] is None
    assert rows[1]["fill_value_jpy"] is None
    with pytest.raises(ValueError, match="lacks a year"):
        rakuten_csv_rows(csv.replace("01/16 14:00:00", "01/15 14:00:00").encode("cp932"),
                         observed_at=datetime.fromisoformat(STAMP), recorded_at=datetime.fromisoformat(NOW),
                         account_alias="example", evidence_ref="example:broker")


def test_import_failure_leaves_original_bytes(tmp_path, monkeypatch, capsys):
    from src.private_trade_review import main
    ledger = tmp_path / "ledger.jsonl"
    ledger.write_bytes(append_rows(b"", [order()]))
    original = ledger.read_bytes()
    source = tmp_path / "bad.json"
    source.write_text(json.dumps([order(status="OPEN")]))
    monkeypatch.setattr("sys.argv", ["private_trade_review", "--ledger", str(ledger),
                                     "--append", str(source), "--as-of", NOW])
    with pytest.raises(SystemExit) as caught:
        main()
    assert caught.value.code == 1
    assert ledger.read_bytes() == original
    assert "TRADE_IMPORT_REJECTED" in capsys.readouterr().out
