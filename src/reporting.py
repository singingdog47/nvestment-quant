from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import SETTINGS


def add_daily_changes(current: pd.DataFrame, previous_path: Path) -> pd.DataFrame:
    result = current.copy()
    result["previous_market_rank"] = pd.NA
    result["rank_change"] = pd.NA
    result["daily_change"] = "new_entry"
    if previous_path.exists():
        previous = pd.read_csv(previous_path, usecols=lambda c: c in {"ticker", "market", "market_rank"})
        if {"ticker", "market", "market_rank"}.issubset(previous.columns):
            previous = previous.rename(columns={"market_rank": "previous_market_rank"})
            result = result.merge(previous, on=["ticker", "market"], how="left", suffixes=("", "_old"))
            if "previous_market_rank_old" in result:
                result["previous_market_rank"] = result["previous_market_rank_old"]
                result = result.drop(columns=["previous_market_rank_old"])
            result["rank_change"] = result["previous_market_rank"] - result["market_rank"]
            result["daily_change"] = "unchanged"
            result.loc[result["previous_market_rank"].isna(), "daily_change"] = "new_entry"
            result.loc[result["rank_change"].ge(SETTINGS.rank_alert_threshold), "daily_change"] = "rank_up"
            result.loc[result["rank_change"].le(-SETTINGS.rank_alert_threshold), "daily_change"] = "rank_down"
    return result


def select_diversified_candidates(final: pd.DataFrame) -> pd.DataFrame:
    selected = final[final["research_candidate"]].copy()
    market_count = max(1, selected["market"].nunique())
    per_market = max(1, SETTINGS.output_top_n // market_count)
    return (
        selected.sort_values(["market", "total_score"], ascending=[True, False])
        .groupby("market", group_keys=False)
        .head(per_market)
        .sort_values("total_score", ascending=False)
        .head(SETTINGS.output_top_n)
    )


def daily_report_markdown(final: pd.DataFrame, selected: pd.DataFrame, report: dict) -> str:
    lines = [
        "# Daily Quant Report",
        "",
        f"- Data retrieved (UTC): {report.get('data_retrieved_at_utc') or 'unavailable'}",
        "- Price basis: TradingView scanner close; exact exchange timestamp unavailable.",
        "- This report is for research. A high score is not a buy signal.",
        "",
        "## Concentration guard",
        "",
        f"- Maximum displayed research candidates per market for Financials or Shipping: {SETTINGS.max_per_theme}",
        "- Mortgage REITs are watch-only and excluded from the research-candidate list.",
        "",
        "## Theme distribution in unfiltered score leaders",
        "",
        "| Market | Theme | Names in top 20 |",
        "|---|---|---:|",
    ]
    leaders = final.sort_values(["market", "market_rank"]).groupby("market", group_keys=False).head(20)
    distribution = leaders.groupby(["market", "theme"]).size().reset_index(name="count")
    for row in distribution.itertuples(index=False):
        lines.append(f"| {row.market} | {row.theme} | {row.count} |")
    lines += ["", "## Research candidates", "", "| Market | Rank | Ticker | Name | Theme | Score | Daily change |", "|---|---:|---|---|---|---:|---|"]
    display = selected.sort_values(["market", "market_rank"]).groupby("market", group_keys=False).head(10)
    for row in display.itertuples(index=False):
        lines.append(
            f"| {row.market} | {int(row.market_rank)} | {row.ticker} | {row.name} | {row.theme} | {row.total_score:.1f} | {row.daily_change} |"
        )
    lines += [
        "",
        "## Required manual checks before an order",
        "",
        "1. Verify the current executable price with the broker.",
        "2. Check the latest earnings release, guidance, and material disclosures.",
        "3. Do not add a second name with the same economic driver without reducing another position.",
        "",
        "## Earnings-calendar status",
        "",
        "No official cross-market earnings-calendar source is connected in v1.3. Earnings-date alerts are intentionally marked unavailable rather than guessed.",
    ]
    return "\n".join(lines) + "\n"
