from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class PTSObservation:
    code: str
    name: str
    regular_close: float
    pts_price: float
    volume: int
    turnover_jpy: float

    @property
    def move_pct(self) -> float:
        if not self.regular_close:
            return 0.0
        return (self.pts_price / self.regular_close - 1.0) * 100.0


def confidence(turnover_jpy: float, min_turnover: float, high_turnover: float) -> str:
    if turnover_jpy >= high_turnover:
        return "high"
    if turnover_jpy >= min_turnover:
        return "medium"
    return "low"


def evaluate(observations: Iterable[PTSObservation], config: dict) -> pd.DataFrame:
    t = config["thresholds"]
    rows = []
    for o in observations:
        move = o.move_pct
        conf = confidence(o.turnover_jpy, t["min_turnover_jpy"], t["high_confidence_turnover_jpy"])
        rows.append({
            "code": o.code,
            "name": o.name,
            "regular_close": o.regular_close,
            "pts_price": o.pts_price,
            "move_pct": round(move, 3),
            "volume": o.volume,
            "turnover_jpy": o.turnover_jpy,
            "confidence": conf,
            "alert": abs(move) >= t["absolute_move_pct"] and conf != "low",
        })
    return pd.DataFrame(rows)


def load_config(path: str | Path = "config/pts_observer_v1.json") -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def append_observations(frame: pd.DataFrame, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    header = not p.exists()
    frame.to_csv(p, mode="a", header=header, index=False)


def attach_forward_return(signals: pd.DataFrame, closes: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Research helper. closes columns: code, session, close; session is ordered per code."""
    out = signals.copy()
    if out.empty:
        out[f"forward_{horizon}s_pct"] = pd.Series(dtype=float)
        return out
    c = closes.sort_values(["code", "session"]).copy()
    c[f"future_close_{horizon}"] = c.groupby("code")["close"].shift(-horizon)
    c[f"forward_{horizon}s_pct"] = (c[f"future_close_{horizon}"] / c["close"] - 1) * 100
    return out.merge(
        c[["code", "session", f"forward_{horizon}s_pct"]],
        on=["code", "session"],
        how="left",
    )
