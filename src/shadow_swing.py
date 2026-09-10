from __future__ import annotations

import csv
import json
import math
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import requests

VERSION = "1.0.0"
ROOT = Path("data")
OUT = ROOT / "shadow_swing"
CONFIG = Path("config/shadow_swing_v1.json")
JST = ZoneInfo("Asia/Tokyo")


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def as_float(value: Any, default: float | None = None) -> float | None:
    try:
        x = float(value)
        return x if math.isfinite(x) else default
    except (TypeError, ValueError):
        return default


def today_jst() -> date:
    override = os.getenv("SHADOW_AS_OF_DATE")
    return date.fromisoformat(override) if override else datetime.now(JST).date()


def new_state(cfg: dict[str, Any]) -> dict[str, Any]:
    capital = float(cfg["initial_cash_jpy"])
    return {
        "version": VERSION,
        "mode": "SHADOW_ONLY",
        "start_date": cfg["start_date"],
        "end_date": cfg["end_date"],
        "cash_jpy": capital,
        "positions": {},
        "pending_orders": [],
        "processed_gpt_decision_ids": [],
        "realized_pnl_jpy": 0.0,
        "nav_jpy": capital,
        "peak_nav_jpy": capital,
        "max_drawdown_pct": 0.0,
        "benchmark_start_price": None,
        "last_run_date": None,
        "status": "ACTIVE",
    }


def fetch_bar(symbol: str, session_date: date) -> dict[str, float] | None:
    start = datetime.combine(session_date - timedelta(days=2), datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(session_date + timedelta(days=2), datetime.min.time(), tzinfo=timezone.utc)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "period1": int(start.timestamp()),
        "period2": int(end.timestamp()),
        "interval": "1d",
        "events": "history",
    }
    try:
        r = requests.get(url, params=params, timeout=15, headers={"User-Agent": "investment-quant-shadow/1.0"})
        r.raise_for_status()
        result = r.json().get("chart", {}).get("result", [])
        if not result:
            return None
        payload = result[0]
        stamps = payload.get("timestamp", [])
        quote = payload.get("indicators", {}).get("quote", [{}])[0]
        for i, stamp in enumerate(stamps):
            d = datetime.fromtimestamp(stamp, timezone.utc).astimezone(JST).date()
            if d != session_date:
                continue
            bar: dict[str, float] = {}
            for key in ("open", "high", "low", "close"):
                values = quote.get(key, [])
                value = as_float(values[i] if i < len(values) else None)
                if value is None:
                    return None
                bar[key] = value
            return bar
    except Exception:
        return None
    return None


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def append_csv(path: Path, row: dict[str, Any], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow({k: row.get(k) for k in fields})


def queue_order(state: dict[str, Any], order: dict[str, Any]) -> None:
    if any(
        x.get("symbol") == order.get("symbol") and x.get("side") == order.get("side")
        for x in state.get("pending_orders", [])
    ):
        return
    state.setdefault("pending_orders", []).append(order)
    append_jsonl(OUT / "orders.jsonl", order)


def ingest_gpt_decision(state: dict[str, Any], as_of: date, cfg: dict[str, Any]) -> None:
    decision = read_json(OUT / "gpt_decision_latest.json", {})
    decision_id = str(decision.get("decision_id") or "")
    decision_date_text = str(decision.get("decision_date") or "")
    if not decision_id or not decision_date_text or decision.get("mode") != "SHADOW_ONLY":
        return
    try:
        signal_date = date.fromisoformat(decision_date_text)
    except ValueError:
        return
    if signal_date > as_of or decision_id in set(state.get("processed_gpt_decision_ids", [])):
        return

    risk = cfg["risk"]
    initial = float(cfg["initial_cash_jpy"])
    pending_symbols = {str(x.get("symbol")) for x in state.get("pending_orders", [])}

    for action in decision.get("actions", []):
        side = str(action.get("action") or "").upper()
        if side == "HOLD":
            continue
        if side not in {"BUY", "SELL"}:
            continue
        symbol = str(action.get("symbol") or "").strip()
        if not symbol.endswith(".T"):
            continue

        if side == "SELL":
            pos = state.get("positions", {}).get(symbol)
            if not pos or symbol in pending_symbols:
                continue
            queue_order(state, {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "decision_id": decision_id,
                "signal_date": signal_date.isoformat(),
                "side": "SELL",
                "symbol": symbol,
                "code": pos.get("code"),
                "name": pos.get("name"),
                "qty": int(pos["qty"]),
                "order_type": "MARKET_NEXT_OPEN",
                "reason": action.get("reason", "gpt_exit"),
                "confidence": action.get("confidence"),
                "status": "PENDING",
            })
            pending_symbols.add(symbol)
            continue

        if symbol in state.get("positions", {}) or symbol in pending_symbols:
            continue
        active_buys = sum(1 for x in state.get("pending_orders", []) if x.get("side") == "BUY")
        if len(state.get("positions", {})) + active_buys >= int(risk["max_positions"]):
            continue
        signal_price = as_float(action.get("signal_price"))
        if not signal_price or signal_price <= 0:
            continue

        requested_weight = as_float(action.get("target_weight_pct"), 0.20) or 0.20
        target_weight = min(float(risk["max_position_pct"]), max(0.0, requested_weight))
        current_mv = sum(float(p["last_price"]) * int(p["qty"]) for p in state.get("positions", {}).values())
        room_by_cash = float(state["cash_jpy"]) - initial * float(risk["min_cash_pct"])
        room_by_invested = initial * float(risk["max_invested_pct"]) - current_mv
        budget = max(0.0, min(initial * target_weight, room_by_cash, room_by_invested))
        lot = int(cfg["execution"]["round_lot_shares"])
        lots = int(budget // (signal_price * lot))
        if lots < 1:
            continue
        qty = lots * lot

        order_type = "LIMIT" if str(action.get("order_type") or "").upper() == "LIMIT" else "MARKET_NEXT_OPEN"
        order = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "decision_id": decision_id,
            "signal_date": signal_date.isoformat(),
            "side": "BUY",
            "symbol": symbol,
            "code": action.get("code"),
            "name": action.get("name", symbol),
            "theme": action.get("theme", "Other"),
            "qty": qty,
            "signal_price": signal_price,
            "order_type": order_type,
            "reason": action.get("reason", "gpt_entry"),
            "confidence": action.get("confidence"),
            "status": "PENDING",
            "attempts": 0,
        }
        if order_type == "LIMIT":
            limit_price = as_float(action.get("limit_price"))
            if not limit_price or limit_price <= 0:
                continue
            order["limit_price"] = limit_price
        queue_order(state, order)
        pending_symbols.add(symbol)

    state.setdefault("processed_gpt_decision_ids", []).append(decision_id)
    state["processed_gpt_decision_ids"] = state["processed_gpt_decision_ids"][-200:]


def process_pending(state: dict[str, Any], as_of: date, cfg: dict[str, Any]) -> list[dict[str, Any]]:
    fills: list[dict[str, Any]] = []
    keep: list[dict[str, Any]] = []
    slippage = float(cfg["execution"]["slippage_bps"]) / 10000.0

    for order in state.get("pending_orders", []):
        signal_date = date.fromisoformat(order["signal_date"])
        if as_of <= signal_date:
            keep.append(order)
            continue
        bar = fetch_bar(order["symbol"], as_of)
        if not bar:
            keep.append(order)
            continue

        side = order["side"]
        fill_price: float | None = None
        if side == "BUY" and order.get("order_type") == "LIMIT":
            limit_price = float(order["limit_price"])
            if bar["low"] <= limit_price:
                fill_price = min(bar["open"], limit_price)
        else:
            fill_price = bar["open"] * (1 + slippage if side == "BUY" else 1 - slippage)

        if fill_price is None:
            order["attempts"] = int(order.get("attempts", 0)) + 1
            if order["attempts"] < int(cfg["execution"]["limit_expiry_sessions"]):
                keep.append(order)
            else:
                order["status"] = "EXPIRED"
                order["resolved_date"] = as_of.isoformat()
                append_jsonl(OUT / "orders.jsonl", order)
            continue

        qty = int(order["qty"])
        value = fill_price * qty
        if side == "BUY":
            if value > float(state["cash_jpy"]):
                order["status"] = "REJECTED_CASH"
                order["resolved_date"] = as_of.isoformat()
                append_jsonl(OUT / "orders.jsonl", order)
                continue
            state["cash_jpy"] = float(state["cash_jpy"]) - value
            state["positions"][order["symbol"]] = {
                "symbol": order["symbol"],
                "code": order.get("code"),
                "name": order.get("name"),
                "theme": order.get("theme", "Other"),
                "qty": qty,
                "entry_price": fill_price,
                "entry_date": as_of.isoformat(),
                "last_price": fill_price,
                "peak_price": fill_price,
                "holding_sessions": 0,
                "confidence": order.get("confidence"),
                "decision_id": order.get("decision_id"),
            }
            pnl = 0.0
        else:
            pos = state["positions"].pop(order["symbol"], None)
            if not pos:
                continue
            qty = int(pos["qty"])
            value = fill_price * qty
            pnl = (fill_price - float(pos["entry_price"])) * qty
            state["cash_jpy"] = float(state["cash_jpy"]) + value
            state["realized_pnl_jpy"] = float(state.get("realized_pnl_jpy", 0.0)) + pnl

        fill = {
            "date": as_of.isoformat(),
            "symbol": order["symbol"],
            "side": side,
            "qty": qty,
            "fill_price": round(fill_price, 4),
            "value_jpy": round(value, 2),
            "realized_pnl_jpy": round(pnl, 2),
            "reason": order.get("reason"),
            "signal_date": order.get("signal_date"),
            "decision_id": order.get("decision_id"),
        }
        fills.append(fill)
        append_csv(
            OUT / "trades.csv",
            fill,
            ["date", "symbol", "side", "qty", "fill_price", "value_jpy", "realized_pnl_jpy", "reason", "signal_date", "decision_id"],
        )
        order["status"] = "FILLED"
        order["resolved_date"] = as_of.isoformat()
        order["fill_price"] = round(fill_price, 4)
        append_jsonl(OUT / "orders.jsonl", order)

    state["pending_orders"] = keep
    return fills


def screening_price_map(screen: pd.DataFrame) -> dict[str, float]:
    prices: dict[str, float] = {}
    if screen.empty:
        return prices
    for _, row in screen.iterrows():
        market = str(row.get("market") or "").upper()
        code = str(row.get("code") or "").strip()
        ticker = str(row.get("ticker") or "").strip()
        if market not in {"JP", "JAPAN", "TSE", "TOKYO"}:
            continue
        symbol = ticker if ticker.endswith(".T") else (f"{code}.T" if code else "")
        price = as_float(row.get("price"))
        if symbol and price and price > 0:
            prices[symbol] = price
    return prices


def mark_to_market(state: dict[str, Any], screen: pd.DataFrame, as_of: date) -> None:
    prices = screening_price_map(screen)
    market_value = 0.0
    for symbol, pos in state.get("positions", {}).items():
        price = prices.get(symbol)
        if price is None:
            bar = fetch_bar(symbol, as_of)
            price = bar["close"] if bar else float(pos["last_price"])
        pos["last_price"] = float(price)
        pos["peak_price"] = max(float(pos.get("peak_price", price)), float(price))
        pos["holding_sessions"] = int(pos.get("holding_sessions", 0)) + 1
        market_value += float(price) * int(pos["qty"])
    nav = float(state["cash_jpy"]) + market_value
    state["nav_jpy"] = nav
    state["peak_nav_jpy"] = max(float(state.get("peak_nav_jpy", nav)), nav)
    dd = nav / float(state["peak_nav_jpy"]) - 1 if state["peak_nav_jpy"] else 0.0
    state["max_drawdown_pct"] = min(float(state.get("max_drawdown_pct", 0.0)), dd * 100)


def market_is_stressed(regime: dict[str, Any]) -> bool:
    label = str(regime.get("regime_label") or "").upper()
    return bool(regime.get("stress_flag")) or any(x in label for x in ("PANIC", "RISK_OFF", "RISK-OFF"))


def queue_mechanical_exits(state: dict[str, Any], as_of: date, cfg: dict[str, Any], regime: dict[str, Any]) -> None:
    risk = cfg["risk"]
    pending = {str(x.get("symbol")) for x in state.get("pending_orders", [])}
    for symbol, pos in list(state.get("positions", {}).items()):
        if symbol in pending:
            continue
        entry = float(pos["entry_price"])
        price = float(pos["last_price"])
        peak = float(pos.get("peak_price", price))
        ret = price / entry - 1
        reason = None
        if state.get("status") == "KILL_SWITCH":
            reason = "portfolio_kill_switch"
        elif market_is_stressed(regime):
            reason = "market_regime_stress"
        elif ret <= float(risk["hard_stop_pct"]):
            reason = "hard_stop"
        elif ret >= float(risk["take_profit_pct"]):
            reason = "take_profit"
        elif peak / entry - 1 >= float(risk["trailing_activation_pct"]) and price / peak - 1 <= -float(risk["trailing_stop_pct"]):
            reason = "trailing_stop"
        elif int(pos.get("holding_sessions", 0)) >= int(risk["max_holding_sessions"]):
            reason = "time_exit"
        if reason:
            queue_order(state, {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "signal_date": as_of.isoformat(),
                "side": "SELL",
                "symbol": symbol,
                "code": pos.get("code"),
                "name": pos.get("name"),
                "qty": int(pos["qty"]),
                "order_type": "MARKET_NEXT_OPEN",
                "reason": reason,
                "status": "PENDING",
            })


def benchmark_return(cfg: dict[str, Any], state: dict[str, Any], as_of: date) -> float | None:
    symbol = str(cfg["benchmark_symbol"])
    start_date = date.fromisoformat(cfg["start_date"])
    start_bar = fetch_bar(symbol, start_date)
    now_bar = fetch_bar(symbol, as_of)
    if state.get("benchmark_start_price") is None and start_bar:
        state["benchmark_start_price"] = start_bar["close"]
    base = as_float(state.get("benchmark_start_price"))
    return now_bar["close"] / base - 1 if base and now_bar else None


def metrics(cfg: dict[str, Any], state: dict[str, Any], bench: float | None) -> dict[str, Any]:
    initial = float(cfg["initial_cash_jpy"])
    ret = float(state["nav_jpy"]) / initial - 1
    return {
        "initial_capital_jpy": initial,
        "nav_jpy": round(float(state["nav_jpy"]), 2),
        "cash_jpy": round(float(state["cash_jpy"]), 2),
        "total_return_pct": round(ret * 100, 3),
        "benchmark_return_pct": round(bench * 100, 3) if bench is not None else None,
        "alpha_pct": round((ret - bench) * 100, 3) if bench is not None else None,
        "realized_pnl_jpy": round(float(state.get("realized_pnl_jpy", 0.0)), 2),
        "max_drawdown_pct": round(float(state.get("max_drawdown_pct", 0.0)), 3),
        "positions": len(state.get("positions", {})),
        "pending_orders": len(state.get("pending_orders", [])),
    }


def record_equity(as_of: date, m: dict[str, Any]) -> None:
    path = OUT / "equity_curve.csv"
    if path.exists():
        try:
            old = pd.read_csv(path)
            if "date" in old and as_of.isoformat() in set(old["date"].astype(str)):
                return
        except Exception:
            pass
    append_csv(path, {"date": as_of.isoformat(), **m}, [
        "date", "initial_capital_jpy", "nav_jpy", "cash_jpy", "total_return_pct",
        "benchmark_return_pct", "alpha_pct", "realized_pnl_jpy", "max_drawdown_pct",
        "positions", "pending_orders",
    ])


def build_report(as_of: date, cfg: dict[str, Any], state: dict[str, Any], m: dict[str, Any], fills: list[dict[str, Any]]) -> str:
    bench = f"{m['benchmark_return_pct']:+.2f}%" if m["benchmark_return_pct"] is not None else "N/A"
    alpha = f"{m['alpha_pct']:+.2f}%" if m["alpha_pct"] is not None else "N/A"
    lines = [
        "# AI Shadow Swing — Daily Status", "",
        f"- As of: {as_of.isoformat()} JST",
        f"- Experiment: ¥{int(cfg['initial_cash_jpy']):,} / {cfg['start_date']} → {cfg['end_date']}",
        "- Mode: SHADOW ONLY — no broker connection and no real orders",
        f"- NAV: ¥{m['nav_jpy']:,.0f} | Cash: ¥{m['cash_jpy']:,.0f}",
        f"- Return: {m['total_return_pct']:+.2f}% | Benchmark: {bench} | Alpha: {alpha}",
        f"- Max DD: {m['max_drawdown_pct']:.2f}% | Status: {state['status']}", "", "## Positions",
    ]
    if not state.get("positions"):
        lines.append("- None")
    for pos in state.get("positions", {}).values():
        r = (float(pos["last_price"]) / float(pos["entry_price"]) - 1) * 100
        lines.append(f"- {pos['symbol']} {pos.get('name','')}: {pos['qty']} shares / entry ¥{pos['entry_price']:.2f} / last ¥{pos['last_price']:.2f} / {r:+.2f}%")
    lines += ["", "## Pending orders"]
    if not state.get("pending_orders"):
        lines.append("- None")
    for order in state.get("pending_orders", []):
        limit_text = f" @ ¥{order['limit_price']:.2f}" if order.get("order_type") == "LIMIT" else ""
        lines.append(f"- {order['side']} {order['symbol']} {order['qty']} / {order['order_type']}{limit_text} / {order.get('reason')}")
    lines += ["", "## Fills today"]
    if not fills:
        lines.append("- None")
    for fill in fills:
        lines.append(f"- {fill['side']} {fill['symbol']} {fill['qty']} @ ¥{fill['fill_price']:.2f} / {fill['reason']}")
    lines += ["", "## Rules", "- ChatGPT supplies discretionary BUY/SELL/HOLD decisions; code enforces sizing and loss limits.",
              "- Signals are post-close and cannot fill before the next session.",
              "- No leverage, short selling, or real-money execution."]
    return "\n".join(lines) + "\n"


def run(as_of: date | None = None) -> dict[str, Any]:
    as_of = as_of or today_jst()
    cfg = read_json(CONFIG, {})
    if not cfg:
        raise FileNotFoundError(str(CONFIG))
    start = date.fromisoformat(cfg["start_date"])
    end = date.fromisoformat(cfg["end_date"])
    if as_of < start:
        return {"status": "NOT_STARTED", "as_of_date": as_of.isoformat()}

    OUT.mkdir(parents=True, exist_ok=True)
    state_path = OUT / "state.json"
    state = read_json(state_path, None) or new_state(cfg)
    if state.get("last_run_date") == as_of.isoformat():
        return {"status": "IDEMPOTENT_NOOP", **read_json(OUT / "latest.json", {})}

    screen_path = ROOT / "screening_latest.csv"
    screen = pd.read_csv(screen_path) if screen_path.exists() else pd.DataFrame()
    regime = read_json(ROOT / "regime" / "market_regime_latest.json", {})
    data_fresh = str(regime.get("date_jst") or "") == as_of.isoformat()

    if state.get("status") == "ACTIVE" and as_of < end:
        ingest_gpt_decision(state, as_of, cfg)
    fills = process_pending(state, as_of, cfg)
    mark_to_market(state, screen if data_fresh else pd.DataFrame(), as_of)

    drawdown = float(state["nav_jpy"]) / float(state["peak_nav_jpy"]) - 1 if state["peak_nav_jpy"] else 0.0
    if drawdown <= float(cfg["risk"]["portfolio_kill_switch_drawdown_pct"]):
        state["status"] = "KILL_SWITCH"
    if as_of >= end:
        state["status"] = "ENDED"
    if state["status"] != "ENDED":
        queue_mechanical_exits(state, as_of, cfg, regime)

    bench = benchmark_return(cfg, state, as_of)
    m = metrics(cfg, state, bench)
    record_equity(as_of, m)
    state["last_run_date"] = as_of.isoformat()
    write_json(state_path, state)

    latest = {
        "version": VERSION,
        "as_of_date": as_of.isoformat(),
        "status": state["status"],
        "data_fresh": data_fresh,
        "metrics": m,
        "regime": {
            "label": regime.get("regime_label"),
            "score": regime.get("regime_score"),
            "confidence": regime.get("confidence"),
        },
        "fills_today": fills,
        "pending_orders": state.get("pending_orders", []),
        "positions": list(state.get("positions", {}).values()),
    }
    write_json(OUT / "latest.json", latest)
    (OUT / "latest_report.md").write_text(build_report(as_of, cfg, state, m, fills), encoding="utf-8")
    print(json.dumps(latest, ensure_ascii=False, indent=2, default=str))
    return latest


if __name__ == "__main__":
    run()
