from __future__ import annotations

import os
from dataclasses import dataclass


def _int(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _float(name: str, default: float) -> float:
    return float(os.getenv(name, str(default)))


@dataclass(frozen=True)
class Settings:
    output_top_n: int = _int("OUTPUT_TOP_N", 100)
    max_tickers: int = _int("MAX_TICKERS", 0)
    min_price_jp: float = _float("MIN_PRICE_JP", 100.0)
    min_price_us: float = _float("MIN_PRICE_US", 2.0)
    min_turnover_jp: float = _float("MIN_TURNOVER_JP", 50_000_000.0)
    min_turnover_us: float = _float("MIN_TURNOVER_US", 1_000_000.0)
    request_timeout: int = _int("REQUEST_TIMEOUT", 30)
    http_user_agent: str = os.getenv(
        "HTTP_USER_AGENT", "investment-quant-v1.2 personal-research"
    )


SETTINGS = Settings()
