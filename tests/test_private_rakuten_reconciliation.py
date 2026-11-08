"""Synthetic reconciliation checks for the Rakuten account summary structure."""
from private_account_import import parse_account_summary_bytes, reconcile_account_components



def test_historical_reconciliation_does_not_authorize_cash():
    raw = ('資産合計,2000\n保有商品の評価額合計,1000\n'
           '預り金合計,800\n預り金,300\n外貨預り金,100\n'
           '国内株式信用保証金,400\nFX証拠金（純資産）,200\n').encode("cp932")
    result = reconcile_account_components(parse_account_summary_bytes(raw))
    assert result["status"] == "RECONCILED_HISTORICAL"
    assert result["asset_residual_jpy"] == 0
    assert result["deposit_residual_jpy"] == 0
    assert result["deployable_cash_jpy"] is None
    assert result["execution_ready"] is False


def test_missing_collateral_cannot_pass():
    raw = ('資産合計,2000\n保有商品の評価額合計,1000\n'
           '預り金合計,800\n預り金,300\n外貨預り金,100\n'
           'FX証拠金（純資産）,200\n').encode("cp932")
    assert reconcile_account_components(parse_account_summary_bytes(raw))["status"] == "INCOMPLETE"


def test_nonzero_reconciliation_difference_blocks():
    raw = ('資産合計,2001\n保有商品の評価額合計,1000\n'
           '預り金合計,800\n預り金,300\n外貨預り金,100\n'
           '国内株式信用保証金,400\nFX証拠金（純資産）,200\n').encode("cp932")
    result = reconcile_account_components(parse_account_summary_bytes(raw))
    assert result["status"] == "MISMATCH"
    assert result["asset_residual_jpy"] == 1
