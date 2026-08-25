# Investment Quant Daily Integrated Report v2.7

Generated (UTC): 2026-08-25T09:24:51+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 59.29
- Confidence: 0.591
- VIX: 15.789999961853027
- Treasury realized-vol proxy (not ICE MOVE): 72.293 bps annualized; percentile=0.6984
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 12, 'WARNING': 7, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WATCH] COMPANY_EVENT / povo、「5G SA（スタンドアローン）」サービスを提供開始 - KDDI ニュースルーム

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=78.25171949217419 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=77.00253256333092 | cross_pct=99.94850669412976
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=76.6744030323236 | cross_pct=99.89701338825952
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=5.0 | raw=75.538932687693 | cross_pct=99.79402677651905
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.81741994457258 | cross_pct=99.63954685890835

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.970492494165 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=83.2847501708291 | cross_pct=99.97083697871099
- 3. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=3.0 | raw=83.15332889864739 | cross_pct=99.94167395742198
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=81.93907464508197 | cross_pct=99.88334791484398
- 5. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=6.0 | raw=81.51773332201557 | cross_pct=99.85418489355497

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.970492494165
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=78.25171949217419
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.97083697871099 | raw=83.2847501708291
- 4. [JP] Akatsuki Inc. | cross_pct=99.94850669412976 | raw=77.00253256333092
- 5. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.94167395742198 | raw=83.15332889864739
- 6. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.89701338825952 | raw=76.6744030323236
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88334791484398 | raw=81.93907464508197
- 8. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.85418489355497 | raw=81.51773332201557
- 9. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.79402677651905 | raw=75.538932687693
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.70836978710994 | raw=81.22053545677689
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
