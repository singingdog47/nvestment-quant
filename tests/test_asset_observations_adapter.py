import pytest
from asset_observations_adapter import import_asset_observations
from verified_facts_ledger import read_verified_facts, FactConflict


def _payload(asset_class, metric, value, unit, currency=None):
    return {"source": {"verified": True, "coherence_verified": True,
            "observed_at": "2099-01-01T10:00:00+09:00",
            "evidence_ref": "private:synthetic-fixture", "scope": "single-account",
            "asset_class": asset_class, "account_ref": "demo-account",
            "coverage": "partial"},
            "observations": [{"entity_ref": "demo-position", "metric": metric,
                              "value": value, "unit": unit, "currency": currency}]}


@pytest.mark.parametrize("asset_class,metric,value,unit,currency", [
    ("domestic_equity", "quantity", 10, "shares", None),
    ("foreign_equity", "market_value", 200, "currency", "USD"),
    ("mutual_fund", "order_status", "filled", "status", None),
    ("bank", "balance", 5000, "currency", "JPY"),
    ("fx", "position_quantity", -1000, "currency", "USD"),
    ("crypto", "quantity", 0.02, "BTC", None),
    ("other_asset", "appraised_value", 800, "currency", "JPY"),
])
def test_generic_asset_classes(tmp_path, asset_class, metric, value, unit, currency):
    p = tmp_path / "facts.jsonl"
    import_asset_observations(_payload(asset_class, metric, value, unit, currency), str(p))
    record = next(iter(read_verified_facts(p).values()))
    assert record["value"]["amount"] == value
    assert record["value"]["coverage"] == "partial"


def test_conflicting_asset_fact_cannot_be_overwritten(tmp_path):
    p = tmp_path / "facts.jsonl"
    import_asset_observations(_payload("crypto", "quantity", 1, "BTC"), str(p))
    with pytest.raises(FactConflict):
        import_asset_observations(_payload("crypto", "quantity", 2, "BTC"), str(p))


def test_unverified_source_is_rejected(tmp_path):
    p = tmp_path / "facts.jsonl"
    payload = _payload("bank", "balance", 100, "currency", "JPY")
    payload["source"]["coherence_verified"] = False
    with pytest.raises(ValueError):
        import_asset_observations(payload, str(p))
    assert not p.exists()
