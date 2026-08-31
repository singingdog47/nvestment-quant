# Investment Quant Daily Integrated Report v2.7

Generated (UTC): 2026-08-31T07:29:31+00:00

## 1. 結論 / 今日の優先アクション
- **SELECTIVE REVIEW OF TOP CANDIDATES**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Data actionable: `True`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.88
- Confidence: 0.591
- VIX: 14.430000305175781
- Treasury realized-vol proxy (not ICE MOVE): 74.687 bps annualized; percentile=0.7659
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WATCH**
- Counts: {'INFO': 0, 'WATCH': 6, 'WARNING': 0, 'CRITICAL': 0}
- [WATCH] COMPANY_EVENT / ＫＤＤＩ(株)【9433】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
- [WATCH] COMPANY_EVENT / KDDI の ISP 事業者向けメールシステムへの不正アクセス、レンタルサーバCPIへの影響が明らかに - ScanNetSecurity
- [WATCH] COMPANY_EVENT / 【日本】KDDI等6社、バッテリーリサイクルで新規資源同等の性能実現。サーキュラー | Sustainable Japan | 世界のサステナビリティ・ESG投資・SDGs - Sustainable Japan
- [WATCH] COMPANY_EVENT / ＮＥＣ【6701】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
- [WATCH] COMPANY_EVENT / NECグループ、「国際物流総合展2026」に出展 - PR TIMES
- [WATCH] COMPANY_EVENT / NEC、SCM業務を自律実行する「NEC SCM AIエージェント」を9月より販売開始 需要予測や生産計画の最適化などを自動化 - クラウド Watch

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.5079576573533 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=77.1932075915799 | cross_pct=99.94910941475827
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=76.49990108752799 | cross_pct=99.89821882951654
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=76.24082778613649 | cross_pct=99.79643765903307
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=72.79206970379795 | cross_pct=99.59287531806615

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.90532373324889 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.06097294083133 | cross_pct=99.97076023391813
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.9925454417412 | cross_pct=99.94152046783626
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=5.0 | raw=81.78511670163559 | cross_pct=99.88304093567251
- 5. First Busey Corporation - Common Stock BUSE | market_rank=7.0 | raw=81.02284974942003 | cross_pct=99.82456140350877

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.90532373324889
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.5079576573533
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97076023391813 | raw=83.06097294083133
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94910941475827 | raw=77.1932075915799
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94152046783626 | raw=82.9925454417412
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89821882951654 | raw=76.49990108752799
- 7. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.88304093567251 | raw=81.78511670163559
- 8. [US] First Busey Corporation - Common Stock | cross_pct=99.82456140350877 | raw=81.02284974942003
- 9. [JP] Akatsuki Inc. | cross_pct=99.79643765903307 | raw=76.24082778613649
- 10. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.79532163742691 | raw=81.00894401818664
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 5. 過去判断の検証 / 学習
- Matured observations: 12
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
