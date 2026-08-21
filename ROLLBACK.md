# Rollback

v1.6は追加型なので、問題があれば以下だけを削除すればv1.3へ戻せます。

- `.github/workflows/intelligence-v1.6.yml`
- `.github/workflows/market-regime-v1.5-manual.yml`
- `src/market_regime/`
- `src/company_intel/`
- `src/run_market_regime.py`
- `src/run_company_intel.py`
- `requirements-regime.txt`
- `requirements-intelligence.txt`
- `config/market_regime_v1_5.yml`
- `config/intelligence_v1_6.yml`
- `config/policy_v1_6.yml`
- `config/intelligence_watchlist.csv`
- `config/company_sources_v1_6.csv`
- `data/regime/`
- `data/intelligence/`
- `data/state/`

v1.3の既存workflow/src/dataは変更しないため、ロールバックで復元作業を最小化できます。
