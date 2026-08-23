from __future__ import annotations

import os
from pathlib import Path

from private_drive import download_named, upload_or_replace
from portfolio_risk import main as run_risk


def main() -> None:
    private_dir = Path(os.getenv("PRIVATE_WORKDIR", ".private"))
    private_dir.mkdir(parents=True, exist_ok=True)
    portfolio_name = os.getenv("PORTFOLIO_DRIVE_FILENAME", "portfolio_latest.csv")
    local_portfolio = private_dir / "portfolio_latest.csv"
    download_named(portfolio_name, local_portfolio)
    os.environ["PORTFOLIO_PATH"] = str(local_portfolio)
    os.environ.setdefault("PRIVATE_OUTPUT_DIR", str(private_dir / "portfolio_risk"))
    run_risk()
    out_dir = Path(os.environ["PRIVATE_OUTPUT_DIR"])
    upload_or_replace(out_dir / "portfolio_risk_latest.json", "portfolio_risk_latest.json", "application/json")
    upload_or_replace(out_dir / "portfolio_risk_latest.md", "portfolio_risk_latest.md", "text/markdown")
    print("Private portfolio risk outputs updated in Google Drive.")


if __name__ == "__main__":
    main()
