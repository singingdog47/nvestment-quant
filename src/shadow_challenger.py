"""Independent paper-only challenger: evaluate opportunities, even with ancillary feed gaps.

Signals use a same-day *post-close* screening snapshot. Fills/stop executions
require verified next-session OHLC; scanner prices NEVER produce fills.
No brokerage integration or personal portfolio holdings.
"""
from __future__ import annotations

import csv
import json
import math
from datetime import date
from pathlib import Path
from typing import Callable

from shadow_swing import today_jst
from shadow_swing_v2 import verified_daily_bar, after_jp_market_close

DATA = Path("data")
OUT = DATA / "shadow_challenger"
CONFIG = Path("config/shadow_challenger_v1.json")


def load_json(path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rows(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def finite(value, default=None):
    try:
        v = float(value)
        return v if math.isfinite(v) else default
    except (TypeError, ValueError):
        return default


def new_state(cfg):
    cash = float(cfg["initial_cash_jpy"])
    return {
        "cohort": cfg["cohort"], "mode": "SHADOW_ONLY",
        "cash_jpy": cash, "initial_cash_jpy": cash, "positions": {},
        "pending_buys": [], "pending_sells": [], "trades": [],
        "peak_nav_jpy": cash, "nav_jpy": cash, "last_run_date": None,
        "last_screen_date": None, "benchmark_start_close": None,
    }


def candidate_audit(screen, cfg):
    result = []
    for x in screen:
        if x.get("market") != "JP" or not str(x.get("ticker", "")).endswith(".T"):
            continue
        score = finite(x.get("total_score"))
        momentum = finite(x.get("momentum_score"))
        liquidity = finite(x.get("liquidity_score"))
        turnover = finite(x.get("avg_turnover_30d"))
        price = finite(x.get("price"))
        failures = []
        if str(x.get("eligible")).lower() != "true":
            failures.append("not_eligible")
        if any(v is None for v in (score, momentum, liquidity, turnover, price)):
            failures.append("missing_essential_factor")
        else:
            if score < cfg["selection"]["min_total_score"]:
                failures.append("low_composite")
            if momentum < cfg["selection"]["min_momentum_score"]:
                failures.append("weak_momentum")
            if liquidity < cfg["selection"]["min_liquidity_score"] or turnover < cfg["selection"]["min_avg_turnover_jpy"]:
                failures.append("liquidity")
            if price <= 0:
                failures.append("invalid_price")
        result.append({
            "symbol": x.get("ticker"), "score": score, "momentum": momentum,
            "price": price, "theme": x.get("theme") or "Other",
            "fundamental_partial": x.get("flags") == "fundamental_partial",
            "vetoes": failures, "eligible": not failures,
        })
    result.sort(key=lambda x: (x["score"] or -1), reverse=True)
    return result[:cfg["selection"]["audit_top_n"]]


def valid_bar(bar):
    if not isinstance(bar, dict):
        return False
    values = [finite(bar.get(k)) for k in ("open", "high", "low", "close")]
    o, h, l, c = values
    return all(v is not None and v > 0 for v in values) and l <= min(o, c) <= max(o, c) <= h


def run(as_of=None, bar_source: Callable | None = None):
    as_of = as_of or today_jst()
    cfg = load_json(CONFIG)
    if cfg["mode"] != "SHADOW_ONLY":
        raise ValueError("SHADOW_ONLY required")
    if as_of < date.fromisoformat(cfg["start_date"]) or as_of.weekday() >= 5:
        return {"status": "OUTSIDE_SESSION"}
    state = load_json(OUT / "state.json") or new_state(cfg)
    if state["cohort"] != cfg["cohort"] or state["initial_cash_jpy"] != cfg["initial_cash_jpy"]:
        raise ValueError("Immutable cohort mismatch")
    if state.get("last_run_date") == as_of.isoformat():
        return {"status": "ALREADY_PROCESSED", "nav_jpy": state["nav_jpy"]}

    source = bar_source or verified_daily_bar
    cache = {}
    def bar(symbol):
        if symbol not in cache:
            observation = source(symbol, as_of)
            cache[symbol] = observation if valid_bar(observation) else None
        return cache[symbol]

    events = []
    risk, execution = cfg["risk"], cfg["execution"]
    slip = execution["slippage_bps"] / 10000

    # An unfilled BUY must not survive indefinitely or fill retrospectively.
    pending = []
    for order in state["pending_buys"]:
        age = (as_of - date.fromisoformat(order["signal_date"])).days
        if age <= 0:
            pending.append(order)
            continue
        if age > execution["max_pending_calendar_days"]:
            events.append({"event": "ENTRY_EXPIRED", "symbol": order["symbol"]})
            continue
        b = bar(order["symbol"])
        if b is None:
            events.append({"event": "ENTRY_BAR_MISSING", "symbol": order["symbol"]})
            pending.append(order)
            continue
        fill = b["open"] * (1 + slip)
        # Size from current open, never trust the signal price as a fill.
        affordable = min(state["cash_jpy"], risk["max_gross_invested_pct"] * cfg["initial_cash_jpy"] -
                         sum(p["qty"] * p["last_price"] for p in state["positions"].values()))
        lot = execution["round_lot_shares"]
        qty = min(order["qty"], int(min(affordable, order["max_notional"]) // (lot * fill)) * lot)
        if qty < lot or order["symbol"] in state["positions"]:
            events.append({"event": "ENTRY_CANCELLED_CAPACITY", "symbol": order["symbol"]})
            continue
        state["positions"][order["symbol"]] = {
            "qty": qty, "entry_price": fill, "last_price": fill,
            "entry_date": as_of.isoformat(), "sessions": 0,
            "theme": order["theme"], "peak_close": b["close"],
        }
        state["cash_jpy"] -= qty * fill
        events.append({"event": "BUY", "symbol": order["symbol"], "qty": qty, "price": round(fill, 3)})
    state["pending_buys"] = pending

    # Exit at a VERIFIED bar. Intraday stop takes precedence over target if both hit.
    for symbol, pos in list(state["positions"].items()):
        b = bar(symbol)
        if b is None:
            events.append({"event": "POSITION_BAR_MISSING", "symbol": symbol})
            continue
        pos["sessions"] += 1
        pos["peak_close"] = max(pos["peak_close"], b["close"])
        stop = pos["entry_price"] * (1 - risk["stop_loss_pct"] / 100)
        target = pos["entry_price"] * (1 + risk["take_profit_pct"] / 100)
        reason, exit_price = None, None
        if symbol in state["pending_sells"]:
            reason, exit_price = "TIME_EXIT", b["open"] * (1 - slip)
        elif b["low"] <= stop:
            reason, exit_price = "STOP", min(b["open"], stop) * (1 - slip)
        elif b["high"] >= target:
            reason, exit_price = "TARGET", max(b["open"], target) * (1 - slip)
        if reason:
            state["cash_jpy"] += pos["qty"] * exit_price
            pnl = pos["qty"] * (exit_price - pos["entry_price"])
            trade = {"date": as_of.isoformat(), "symbol": symbol, "qty": pos["qty"],
                     "entry": round(pos["entry_price"], 3), "exit": round(exit_price, 3),
                     "pnl_jpy": round(pnl, 2), "reason": reason}
            state["trades"].append(trade)
            events.append({"event": "SELL", **trade})
            del state["positions"][symbol]
            continue
        pos["last_price"] = b["close"]
        if pos["sessions"] >= risk["max_holding_sessions"] and symbol not in state["pending_sells"]:
            state["pending_sells"].append(symbol)
    state["pending_sells"] = [s for s in state["pending_sells"] if s in state["positions"]]

    screen = rows(DATA / "screening_latest.csv")
    screen_fresh = bool(screen and after_jp_market_close(screen[0].get("data_retrieved_at_utc"), as_of))
    audits = candidate_audit(screen, cfg) if screen_fresh else []
    regime = load_json(DATA / "regime" / "market_regime_latest.json", {}) or {}
    regime_ok = regime.get("date_jst") == as_of.isoformat() and regime.get("actionable") is True
    # Missing optional market context reduces size, NOT candidate investigation.
    size_multiplier = 1.0 if regime_ok else risk["uncertain_regime_size_multiplier"]
    gross = sum(p["qty"] * p["last_price"] for p in state["positions"].values())
    themes = {}
    for p in state["positions"].values():
        themes[p["theme"]] = themes.get(p["theme"], 0) + 1
    for p in state["pending_buys"]:
        themes[p["theme"]] = themes.get(p["theme"], 0) + 1
    busy = set(state["positions"]) | {p["symbol"] for p in state["pending_buys"]}
    selected = 0
    if screen_fresh and as_of <= date.fromisoformat(cfg["end_date"]):
        for candidate in audits:
            if selected >= risk["max_entries_per_session"] or len(busy) >= risk["max_positions"]:
                break
            symbol = candidate["symbol"]
            if not candidate["eligible"] or symbol in busy:
                continue
            theme = candidate["theme"]
            if themes.get(theme, 0) >= risk["max_per_theme"]:
                continue
            budget = min(cfg["initial_cash_jpy"] * risk["max_position_pct"] * size_multiplier *
                         (risk["partial_fundamental_size_multiplier"] if candidate["fundamental_partial"] else 1),
                         risk["max_gross_invested_pct"] * cfg["initial_cash_jpy"] - gross,
                         state["cash_jpy"])
            lot = execution["round_lot_shares"]
            qty = int(budget // (lot * candidate["price"])) * lot
            if qty < lot:
                continue
            state["pending_buys"].append({"symbol": symbol, "signal_date": as_of.isoformat(),
                                          "qty": qty, "theme": theme, "signal_price": candidate["price"], "max_notional": budget})
            busy.add(symbol)
            themes[theme] = themes.get(theme, 0) + 1
            gross += qty * candidate["price"]
            selected += 1
            events.append({"event": "BUY_SIGNAL", "symbol": symbol, "qty": qty})
    elif not screen_fresh:
        events.append({"event": "STALE_SCREEN", "note": "No fresh buy signals; exits remain active"})

    unpriced = [symbol for symbol in state["positions"] if bar(symbol) is None]
    nav = state["cash_jpy"] + sum(p["qty"] * p["last_price"] for p in state["positions"].values())
    benchmark = bar("1306.T")
    if benchmark is not None and state.get("benchmark_start_close") is None:
        state["benchmark_start_close"] = benchmark["close"]
    benchmark_return = ((benchmark["close"] / state["benchmark_start_close"] - 1) * 100
                        if benchmark is not None and state.get("benchmark_start_close") else None)
    state["nav_jpy"] = round(nav, 2)
    state["peak_nav_jpy"] = max(state["peak_nav_jpy"], nav)
    state["last_run_date"] = as_of.isoformat()
    state["last_screen_date"] = as_of.isoformat() if screen_fresh else state.get("last_screen_date")
    result = {
        "date": as_of.isoformat(), "mode": "SHADOW_ONLY", "status": "OK" if screen_fresh else "NO_NEW_SIGNALS",
        "nav_jpy": state["nav_jpy"], "return_pct": round(100 * (nav / cfg["initial_cash_jpy"] - 1), 3),
        "cash_jpy": round(state["cash_jpy"], 2), "positions": len(state["positions"]),
        "pending_buys": len(state["pending_buys"]), "trades": len(state["trades"]),
        "screen_fresh": screen_fresh, "regime_actionable": regime_ok,
        "sizing_multiplier": size_multiplier, "unpriced_symbols": unpriced,
        "candidate_audit": audits[:10], "events": events,
        "benchmark_return_pct": round(benchmark_return, 3) if benchmark_return is not None else None,
        "benchmark_comparison_start": "first successfully priced session, not necessarily cohort start",
        "benchmark_note": "TOPIX comparison optional; missing benchmark never blocks paper entries.",
        "caveat": "NAV uses last known price for unpriced positions; do not treat as verified daily return.",
    }
    write_json(OUT / "state.json", state)
    write_json(OUT / "latest.json", result)
    (OUT / "latest_report.md").write_text(
        "# AI Challenger v1 — SHADOW ONLY\n\n"
        f"Date: {as_of} | NAV: ¥{nav:,.0f} | Return: {result['return_pct']:+.2f}%\n\n"
        f"Positions: {len(state['positions'])} | Pending entries: {len(state['pending_buys'])} | "
        f"Closed trades: {len(state['trades'])}\n\n"
        f"Fresh screen: {screen_fresh} | Regime actionable: {regime_ok} | "
        f"Sizing multiplier: {size_multiplier}\n\n"
        f"Unpriced: {unpriced}\n\n"
        "No actual broker orders. Signals and fills are separate sessions.\n",
        encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
