from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.portfolio_import import convert_file


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("destination", nargs="?", default="private/portfolio_latest.csv")
    args = p.parse_args()
    r = convert_file(Path(args.source), Path(args.destination))
    print(json.dumps({
        "status": "ok",
        "source_encoding": r.source_encoding,
        "rows_seen": r.rows_seen,
        "rows_kept": r.rows_kept,
        "destination": args.destination,
        "weight_sum": round(float(r.portfolio["weight"].sum()), 10),
        "market_value_total": float(r.portfolio["market_value"].sum()),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
