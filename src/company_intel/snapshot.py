from __future__ import annotations

from pathlib import Path
import pandas as pd

from .common import now_iso, SourceHealth

# Dedicated fundamentals are "primary/structured fundamentals".
FUNDAMENTAL_FILES = [
    "data/fundamentals_latest.csv",
    "data/intelligence/fundamentals_latest.csv",
]

# Screening contains useful fallback fields but must not be counted as a
# dedicated fundamentals feed merely because it has some valuation columns.
SCREENING_FILES = [
    "data/screening_latest.csv",
    "data/intelligence/screening_latest.csv",
]


def _read_source(p):
    try:
        return pd.read_csv(p, dtype=str)
    except Exception:
        return None


def _code_column(df):
    return next(
        (
            c
            for c in df.columns
            if str(c).lower() in ("code", "ticker", "銘柄コード", "symbol")
        ),
        None,
    )


def _normalize_code(df, code_col):
    tmp = df.copy()
    tmp["_code"] = (
        tmp[code_col]
        .astype(str)
        .str.extract(r"(\d{4})", expand=False)
        .fillna(tmp[code_col].astype(str))
    )
    return tmp


def _merge_file(base, p, suffix):
    df = _read_source(p)
    if df is None or df.empty:
        return base, None, []

    code_col = _code_column(df)
    if not code_col:
        return base, None, []

    tmp = _normalize_code(df, code_col)
    src_cols = [c for c in tmp.columns if c not in (code_col, "_code")]
    merged = base.merge(
        tmp.drop_duplicates("_code"),
        left_on="code",
        right_on="_code",
        how="left",
        suffixes=("", suffix),
    )
    return merged, p, src_cols


def _merge_existing(base):
    # 1) Dedicated fundamentals: only these can set fundamental_status="ok".
    for p in FUNDAMENTAL_FILES:
        if not Path(p).exists():
            continue
        merged, used, src_cols = _merge_file(base, p, "_fund")
        if used:
            available_cols = [c for c in src_cols if c in merged.columns]
            if available_cols:
                available = merged[available_cols].notna().any(axis=1)
                merged.loc[available, "fundamental_status"] = "ok"
            merged["fundamental_source_file"] = p
            merged["secondary_fundamental_status"] = "missing"
            merged["secondary_fundamental_source_file"] = ""
            return merged

    # 2) v1.3 screening is a fallback/reference snapshot, not primary
    # fundamentals. Keep the data, but do not inflate fundamental coverage.
    for p in SCREENING_FILES:
        if not Path(p).exists():
            continue
        merged, used, src_cols = _merge_file(base, p, "_screen")
        if used:
            available_cols = [c for c in src_cols if c in merged.columns]
            available = (
                merged[available_cols].notna().any(axis=1)
                if available_cols
                else pd.Series(False, index=merged.index)
            )
            merged.loc[available, "secondary_fundamental_status"] = "ok"
            merged["fundamental_source_file"] = ""
            merged["secondary_fundamental_source_file"] = p
            return merged

    base["fundamental_source_file"] = ""
    base["secondary_fundamental_status"] = "missing"
    base["secondary_fundamental_source_file"] = ""
    return base


def _yf_fallback(df, max_targets=40):
    try:
        import yfinance as yf
    except Exception as e:
        return df, SourceHealth(
            "yfinance", "missing", now_iso(), 0, str(e), "secondary"
        )

    rows = 0
    errors = []
    wanted = df[df["fundamental_status"] != "ok"].head(max_targets)

    for idx, r in wanted.iterrows():
        ticker = str(r.get("ticker", "")).strip()
        if not ticker:
            continue
        try:
            info = yf.Ticker(ticker).info or {}
            fields = {
                "yf_price": info.get("currentPrice")
                or info.get("regularMarketPrice"),
                "yf_market_cap": info.get("marketCap"),
                "yf_trailing_pe": info.get("trailingPE"),
                "yf_forward_pe": info.get("forwardPE"),
                "yf_pbr": info.get("priceToBook"),
                "yf_roe": info.get("returnOnEquity"),
                "yf_profit_margin": info.get("profitMargins"),
                "yf_revenue_growth": info.get("revenueGrowth"),
                "yf_earnings_growth": info.get("earningsGrowth"),
                "yf_dividend_yield": info.get("dividendYield"),
                "yf_beta": info.get("beta"),
            }
            for k, v in fields.items():
                df.loc[idx, k] = v

            if any(v is not None for v in fields.values()):
                df.loc[idx, "secondary_snapshot_status"] = "ok"
                df.loc[idx, "secondary_snapshot_source"] = "yfinance"
                rows += 1
        except Exception as e:
            errors.append(f"{ticker}:{type(e).__name__}")

    status = "ok" if not errors else ("partial" if rows else "error")
    return df, SourceHealth(
        "yfinance",
        status,
        now_iso(),
        rows,
        " | ".join(errors)[:1000],
        "secondary",
    )


def build_snapshot(targets, yfinance_enabled=True, yfinance_max_targets=40):
    base = targets.copy()
    base["fetched_at"] = now_iso()
    base["fundamental_status"] = "missing"
    base["secondary_snapshot_status"] = "missing"
    base["secondary_snapshot_source"] = ""
    base["secondary_fundamental_status"] = "missing"
    base["secondary_fundamental_source_file"] = ""

    merged = _merge_existing(base)

    if yfinance_enabled:
        return _yf_fallback(merged, yfinance_max_targets)

    return merged, SourceHealth(
        "yfinance", "disabled", now_iso(), 0, "", "secondary"
    )
