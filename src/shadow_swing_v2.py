"""Independent, auditable, rule-driven SHADOW account. Never places broker orders.

Separate from v1: no migration/reset of v1 NAV, trades or pending hard stop.
Only information timestamped no later than the signal session is eligible.
"""
from __future__ import annotations

import csv
import json
import math
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from shadow_swing import fetch_bar, today_jst

ROOT = Path("data")
OUT = ROOT / "shadow_swing_v2"
CFG_PATH = Path("config/shadow_swing_v2.json")
JST = ZoneInfo("Asia/Tokyo")


def number(value, default=None):
    try:
        x = float(value)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def read_json(path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, item):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(item, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def append_csv(path, row, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({x: row.get(x) for x in fields})


def verified_daily_bar(symbol, as_of):
    """Verified same-session OHLC; independent Yahoo chart and yfinance fallback.

    If BOTH sources fail, report an execution blocker. Never convert a
    screening/scanner 'last price' into fictional OHLC.
    """
    bar = fetch_bar(symbol, as_of)
    if bar is not None:
        return bar
    try:
        import yfinance as yf
        df = yf.download(
            symbol, start=as_of.isoformat(),
            end=(as_of + timedelta(days=1)).isoformat(),
            auto_adjust=False, progress=False, threads=False, timeout=12,
        )
        if df is None or df.empty:
            return None
        if getattr(df.columns, "nlevels", 1) > 1:
            df.columns = df.columns.get_level_values(0)
        rows = df.loc[df.index.date == as_of]
        if rows.empty:
            return None
        row = rows.iloc[-1]
        values = {key: number(row[key.capitalize()]) for key in ("open", "high", "low", "close")}
        if any(v is None or v <= 0 for v in values.values()):
            return None
        if (values["high"] < max(values["open"], values["close"])
                or values["low"] > min(values["open"], values["close"])
                or values["low"] > values["high"]):
            return None
        return values
    except Exception:
        return None


def after_jp_market_close(timestamp, day):
    if not is_same_jst_date(timestamp, day):
        return False
    dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
    local = dt.astimezone(JST)
    return (local.hour, local.minute) >= (15, 30)


def initial_state(cfg):
    capital = int(cfg["initial_cash_jpy"])
    return {
        "version": "2.0.0", "mode": "SHADOW_ONLY",
        "cohort": cfg["cohort"], "start_date": cfg["start_date"],
        "initial_cash_jpy": capital, "cash_jpy": capital, "positions": {},
        "pending_buys": [], "completed_trades": 0, "realized_pnl_jpy": 0,
        "nav_jpy": capital, "peak_nav_jpy": capital, "max_drawdown_pct": 0.0,
        "last_run_date": None, "missing_market_data": []
    }


def is_same_jst_date(timestamp, day):
    if not timestamp:
        return False
    try:
        dt = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            return False
        return dt.astimezone(JST).date() == day
    except (ValueError, TypeError):
        return False


def history_for_symbol(rows, symbol, as_of):
    out = {}
    for row in rows:
        if row.get("ticker", "").upper() != symbol.upper():
            continue
        try:
            obs = date.fromisoformat(row["observed_date"])
        except (ValueError, KeyError):
            continue
        # Historical records are only valid when their price was observed on that session.
        if obs >= as_of or not is_same_jst_date(row.get("price_as_of"), obs):
            continue
        price = number(row.get("current_price"))
        if price and price > 0:
            out[obs] = price
    return [p for _, p in sorted(out.items())][-12:]


def evaluate_candidate(screen, supply, historical_prices, cfg, as_of):
    """Independent negative checks; a high score cannot override any hard veto."""
    symbol = str(screen.get("ticker") or "")
    failures = []
    uncertainty = []
    if screen.get("market") != "JP" or not symbol.endswith(".T"):
        failures.append("not_japanese_cash_equity")
    if str(screen.get("eligible")).lower() != "true":
        failures.append("not_screening_eligible")
    if str(screen.get("research_candidate")).lower() != "true":
        failures.append("not_research_candidate")
    if not after_jp_market_close(screen.get("data_retrieved_at_utc"), as_of):
        failures.append("screen_timestamp_stale")
    if not supply or supply.get("observed_date") != as_of.isoformat():
        failures.append("supply_snapshot_missing_or_stale")
    if supply and not after_jp_market_close(supply.get("price_as_of"), as_of):
        failures.append("exchange_price_timestamp_stale")

    total = number(screen.get("total_score"))
    momentum = number(screen.get("momentum_score"))
    risk = number(screen.get("risk_score"))
    liquidity = number(screen.get("liquidity_score"))
    ret1 = number(screen.get("return_1m"))
    ret3 = number(screen.get("return_3m"))
    volume_ratio = number(supply.get("current_volume_ratio_30d")) if supply else None
    daily_change = number(supply.get("daily_change_pct")) if supply else None
    current_price = number(supply.get("current_price")) if supply else None
    scanner_price = number(screen.get("price"))
    turnover = number(supply.get("avg_turnover_30d")) if supply else None

    if any(v is None for v in (total, momentum, risk, liquidity, ret1, ret3)):
        failures.append("missing_factor_data")
    else:
        if total < cfg["gate"]["min_total_score"] or momentum < cfg["gate"]["min_momentum_score"]:
            failures.append("weak_factor_or_momentum")
        if risk < cfg["gate"]["min_risk_score"] or liquidity < cfg["gate"]["min_liquidity_score"]:
            failures.append("insufficient_risk_or_liquidity_score")
        if ret1 < cfg["gate"]["min_return_1m_pct"] or ret3 < cfg["gate"]["min_return_3m_pct"]:
            failures.append("unconfirmed_trend")
        if ret1 > cfg["gate"]["max_return_1m_pct"]:
            failures.append("overextended_one_month_run")

    if turnover is None or turnover < cfg["gate"]["min_avg_turnover_jpy"]:
        failures.append("insufficient_turnover")
    if current_price is None or current_price <= 0 or volume_ratio is None or daily_change is None:
        failures.append("missing_price_volume_evidence")
    if current_price and scanner_price:
        if abs(current_price / scanner_price - 1) > cfg["gate"]["max_price_source_disagreement_pct"] / 100:
            failures.append("price_source_disagreement")
    if supply and supply.get("data_status") not in {"ok", "partial"}:
        failures.append("supply_data_unusable")

    if len(historical_prices) < cfg["gate"]["min_history_sessions"]:
        failures.append("insufficient_point_in_time_history")

    demand_mode = None
    if not failures and historical_prices:
        prior = historical_prices[-1]
        recent = historical_prices[-4:]
        breakout = (daily_change >= 0.008 and volume_ratio >= 1.20
                    and current_price > max(recent))
        reversal = (len(historical_prices) >= 3
                    and historical_prices[-1] < historical_prices[-2]
                    and current_price > prior * 1.005
                    and volume_ratio >= 0.90 and daily_change > 0.003)
        continuation = (daily_change >= 0.005 and volume_ratio >= 0.95
                        and current_price > sum(recent) / len(recent)
                        and current_price > prior)
        if breakout:
            demand_mode = "volume_confirmed_breakout"
        elif reversal:
            demand_mode = "pullback_reversal"
        elif continuation:
            demand_mode = "positive_price_volume_continuation"
        else:
            failures.append("no_positive_demand_confirmation")
        if len(historical_prices) >= 4 and current_price / historical_prices[-4] - 1 < -0.07:
            failures.append("three_session_breakdown")
        if daily_change > 0.065:
            failures.append("late_chase_large_daily_jump")
        if volume_ratio >= 1.5 and daily_change <= -0.02:
            failures.append("distribution_risk_down_on_volume")
    short_present = bool(supply and any(supply.get(k, "") not in {"", None}
        for k in ("short_percent_float", "days_to_cover", "short_interest_change_ratio")))
    if not short_present:
        uncertainty.append("short_and_margin_positioning_unverified")
    if supply and supply.get("data_quality_flags"):
        uncertainty.append("supply_quality_flags:" + supply["data_quality_flags"])
    if supply and "SHORT_CROWDING" in str(supply.get("context_flags", "")):
        failures.append("short_crowding_requires_manual_review")
    if supply and "PRICE_DOWN_ON_VOLUME_EXPANSION" in str(supply.get("context_flags", "")):
        failures.append("observed_high_volume_distribution")
    # This is explicitly NOT a statistically calibrated alpha estimate.
    score = (total or 0) * 0.50 + (momentum or 0) * 0.25 + (risk or 0) * 0.15 + (liquidity or 0) * 0.10
    return {
        "symbol": symbol, "name": screen.get("name"), "theme": screen.get("theme") or "Other",
        "eligible": not failures, "vetoes": sorted(set(failures)),
        "unknowns": uncertainty, "signal_price": current_price,
        "ranking_heuristic": round(score, 2), "demand_mode": demand_mode,
        "observed_volume_ratio": volume_ratio, "observed_daily_return": daily_change,
        "fundamental_score": total,
        "market_may_be_wrong": "Fundamental/trend signal may survive a short-term pullback, not proven",
        "strongest_bear_case": "Prior rally may be exhausting; volume does not identify informed buying",
        "why_trade_now": demand_mode or "No demonstrated near-term buying pressure",
        "do_nothing_baseline": "Hold cash with no execution risk",
        "alternative": "Use 1306.T broad-market ETF instead of an individual stock",
        "falsifier": "Intraday -5% stop, +10% target, or 10-session maximum holding time",
        "data_as_of": as_of.isoformat(),
    }


def candidates_for_day(cfg, as_of):
    screen = read_csv(ROOT / "screening_latest.csv")
    supply = read_csv(ROOT / "supply_demand" / "supply_demand_latest.csv")
    history = read_csv(ROOT / "supply_demand" / "supply_demand_history.csv")
    lookup = {r.get("ticker", "").upper(): r for r in supply}
    jp = [r for r in screen if r.get("market") == "JP" and r.get("ticker", "").endswith(".T")]
    jp.sort(key=lambda r: number(r.get("total_score"), 0), reverse=True)
    audits = []
    for row in jp[:cfg["gate"]["audit_top_japan_candidates"]]:
        s = row["ticker"].upper()
        audits.append(evaluate_candidate(row, lookup.get(s), history_for_symbol(history, s, as_of), cfg, as_of))
    return audits


def record_trade(state, as_of, symbol, position, price, why, benchmark_close):
    qty = int(position["qty"])
    proceeds = qty * price
    cost = qty * float(position["entry_price"])
    pnl = proceeds - cost
    state["cash_jpy"] += proceeds
    state["realized_pnl_jpy"] += pnl
    state["completed_trades"] += 1
    benchmark_ret = None
    if position.get("benchmark_entry_price") and benchmark_close:
        benchmark_ret = benchmark_close / position["benchmark_entry_price"] - 1
    append_csv(OUT / "trades.csv", {
        "entry_date": position["entry_date"], "exit_date": as_of.isoformat(),
        "symbol": symbol, "qty": qty, "entry_price": position["entry_price"],
        "exit_price": round(price, 3), "pnl_jpy": round(pnl, 2),
        "return_pct": round(100 * (price / position["entry_price"] - 1), 3),
        "exit_reason": why, "entry_demand_mode": position["demand_mode"],
        "entry_unknowns": "|".join(position["unknowns"]),
        "benchmark_return_pct": round(benchmark_ret * 100, 3) if benchmark_ret is not None else "",
        "benchmark_excess_return_pct": round(100 * (price / position["entry_price"] - 1 - benchmark_ret), 3) if benchmark_ret is not None else "",
    }, ["entry_date", "exit_date", "symbol", "qty", "entry_price", "exit_price", "pnl_jpy",
        "return_pct", "exit_reason", "entry_demand_mode", "entry_unknowns",
        "benchmark_return_pct", "benchmark_excess_return_pct"])


def run(as_of=None):
    as_of = as_of or today_jst()
    cfg = read_json(CFG_PATH)
    if not cfg or cfg.get("mode") != "SHADOW_ONLY":
        raise ValueError("v2 SHADOW_ONLY configuration required")
    if as_of < date.fromisoformat(cfg["start_date"]):
        return {"status": "NOT_STARTED"}
    state_path = OUT / "state.json"
    state = read_json(state_path) if state_path.exists() else initial_state(cfg)
    if state.get("cohort") != cfg["cohort"] or state.get("initial_cash_jpy") != cfg["initial_cash_jpy"]:
        raise ValueError("Immutable cohort/initial capital mismatch; refusing to reset history")
    if state.get("last_run_date") == as_of.isoformat():
        return {"status": "ALREADY_PROCESSED", "nav_jpy": state["nav_jpy"]}
    if as_of.weekday() >= 5:
        return {"status": "NON_TRADING_DAY"}

    bars = {}
    def market_bar(symbol):
        if symbol not in bars:
            bars[symbol] = verified_daily_bar(symbol, as_of)
        return bars[symbol]

    slippage = cfg["execution"]["slippage_bps"] / 10000
    holdings = state["positions"]
    failures = []
    events = []

    benchmark_bar = market_bar("1306.T")
    benchmark_close = benchmark_bar["close"] if benchmark_bar else None

    # Execute yesterday's queued entries at NEXT session's actual open. No same-bar close fills.
    remaining = []
    for order in state["pending_buys"]:
        if order["signal_date"] >= as_of.isoformat():
            remaining.append(order)
            continue
        bar = market_bar(order["symbol"])
        if bar is None:
            failures.append("missing_ohlc_for_pending_buy:" + order["symbol"])
            remaining.append(order)
            continue
        if as_of > date.fromisoformat(order["signal_date"]) + timedelta(days=cfg["execution"]["expiry_calendar_days"]):
            events.append({"event": "BUY_EXPIRED", "symbol": order["symbol"]})
            continue
        signal = float(order["signal_price"])
        if bar["open"] / signal - 1 > cfg["execution"]["max_open_gap_pct"] / 100:
            events.append({"event": "BUY_REJECTED_GAP_CHASE", "symbol": order["symbol"]})
            continue
        fill = bar["open"] * (1 + slippage)
        notional = fill * order["qty"]
        gross = sum(p["qty"] * p["last_price"] for p in holdings.values())
        cap = cfg["risk"]["max_gross_invested_pct"] * state["initial_cash_jpy"]
        if (notional > state["cash_jpy"] or gross + notional > cap
                or len(holdings) >= cfg["risk"]["max_positions"]):
            events.append({"event": "BUY_REJECTED_PORTFOLIO_LIMIT", "symbol": order["symbol"]})
            continue
        state["cash_jpy"] -= notional
        holdings[order["symbol"]] = {
            "qty": order["qty"], "entry_price": fill,
            "entry_date": as_of.isoformat(), "last_price": fill,
            "holding_sessions": 0, "demand_mode": order["demand_mode"],
            "theme": order["theme"], "unknowns": order["unknowns"],
            "benchmark_entry_price": benchmark_bar["open"] if benchmark_bar else None,
        }
        events.append({"event": "BUY_FILLED", "symbol": order["symbol"], "qty": order["qty"],
                       "price": round(fill, 3)})
    state["pending_buys"] = remaining

    for symbol, pos in list(holdings.items()):
        bar = market_bar(symbol)
        if bar is None:
            failures.append("missing_ohlc_for_position:" + symbol)
            continue
        entry = float(pos["entry_price"])
        stop = entry * (1 - cfg["risk"]["stop_loss_pct"] / 100)
        target = entry * (1 + cfg["risk"]["take_profit_pct"] / 100)
        age = int(pos["holding_sessions"]) + 1
        exit_price = None
        reason = None
        # A close-based time exit may only fill on a LATER session's open.
        if pos.get("exit_next_open") and pos.get("exit_signal_date", "") < as_of.isoformat():
            exit_price, reason = bar["open"] * (1 - slippage), pos["exit_next_open"]
        # Conservative stop-first assumption for ambiguous same-day OHLC ordering.
        elif bar["open"] <= stop:
            exit_price, reason = bar["open"] * (1 - slippage), "gap_through_stop"
        elif bar["low"] <= stop:
            exit_price, reason = stop * (1 - slippage), "intraday_stop"
        elif bar["open"] >= target:
            exit_price, reason = bar["open"] * (1 - slippage), "gap_through_target"
        elif bar["high"] >= target:
            exit_price, reason = target * (1 - slippage), "intraday_target"
        elif age >= cfg["risk"]["max_holding_sessions"] and not pos.get("exit_next_open"):
            pos["exit_next_open"] = "time_exit"
            pos["exit_signal_date"] = as_of.isoformat()
        if exit_price is not None:
            record_trade(state, as_of, symbol, pos, exit_price, reason, benchmark_close)
            events.append({"event": "SELL_FILLED", "symbol": symbol, "reason": reason,
                           "price": round(exit_price, 3)})
            del holdings[symbol]
        else:
            pos["last_price"] = bar["close"]
            pos["holding_sessions"] = age

    # Market/feed uncertainty is exposed and must never create synthetic executions.
    state["missing_market_data"] = sorted(set(failures))
    audits = []
    entries = 0
    regime = read_json(ROOT / "regime" / "market_regime_latest.json", {})
    screen = read_csv(ROOT / "screening_latest.csv")
    if not screen or not after_jp_market_close(screen[0].get("data_retrieved_at_utc"), as_of):
        failures.append("screen_outdated_no_new_trades")
    if regime.get("date_jst") != as_of.isoformat() or not regime.get("actionable", False):
        failures.append("regime_stale_or_non_actionable")
    if regime.get("stress_flag") or regime.get("thin_liquidity_flag"):
        failures.append("market_stress_no_new_entries")
    if benchmark_bar is None:
        failures.append("benchmark_bar_unavailable")
    if not failures and as_of <= date.fromisoformat(cfg["end_date"]):
        audits = candidates_for_day(cfg, as_of)
        themes = {}
        for p in holdings.values():
            themes[p.get("theme", "Other")] = themes.get(p.get("theme", "Other"), 0) + 1
        for p in state["pending_buys"]:
            themes[p["theme"]] = themes.get(p["theme"], 0) + 1
        busy = set(holdings) | {p["symbol"] for p in state["pending_buys"]}
        for a in sorted(audits, key=lambda x: x["ranking_heuristic"], reverse=True):
            if entries >= cfg["risk"]["max_new_entries_per_session"]:
                break
            if not a["eligible"] or a["symbol"] in busy:
                continue
            if themes.get(a["theme"], 0) >= cfg["risk"]["max_positions_per_theme"]:
                a["vetoes"].append("theme_concentration")
                a["eligible"] = False
                continue
            if len(busy) >= cfg["risk"]["max_positions"]:
                break
            fraction = cfg["risk"]["max_position_pct"]
            if a["unknowns"]:
                fraction *= cfg["risk"]["uncertainty_size_multiplier"]
            current_mv = sum(x["qty"] * x["last_price"] for x in holdings.values())
            committed = sum(p["qty"] * p["signal_price"] for p in state["pending_buys"])
            gross_room = cfg["risk"]["max_gross_invested_pct"] * state["initial_cash_jpy"] - current_mv - committed
            budget = min(fraction * state["initial_cash_jpy"],
                         state["cash_jpy"] - committed, gross_room)
            lot = cfg["execution"]["round_lot_shares"]
            qty = int(budget // (lot * a["signal_price"])) * lot if a["signal_price"] else 0
            avg_turnover = next((number(r.get("avg_turnover_30d")) for r in read_csv(ROOT / "supply_demand" / "supply_demand_latest.csv")
                                 if r.get("ticker") == a["symbol"]), None)
            if not avg_turnover or qty * a["signal_price"] > cfg["execution"]["max_turnover_participation_pct"] / 100 * avg_turnover:
                a["vetoes"].append("execution_liquidity_limit")
                a["eligible"] = False
                continue
            if qty < lot:
                a["vetoes"].append("insufficient_capacity_for_one_lot")
                a["eligible"] = False
                continue
            order = {
                "signal_date": as_of.isoformat(), "symbol": a["symbol"], "qty": qty,
                "signal_price": a["signal_price"], "demand_mode": a["demand_mode"],
                "theme": a["theme"], "unknowns": a["unknowns"],
                "critical_review": {"bear_case": a["strongest_bear_case"],
                    "do_nothing": a["do_nothing_baseline"], "falsifier": a["falsifier"],
                    "market_alternative": a["alternative"]}
            }
            state["pending_buys"].append(order)
            busy.add(a["symbol"])
            themes[a["theme"]] = themes.get(a["theme"], 0) + 1
            entries += 1
            events.append({"event": "BUY_QUEUED_NEXT_OPEN", "symbol": a["symbol"],
                           "qty": qty, "demand_mode": a["demand_mode"]})

    market_value = sum(p["qty"] * p["last_price"] for p in holdings.values())
    state["nav_jpy"] = round(state["cash_jpy"] + market_value, 2)
    state["peak_nav_jpy"] = max(state["peak_nav_jpy"], state["nav_jpy"])
    state["max_drawdown_pct"] = min(state["max_drawdown_pct"],
                                    100 * (state["nav_jpy"] / state["peak_nav_jpy"] - 1))
    state["last_run_date"] = as_of.isoformat()
    state["missing_market_data"] = sorted(set(failures))
    snapshot = {
        "as_of_date": as_of.isoformat(), "cohort": cfg["cohort"], "mode": "SHADOW_ONLY",
        "initial_cash_jpy": state["initial_cash_jpy"], "nav_jpy": state["nav_jpy"],
        "return_pct": round(100 * (state["nav_jpy"] / state["initial_cash_jpy"] - 1), 3),
        "cash_jpy": round(state["cash_jpy"], 2), "open_positions": len(holdings),
        "completed_trades": state["completed_trades"], "queued_buys": len(state["pending_buys"]),
        "market_data_blockers": sorted(set(failures)),
        "events": events, "candidate_audit": audits,
        "methodology": "Rule-driven paper test; not a validated alpha model or ChatGPT discretionary fill",
        "comparison": "v1 stays in data/shadow_swing, unmodified and historically comparable"
    }
    save_json(state_path, state)
    save_json(OUT / "latest.json", snapshot)
    save_json(OUT / "adversarial_review_latest.json", {
        "as_of_date": as_of.isoformat(),
        "critical_question": "What independent evidence of buying pressure exists, and why not stay in cash?",
        "candidate_audit": audits, "blockers": sorted(set(failures)),
        "interpretation": "Missing short/margin data are explicitly unknown; scores never override vetoes."
    })
    append_csv(OUT / "equity_curve.csv", {
        "date": as_of.isoformat(), "nav_jpy": state["nav_jpy"],
        "cash_jpy": round(state["cash_jpy"], 2), "completed_trades": state["completed_trades"],
        "open_positions": len(holdings), "new_signals": entries,
    }, ["date", "nav_jpy", "cash_jpy", "completed_trades", "open_positions", "new_signals"])
    report = [
        "# AI Shadow Swing v2 — critical-demand paper cohort",
        "Date: " + as_of.isoformat(),
        "Mode: SHADOW ONLY / no real orders",
        "NAV: ¥{:,.0f} / ¥{:,.0f} ({}%)".format(state["nav_jpy"], state["initial_cash_jpy"], snapshot["return_pct"]),
        "Positions: {} | completed: {} | pending next-open buys: {}".format(len(holdings), state["completed_trades"], len(state["pending_buys"])),
        "Market blockers: " + (", ".join(snapshot["market_data_blockers"]) or "none"),
        "Qualified candidates: {} / {}".format(sum(1 for x in audits if x["eligible"]), len(audits)),
        "Events:",
    ] + ["- " + str(x) for x in events]
    (OUT / "latest_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    return snapshot


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, default=str))
