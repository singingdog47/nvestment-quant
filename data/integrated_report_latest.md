# Investment Quant Daily Integrated Report v2.6

Generated (UTC): 2026-08-24T00:37:43+00:00

## 1. 結論 / 今日の優先アクション
- **SELECTIVE REVIEW OF TOP CANDIDATES**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 67.78
- Confidence: 1.0
- VIX: 15.130000114440918
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WATCH**
- Counts: {'INFO': 0, 'WATCH': 2, 'WARNING': 0, 'CRITICAL': 0}
- [WATCH] COMPANY_EVENT / ＫＤＤＩ(株)【9433】：株主優待 - Yahoo!ファイナンス
- [WATCH] LIQUIDITY / Market liquidity is soft

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=78.27513949128851 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=77.07931565069734 | cross_pct=99.94824016563147
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=76.74172501857534 | cross_pct=99.89648033126294
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=75.524468993253 | cross_pct=99.84472049689441
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=73.39189872270546 | cross_pct=99.58592132505176

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.95185196839473 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=83.39530063817661 | cross_pct=99.97086247086247
- 3. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=3.0 | raw=83.26870811641626 | cross_pct=99.94172494172494
- 4. DHT Holdings, Inc. DHT | market_rank=4.0 | raw=82.1512961019224 | cross_pct=99.91258741258741
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=81.82820847088966 | cross_pct=99.88344988344988

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.95185196839473
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=78.27513949128851
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.97086247086247 | raw=83.39530063817661
- 4. [JP] Akatsuki Inc. | cross_pct=99.94824016563147 | raw=77.07931565069734
- 5. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.94172494172494 | raw=83.26870811641626
- 6. [US] DHT Holdings, Inc. | cross_pct=99.91258741258741 | raw=82.1512961019224
- 7. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.89648033126294 | raw=76.74172501857534
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88344988344988 | raw=81.82820847088966
- 9. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.84472049689441 | raw=75.524468993253
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.7960372960373 | raw=81.1734457614353
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 5. 過去判断の検証 / 学習
- Matured observations: 0
- Eligible for model-change review: False

## 6. データ品質 / 反証
- Quality score: 0.745
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.0
- Secondary fundamental coverage: 1.0
- Effective fundamental coverage: 0.65
- Fundamental evidence tier: secondary_only
- Optional primary feeds not configured (confidence booster; not a hard decision blocker):
  - EDINET: EDINET_API_KEY not set
  - SEC: SEC_USER_AGENT not set
- Missing data must not be converted into unsupported buy/sell conclusions.

## 7. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private portfolio risk engine が成功した場合、私有版レポートに統合します。

## 8. 開発状況 / 復旧準備
- System version: v2.6
- Development: operational; cross-market score calibration and report-status visibility added
- Stable fallback branch: `stable-report-v2.5`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 9. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
