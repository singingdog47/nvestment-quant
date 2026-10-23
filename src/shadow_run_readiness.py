"""Non-trading control gates for paper accounts; preserve strategy rules and history."""
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")


def before_today_close(as_of: date, now: datetime | None = None) -> bool:
    current = (now or datetime.now(JST)).astimezone(JST)
    return as_of == current.date() and current.time() < time(15, 30)


def safe_flat_replay(as_of: date, state: dict, prior: dict, kind: str,
                     today: date | None = None) -> bool:
    """Only permit rerun of a failed *flat* current-session snapshot.

    Existing holdings, queued orders and any executed event veto replay, so
    same-session price marks and simulated fills cannot be applied twice.
    """
    today = today or datetime.now(JST).date()
    if as_of != today or prior.get("as_of_date") != as_of.isoformat():
        return False
    if state.get("positions") or state.get("pending_orders") or state.get("pending_buys"):
        return False
    if prior.get("positions") or prior.get("pending_orders") or prior.get("queued_buys"):
        return False
    if prior.get("fills_today") or prior.get("events") or prior.get("open_positions"):
        return False
    if kind == "v1":
        return prior.get("data_fresh") is False and not prior.get("priced_symbols")
    if kind == "v2":
        blockers = set(prior.get("market_data_blockers") or [])
        return bool(blockers & {"screen_outdated_no_new_trades", "regime_stale_or_non_actionable"})
    return False
