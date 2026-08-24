# Investment Quant Daily Integrated Report v2.7

Generated (UTC): 2026-08-24T09:37:28+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 66.14
- Confidence: 1.0
- VIX: 15.880000114440918
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 5, 'WARNING': 46, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=78.2615255078952 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=77.16145496087536 | cross_pct=99.94858611825192
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=76.87931932783377 | cross_pct=99.89717223650385
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=75.53241297481537 | cross_pct=99.84575835475579
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.75472140168148 | cross_pct=99.6401028277635

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.95646270258446 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=83.39904336876124 | cross_pct=99.97088791848617
- 3. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=3.0 | raw=83.27375232616615 | cross_pct=99.94177583697234
- 4. DHT Holdings, Inc. DHT | market_rank=4.0 | raw=82.15424266835396 | cross_pct=99.91266375545852
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=81.8325732262159 | cross_pct=99.88355167394468

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.95646270258446
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=78.2615255078952
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.97088791848617 | raw=83.39904336876124
- 4. [JP] Akatsuki Inc. | cross_pct=99.94858611825192 | raw=77.16145496087536
- 5. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.94177583697234 | raw=83.27375232616615
- 6. [US] DHT Holdings, Inc. | cross_pct=99.91266375545852 | raw=82.15424266835396
- 7. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.89717223650385 | raw=76.87931932783377
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88355167394468 | raw=81.8325732262159
- 9. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.84575835475579 | raw=75.53241297481537
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.7962154294032 | raw=81.1780061563162
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
- Missing data must not be converted into unsupported buy/sell conclusions.

## 7. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private portfolio risk engine が成功した場合、私有版レポートに統合します。

## 8. 開発状況 / 復旧準備
- System version: v2.7
- Development: operational; human-readable mobile brief and portfolio narrative added
- Stable fallback branch: `stable-report-v2.6`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 9. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
