# Investment Quant Daily Integrated Report v2.7

Generated (UTC): 2026-08-28T21:38:59+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.71
- Confidence: 0.591
- VIX: 14.430000305175781
- Treasury realized-vol proxy (not ICE MOVE): 74.687 bps annualized; percentile=0.7659
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 7, 'WARNING': 10, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.42769981877436 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=76.99599864093628 | cross_pct=99.94884910485933
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=76.63949508772828 | cross_pct=99.89769820971867
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=76.09769019306856 | cross_pct=99.846547314578
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=72.74531806429434 | cross_pct=99.59079283887468

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.8999982598155 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.06926916183045 | cross_pct=99.9707516817783
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.97556278355327 | cross_pct=99.94150336355659
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=5.0 | raw=81.78110090441365 | cross_pct=99.88300672711318
- 5. First Busey Corporation - Common Stock BUSE | market_rank=7.0 | raw=81.03007547461876 | cross_pct=99.82451009066978

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.8999982598155
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.42769981877436
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.9707516817783 | raw=83.06926916183045
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94884910485933 | raw=76.99599864093628
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94150336355659 | raw=82.97556278355327
- 6. [JP] Akatsuki Inc. | cross_pct=99.89769820971867 | raw=76.63949508772828
- 7. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.88300672711318 | raw=81.78110090441365
- 8. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.846547314578 | raw=76.09769019306856
- 9. [US] First Busey Corporation - Common Stock | cross_pct=99.82451009066978 | raw=81.03007547461876
- 10. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.79526177244809 | raw=81.0106581613575
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
- Development: operational; stale-data reference mode and portfolio FX controls active
- Stable fallback branch: `stable-report-v2.6`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 9. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
