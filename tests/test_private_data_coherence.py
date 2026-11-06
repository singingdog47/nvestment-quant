from datetime import datetime, timezone

from src.private_data_coherence import classify_private_inputs

NOW = datetime(2026, 11, 6, 12, 0, tzinfo=timezone.utc)
PF = {"source_as_of": "2026-11-06T15:00:00+09:00", "source_as_of_method": "filename_embedded_export_time"}


def inputs(as_of="2026-11-06T15:00:00+09:00", method="filename_embedded_export_time"):
    return {"inputs": {
        kind: {"source_as_of": as_of, "source_as_of_method": method, "data_status": "ok"}
        for kind in ("account_summary", "orders", "buying_power")
    }}


def test_consistent_current_inputs_verified():
    result = classify_private_inputs(PF, inputs(), now=NOW)
    assert result["status"] == "VERIFIED"
    assert result["decision_safe"] is True


def test_old_orders_are_not_verified():
    x = inputs()
    x["inputs"]["orders"]["source_as_of"] = "2026-11-04T15:00:00+09:00"
    result = classify_private_inputs(PF, x, now=NOW)
    assert result["status"] == "PARTIAL"
    assert "PORTFOLIO_TIME_MISMATCH" in result["inputs"]["orders"]["reasons"]


def test_stale_buying_power_is_not_verified():
    x = inputs()
    x["inputs"]["buying_power"]["data_status"] = "stale"
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["buying_power"]["status"] == "UNVERIFIED"


def test_inferred_or_upload_time_not_trusted():
    x = inputs(method="drive_modified_time_fallback")
    assert classify_private_inputs(PF, x, now=NOW)["decision_safe"] is False


def test_unknown_portfolio_date_blocks_all_decisions():
    pf = {"source_as_of": None, "source_as_of_method": "missing"}
    result = classify_private_inputs(pf, inputs(), now=NOW)
    assert result["status"] == "UNVERIFIED"
    assert "PORTFOLIO_TIMESTAMP_UNVERIFIED" in result["portfolio_reasons"]


def test_missing_input_partial():
    x = inputs()
    del x["inputs"]["orders"]
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["orders"]["status"] == "UNVERIFIED"


def test_future_timestamp_is_not_verified():
    x = inputs("2026-11-07T15:00:00+09:00")
    assert classify_private_inputs(PF, x, now=NOW)["decision_safe"] is False


def test_yearless_pdf_date_requires_verification():
    x = inputs(method="pdf_embedded_timestamp_inferred_year")
    # The year is inferred and cannot be considered brokerage-verified.
    assert classify_private_inputs(PF, x, now=NOW)["inputs"]["buying_power"]["status"] == "UNVERIFIED"
