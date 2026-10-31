"""Regression tests for isolated 5m paper fork; no network/real brokerage use."""
import json
from datetime import date
from pathlib import Path

import pytest
import shadow_challenger2 as c2


# Pinned at fork creation (commit 94cafd5934bcd204fc828027357aee3c7fcd19d6).
# Do not use the live, evolving paper state as a replay test fixture.
FORK_SEED_PATH = Path("tests/fixtures/challenger2_initial_fork_20261028.json")


def setup_fork(tmp_path, monkeypatch):
    src_cfg = json.loads(Path("config/shadow_challenger2_v1.json").read_text(encoding="utf-8"))
    src_state = json.loads(FORK_SEED_PATH.read_text(encoding="utf-8"))
    data = tmp_path / "data"
    dst = data / "shadow_challenger2"
    dst.mkdir(parents=True)
    (dst / "state.json").write_text(json.dumps(src_state), encoding="utf-8")
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps(src_cfg), encoding="utf-8")
    monkeypatch.setattr(c2, "DATA_ROOT", data)
    monkeypatch.setattr(c2, "OUT_DIR", dst)
    monkeypatch.setattr(c2, "CONFIG_FILE", cfg_path)
    return src_state, data, dst


def test_fork_initial_capital_and_live_accounting_without_rewriting_history():
    genesis = json.loads(FORK_SEED_PATH.read_text(encoding="utf-8"))
    state = json.loads(Path("data/shadow_challenger2/state.json").read_text(encoding="utf-8"))
    cfg = json.loads(Path("config/shadow_challenger2_v1.json").read_text(encoding="utf-8"))
    assert state["cohort"] == cfg["cohort"] == genesis["cohort"]
    assert state["mode"] == cfg["mode"] == "SHADOW_ONLY"
    assert state["initial_cash_jpy"] == genesis["initial_cash_jpy"] == cfg["initial_cash_jpy"] == 5_000_000
    # Genesis NAV was 5m, but live NAV must be allowed to move with paper P&L.
    assert genesis["nav_jpy"] == 5_000_000
    assert state["fork_metadata"] == genesis["fork_metadata"]
    assert state["capital_ledger"] == genesis["capital_ledger"]
    assert state["fork_metadata"]["source_nav_jpy"] == 992027.83
    assert state["fork_metadata"]["capital_topup_jpy"] == 4007972.17
    assert state["capital_ledger"][0]["counts_as_pnl"] is False
    assert state["capital_ledger"][0]["counts_as_trade"] is False
    inherited_fills = genesis["fork_metadata"]["pre_fork_executions"]
    inherited_trades = genesis["fork_metadata"]["pre_fork_trades"]
    assert len(genesis["execution_log"]) == inherited_fills == 2
    assert len(genesis["trades"]) == inherited_trades == 1
    assert state["execution_log"][:inherited_fills] == genesis["execution_log"]
    assert state["trades"][:inherited_trades] == genesis["trades"]
    assert all(fill.get("paper_only") is True and fill.get("source", "").startswith("verified_")
               for fill in state["execution_log"][inherited_fills:])
    assert state["last_run_date"] >= genesis["last_run_date"]
    assert state["peak_nav_jpy"] >= state["nav_jpy"]
    assert abs(state["cash_jpy"] + sum(p["qty"] * p["last_price"]
               for p in state["positions"].values()) - state["nav_jpy"]) < 0.01


def test_pinned_fork_seed_preserves_inherited_order_and_execution_provenance():
    genesis = json.loads(FORK_SEED_PATH.read_text(encoding="utf-8"))
    assert genesis["last_run_date"] == genesis["fork_metadata"]["source_snapshot_date"]
    assert genesis["positions"]["8789.T"]["qty"] == 600
    assert genesis["pending_buys"] == [{
        "symbol": "3932.T", "signal_date": "2026-10-28", "qty": 100,
        "theme": "Other", "signal_price": 1209, "max_notional": 200000
    }]
    assert len(genesis["execution_log"]) == 2
    assert len(genesis["trades"]) == 1
    assert abs(genesis["cash_jpy"] + sum(p["qty"] * p["last_price"]
               for p in genesis["positions"].values()) - genesis["nav_jpy"]) < 0.01


def test_does_not_mutate_original_challenger_or_count_inherited_fills(tmp_path, monkeypatch):
    _, data, dst = setup_fork(tmp_path, monkeypatch)
    old_dir = data / "shadow_challenger"
    old_dir.mkdir()
    source_marker = '{"locked":"original cohort"}\n'
    (old_dir / "state.json").write_text(source_marker, encoding="utf-8")

    # No verified bar for inherited pending buy: NO fake execution.
    bar = {"open": 153, "high": 154, "low": 151, "close": 153}
    result = c2.run(date(2026, 10, 29),
                    bar_source=lambda s, d: bar if s == "8789.T" else None)
    assert result["strategy"] == "CHALLENGER2"
    assert result["post_fork_verified_fills"] == 0
    assert result["fork"]["inherited_executions"] == 2
    assert result["pending_buys"] == 1
    assert result["nav_jpy"] == 5_000_600
    assert result["return_pct"] > 0  # Capital injection was normalized to the new opening NAV.
    assert (old_dir / "state.json").read_text() == source_marker
    again = c2.run(date(2026, 10, 29),
                   bar_source=lambda s, d: bar if s == "8789.T" else None)
    assert again["status"] == "ALREADY_PROCESSED"
    assert len(json.loads((dst / "state.json").read_text())["execution_log"]) == 2


def test_new_ohlc_fill_distinguished_from_pre_fork_history(tmp_path, monkeypatch):
    _, _, dst = setup_fork(tmp_path, monkeypatch)
    neutral = {"open": 152, "high": 153, "low": 151, "close": 152}
    c2.run(date(2026, 10, 29),
           bar_source=lambda s, d: neutral if s == "8789.T" else None)
    new_buy_bar = {"open": 1209, "high": 1220, "low": 1200, "close": 1215}
    result = c2.run(date(2026, 10, 30),
                    bar_source=lambda s, d: new_buy_bar if s == "3932.T" else
                    neutral if s == "8789.T" else None)
    assert result["post_fork_verified_fills"] == 1
    assert result["post_fork_verified_fill_log"][0]["date"] == "2026-10-30"
    assert result["post_fork_verified_fill_log"][0]["symbol"] == "3932.T"
    state = json.loads((dst / "state.json").read_text())
    assert len(state["execution_log"]) == 3
    assert result["monthly_goal"]["baseline_nav_jpy"] is None

    november = c2.run(date(2026, 11, 2),
                      bar_source=lambda s, d: new_buy_bar if s == "3932.T" else
                      neutral if s == "8789.T" else None)
    assert november["monthly_goal"]["baseline_nav_jpy"] == result["nav_jpy"]
    assert november["monthly_goal"]["return_target_pct"] == 3


def test_missing_fork_state_fails_closed(tmp_path, monkeypatch):
    _, _, dst = setup_fork(tmp_path, monkeypatch)
    (dst / "state.json").unlink()
    with pytest.raises(RuntimeError, match="audited fork"):
        c2.run(date(2026, 10, 29), bar_source=lambda s, d: None)


def test_risk_budget_is_conservative_and_not_a_gap_guarantee():
    cfg = json.loads(Path("config/shadow_challenger2_v1.json").read_text())
    max_notional = cfg["initial_cash_jpy"] * cfg["risk"]["max_position_pct"]
    ordinary_stop_and_fills = (cfg["risk"]["stop_loss_pct"] / 100 +
                                2 * cfg["execution"]["slippage_bps"] / 10000)
    assert cfg["risk"]["max_position_pct"] <= cfg["risk"]["requested_hard_position_ceiling_pct"]
    assert max_notional * ordinary_stop_and_fills <= (
        cfg["initial_cash_jpy"] * cfg["risk"]["planned_per_trade_loss_budget_pct"])
    assert cfg["governance"]["no_synthetic_fills"]
    assert cfg["governance"]["real_orders_forbidden"]
