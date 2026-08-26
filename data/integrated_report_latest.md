# Investment Quant Daily Integrated Report v2.7

Generated (UTC): 2026-08-26T09:31:12+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.8
- Confidence: 0.591
- VIX: 15.699999809265137
- Treasury realized-vol proxy (not ICE MOVE): 74.197 bps annualized; percentile=0.7421
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 7, 'WARNING': 8, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2026年３月期決算短信〔日本基準〕（連結） 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 有価証券報告書－第13期(2025/06/01－2026/05/31)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] COMPANY_EVENT / 内部統制報告書－第13期(2025/06/01－2026/05/31)

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=78.0545208825716 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=76.86264186607485 | cross_pct=99.94850669412976
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=76.65736138209037 | cross_pct=99.89701338825952
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=75.7414366709513 | cross_pct=99.8455200823893
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=72.67210077047392 | cross_pct=99.58805355303811

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.04635506197343 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.40898788527065 | cross_pct=99.97087095834547
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.22007997396706 | cross_pct=99.94174191669094
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=5.0 | raw=81.53040648522332 | cross_pct=99.88348383338189
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=6.0 | raw=81.37520749883905 | cross_pct=99.85435479172735

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.04635506197343
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=78.0545208825716
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97087095834547 | raw=83.40898788527065
- 4. [JP] Akatsuki Inc. | cross_pct=99.94850669412976 | raw=76.86264186607485
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94174191669094 | raw=83.22007997396706
- 6. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.89701338825952 | raw=76.65736138209037
- 7. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.88348383338189 | raw=81.53040648522332
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.85435479172735 | raw=81.37520749883905
- 9. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.8455200823893 | raw=75.7414366709513
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.76696766676376 | raw=80.95216089129194
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
