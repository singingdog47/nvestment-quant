from __future__ import annotations

from datetime import datetime, timezone
import json
import sys
import types

import pandas as pd

from company_intel.snapshot import _yf_fallback
from supply_demand import compute_supply_demand, run, update_history


def _config() -> dict:
    return {
        "version": "1.0.0",
        "thresholds": {
            "tight_free_float_ratio": 0.30,
            "high_average_float_turnover_ratio": 0.02,
            "crowded_short_percent_float": 0.10,
            "high_days_to_cover": 5.0,
            "volume_expansion_ratio": 1.50,
            "material_daily_move": 0.02,
        },
        "governance": {
            "alters_security_ranking": False,
            "alters_fundamental_score": False,
            "alters_investment_thesis": False,
            "missing_value_policy": "preserve_missing_no_imputation",
        },
    }


def _generated() -> datetime:
    return datetime(2026, 9, 8, 8, 0, tzinfo=timezone.utc)


def test_float_turnover_and_short_crowding_are_context_not_score() -> None:
    snapshot = pd.DataFrame(
        [
            {
                "market": "US",
                "code": "AAA",
                "ticker": "AAA",
                "name": "Example",
                "source": "watchlist",
                "fetched_at": "2026-09-08T07:30:00+00:00",
                "yf_shares_outstanding": 1_000_000,
                "yf_float_shares": 200_000,
                "yf_average_volume": 10_000,
                "yf_regular_market_volume": 30_000,
                "yf_market_cap": 10_000_000,
                "yf_price": 10,
                "yf_shares_short": 30_000,
                "yf_shares_short_prior_month": 20_000,
                "yf_short_percent_float": 0.15,
                "yf_short_ratio_days": 6.0,
                "yf_regular_market_change_pct": 3.0,
            }
        ]
    )

    latest, summary = compute_supply_demand(snapshot, _config(), generated_at=_generated())
    row = latest.iloc[0]

    assert row["data_status"] == "ok"
    assert row["free_float_ratio"] == 0.20
    assert row["avg_daily_float_turnover_ratio"] == 0.05
    assert row["current_volume_ratio_30d"] == 3.0
    assert row["daily_change_pct"] == 0.03
    assert row["one_day_capacity_at_participation_rate"] == 10_000
    for flag in (
        "TIGHT_FLOAT",
        "HIGH_FLOAT_TURNOVER",
        "SHORT_CROWDING",
        "SHORT_INTEREST_RISING",
        "VOLUME_EXPANSION",
        "PRICE_UP_ON_VOLUME_EXPANSION",
        "POTENTIAL_SHORT_SQUEEZE_CONTEXT",
    ):
        assert flag in row["context_flags"]
    assert summary["governance"]["alters_security_ranking"] is False
    assert summary["governance"]["alters_fundamental_score"] is False
    assert summary["governance"]["alters_investment_thesis"] is False


def test_missing_free_float_stays_missing_without_market_cap_inference() -> None:
    snapshot = pd.DataFrame(
        [
            {
                "market": "JP",
                "code": "6965",
                "ticker": "6965.T",
                "name": "Hamamatsu Photonics",
                "source": "watchlist",
                "market_cap": 600_000_000_000,
                "price": 1800,
                "avg_volume_30d": 1_000_000,
                "volume": 2_000_000,
            }
        ]
    )

    latest, summary = compute_supply_demand(snapshot, _config(), generated_at=_generated())
    row = latest.iloc[0]

    assert row["data_status"] == "partial"
    assert pd.isna(row["free_float_ratio"])
    assert pd.isna(row["free_float_shares"])
    assert pd.isna(row["avg_daily_float_turnover_ratio"])
    assert summary["coverage"]["free_float_ratio"] == 0.0
    assert summary["coverage"]["current_vs_average_volume"] == 1.0


def test_dated_manual_primary_value_overrides_secondary_observation() -> None:
    snapshot = pd.DataFrame(
        [
            {
                "market": "JP",
                "code": "6965",
                "ticker": "6965.T",
                "name": "Hamamatsu Photonics",
                "source": "watchlist",
                "fetched_at": "2026-09-08T07:30:00+00:00",
                "yf_shares_outstanding": 1000,
                "yf_float_shares": 800,
                "yf_average_volume": 50,
            }
        ]
    )
    manual = pd.DataFrame(
        [
            {
                "market": "JP",
                "code": "6965",
                "ticker": "6965.T",
                "as_of_date": "2026-09-01",
                "source_name": "Company filing",
                "source_tier": "primary",
                "source_url": "https://example.com/company-filing",
                "free_float_ratio": 0.25,
            }
        ]
    )

    latest, _ = compute_supply_demand(snapshot, _config(), manual, _generated())
    row = latest.iloc[0]

    assert row["free_float_ratio"] == 0.25
    assert row["free_float_source"] == "Company filing"
    assert row["free_float_source_tier"] == "primary"
    assert row["source_url"] == "https://example.com/company-filing"
    assert row["source_retrieved_at"] == "2026-09-01"
    assert row["confidence"] == 0.80
    assert "FREE_FLOAT_SOURCE_CONFLICT" in row["data_quality_flags"]


def test_invalid_float_ratio_is_rejected_not_clipped() -> None:
    snapshot = pd.DataFrame(
        [{"market": "US", "code": "BAD", "ticker": "BAD", "avg_volume_30d": 1000}]
    )
    manual = pd.DataFrame(
        [{"market": "US", "code": "BAD", "ticker": "BAD", "as_of_date": "2026-09-08", "free_float_ratio": 150}]
    )

    latest, _ = compute_supply_demand(snapshot, _config(), manual, _generated())
    row = latest.iloc[0]

    assert pd.isna(row["free_float_ratio"])
    assert "INVALID_FREE_FLOAT_RATIO" in row["data_quality_flags"]
    assert row["data_status"] == "partial"


def test_stale_manual_short_data_is_ignored_without_carry_forward() -> None:
    snapshot = pd.DataFrame(
        [
            {
                "market": "US",
                "code": "AAA",
                "ticker": "AAA",
                "yf_float_shares": 500,
                "yf_shares_outstanding": 1000,
                "yf_average_volume": 20,
            }
        ]
    )
    manual = pd.DataFrame(
        [
            {
                "market": "US",
                "code": "AAA",
                "ticker": "AAA",
                "as_of_date": "2026-01-01",
                "source_name": "Old filing",
                "source_tier": "primary",
                "shares_short": 300,
            }
        ]
    )

    latest, _ = compute_supply_demand(snapshot, _config(), manual, _generated())
    row = latest.iloc[0]

    assert pd.isna(row["shares_short"])
    assert pd.isna(row["short_percent_float"])
    assert "STALE_MANUAL_SHORT_DATA" in row["data_quality_flags"]


def test_history_replaces_same_day_snapshot_and_keeps_next_day(tmp_path) -> None:
    history_path = tmp_path / "history.csv"
    base = pd.DataFrame(
        [{"market": "US", "code": "AAA", "ticker": "AAA", "yf_float_shares": 500, "yf_shares_outstanding": 1000, "yf_average_volume": 20}]
    )
    day_one, _ = compute_supply_demand(base, _config(), generated_at=_generated())
    update_history(day_one, history_path, observed_date="2026-09-08")
    changed = base.copy()
    changed.loc[0, "yf_float_shares"] = 400
    same_day, _ = compute_supply_demand(changed, _config(), generated_at=_generated())
    update_history(same_day, history_path, observed_date="2026-09-08")

    day_two_time = datetime(2026, 9, 9, 8, 0, tzinfo=timezone.utc)
    day_two, _ = compute_supply_demand(changed, _config(), generated_at=day_two_time)
    history = update_history(day_two, history_path, observed_date="2026-09-09")

    assert len(history) == 2
    first = history.loc[history["observed_date"] == "2026-09-08"].iloc[0]
    assert float(first["free_float_ratio"]) == 0.4


def test_yfinance_supply_fields_do_not_inflate_fundamental_coverage(monkeypatch) -> None:
    class FakeTicker:
        def __init__(self, ticker: str):
            self.ticker = ticker

        @property
        def info(self) -> dict:
            return {"floatShares": 500, "sharesOutstanding": 1000}

    monkeypatch.setitem(sys.modules, "yfinance", types.SimpleNamespace(Ticker=FakeTicker))
    frame = pd.DataFrame(
        [
            {
                "ticker": "AAA",
                "fundamental_status": "ok",
                "secondary_snapshot_status": "missing",
                "secondary_snapshot_source": "",
                "supply_demand_source_status": "missing",
                "supply_demand_source": "",
            }
        ]
    )

    result, health = _yf_fallback(frame, max_targets=1)

    assert health.status == "ok"
    assert result.loc[0, "supply_demand_source_status"] == "ok"
    assert result.loc[0, "secondary_snapshot_status"] == "missing"
    assert result.loc[0, "fundamental_status"] == "ok"


def test_run_writes_outputs_and_embeds_public_decision_context(tmp_path) -> None:
    (tmp_path / "config").mkdir()
    (tmp_path / "data/intelligence").mkdir(parents=True)
    config = _config()
    config.update(
        {
            "inputs": {
                "company_snapshot": "data/intelligence/company_snapshot_latest.csv",
                "manual_override": "data/supply_demand/supply_demand_manual_latest.csv",
            },
            "outputs": {
                "directory": "data/supply_demand",
                "latest_csv": "supply_demand_latest.csv",
                "summary_json": "supply_demand_summary_latest.json",
                "summary_markdown": "supply_demand_summary_latest.md",
                "history_csv": "supply_demand_history.csv",
                "history_retention_days": 400,
            },
        }
    )
    (tmp_path / "config/supply_demand_v1.json").write_text(
        json.dumps(config), encoding="utf-8"
    )
    pd.DataFrame(
        [
            {
                "market": "US",
                "code": "AAA",
                "ticker": "AAA",
                "name": "Example",
                "source": "watchlist",
                "yf_shares_outstanding": 1000,
                "yf_float_shares": 500,
                "yf_average_volume": 20,
            }
        ]
    ).to_csv(tmp_path / "data/intelligence/company_snapshot_latest.csv", index=False)
    for path in (
        tmp_path / "data/decision_context_latest.json",
        tmp_path / "data/intelligence/decision_context_latest.json",
    ):
        path.write_text(json.dumps({"quality": {"actionable": True}}), encoding="utf-8")

    latest_path, summary_path, markdown_path = run(tmp_path)

    assert latest_path.exists()
    assert summary_path.exists()
    assert markdown_path.exists()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["input_health"]["company_snapshot"]["status"] == "ok"
    assert summary["input_health"]["manual_override"]["status"] == "not_provided"
    context = json.loads(
        (tmp_path / "data/decision_context_latest.json").read_text(encoding="utf-8")
    )
    assert context["supply_demand_context"]["target_count"] == 1
    assert "quantity" not in pd.read_csv(latest_path).columns
