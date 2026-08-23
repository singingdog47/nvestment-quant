from __future__ import annotations

import json
import os
from pathlib import Path

from portfolio_import import parse_rakuten_csv_bytes
from private_drive import download_recent_csvs, upload_or_replace
from portfolio_risk import main as run_risk


def _build_latest_portfolio(private_dir: Path) -> tuple[Path, dict]:
    inbox = private_dir / "drive_inbox"
    candidates = download_recent_csvs(inbox, limit=int(os.getenv("PORTFOLIO_SCAN_LIMIT", "25")))
    errors: list[dict] = []
    for path, meta in candidates:
        # Generated normalized/output CSV files are harmless: the Rakuten parser
        # rejects them because they lack the Japanese holdings-detail header.
        try:
            parsed = parse_rakuten_csv_bytes(path.read_bytes())
        except Exception as e:
            errors.append({"name": meta.get("name"), "error": f"{type(e).__name__}:{e}"})
            continue
        local = private_dir / "portfolio_latest.csv"
        parsed.portfolio.to_csv(local, index=False, encoding="utf-8")
        manifest = {
            "status": "ok",
            "source_file": meta.get("name"),
            "source_modified_time": meta.get("modifiedTime"),
            "source_encoding": parsed.source_encoding,
            "rows_seen": parsed.rows_seen,
            "rows_kept": parsed.rows_kept,
            "market_value_total": float(parsed.portfolio["market_value"].sum()),
            "weight_sum": float(parsed.portfolio["weight"].sum()),
        }
        (private_dir / "portfolio_import_latest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return local, manifest
    raise FileNotFoundError(
        "No valid Rakuten Securities holdings CSV found in private Drive folder. "
        f"Checked {len(candidates)} CSV/text files; sample errors={errors[:5]}"
    )


def main() -> None:
    private_dir = Path(os.getenv("PRIVATE_WORKDIR", ".private"))
    private_dir.mkdir(parents=True, exist_ok=True)

    local_portfolio, manifest = _build_latest_portfolio(private_dir)
    # Save the normalized input back to Drive so the latest machine-readable
    # portfolio is visible there, while never committing it to the public repo.
    upload_or_replace(local_portfolio, "portfolio_latest.csv", "text/csv")
    upload_or_replace(private_dir / "portfolio_import_latest.json", "portfolio_import_latest.json", "application/json")

    os.environ["PORTFOLIO_PATH"] = str(local_portfolio)
    os.environ.setdefault("PRIVATE_OUTPUT_DIR", str(private_dir / "portfolio_risk"))
    run_risk()

    out_dir = Path(os.environ["PRIVATE_OUTPUT_DIR"])
    upload_or_replace(out_dir / "portfolio_risk_latest.json", "portfolio_risk_latest.json", "application/json")
    upload_or_replace(out_dir / "portfolio_risk_latest.md", "portfolio_risk_latest.md", "text/markdown")
    print(json.dumps({"status": "ok", "portfolio_import": manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
