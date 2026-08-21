# v1.3 → v1.6 チェックリスト

- [ ] v1.3のバックアップを取得
- [ ] `.github/workflows/intelligence-v1.6.yml` を追加
- [ ] `.github/workflows/market-regime-v1.5-manual.yml` を追加
- [ ] `src/market_regime/` と `src/company_intel/` を追加
- [ ] `requirements-regime.txt` と `requirements-intelligence.txt` を追加
- [ ] `config/market_regime_v1_5.yml` / `intelligence_v1_6.yml` / `policy_v1_6.yml` を追加
- [ ] `python tools/preflight_v1_3.py` でv1.3検出を確認
- [ ] Actionsから `Investment Intelligence v1.6` を手動実行
- [ ] `data/regime/market_regime_latest.json` を確認
- [ ] `data/intelligence/ai_context_latest.md` を確認
- [ ] `data/intelligence/data_quality_latest.json` の `actionable` を確認
- [ ] `source_health_latest.csv` の missing/errorを確認
- [ ] v1.3の `Daily Quant Screen` が従来どおり成功することを確認
- [ ] 翌営業日に16:17→16:30の連携を確認
