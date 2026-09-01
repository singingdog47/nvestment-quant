# Investment Quant Daily Integrated Report v2.10

Generated (UTC): 2026-09-01T12:18:47+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `False`
- Overall analysis mode: `REVIEW_ONLY_PARTIAL_REGIME`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 61.54
- Confidence: 0.591
- Data status: partial
- Actionability reasons: confidence_below_threshold, core_credit_or_financial_conditions_missing
- VIX: 15.770000457763672
- Treasury realized-vol proxy (not ICE MOVE): 73.188 bps annualized; percentile=0.7421
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 9, 'WARNING': 2, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WATCH] COMPANY_EVENT / IIJ、1枚のSIMでNTTドコモ網とKDDI網を切り替え可能な「IIJマルチプロファイルSIM 2.0」を提供開始 | IIJについて - iij.ad.jp
- [WATCH] COMPANY_EVENT / 三菱商事とKDDI、コンテンツ配信サービス「ローソンビジョン」を活用したリテールメディア事業始動 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / KDDIと三菱商事、リテールメディア事業の新会社「クインタ」を設立 - ビジネスネットワーク
- [WATCH] COMPANY_EVENT / 京セラ本社に「オフィスローソン」が登場 KDDI社外では初の取り組み（ITmedia Mobile） - Yahoo!ニュース
- [WATCH] COMPANY_EVENT / 2 週間で 12 万人規模へ – NEC が Claude Desktop on Amazon Bedrock で実現したセキュアな全社 AI 環境 - aws.amazon.com
- [WATCH] COMPANY_EVENT / NEC無人のAI部署新設、「マネジャー」役が社員を生成して業務をこなす - 産経ニュース

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.6730809305048 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=77.23183902469941 | cross_pct=99.94892747701736
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=76.4001352267573 | cross_pct=99.89785495403473
- 4. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=76.36738870392954 | cross_pct=99.84678243105209
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=72.76263088250496 | cross_pct=99.59141981613891

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.93847637360523 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.22557567627625 | cross_pct=99.97081995914795
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.55649953884253 | cross_pct=99.94163991829589
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=5.0 | raw=81.87899243913269 | cross_pct=99.88327983659178
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=6.0 | raw=81.58444921504386 | cross_pct=99.85409979573971

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.93847637360523
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.6730809305048
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97081995914795 | raw=83.22557567627625
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94892747701736 | raw=77.23183902469941
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94163991829589 | raw=82.55649953884253
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89785495403473 | raw=76.4001352267573
- 7. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.88327983659178 | raw=81.87899243913269
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.85409979573971 | raw=81.58444921504386
- 9. [JP] Akatsuki Inc. | cross_pct=99.84678243105209 | raw=76.36738870392954
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.70819959147943 | raw=80.89745990253508
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 5. 過去判断の検証 / 学習
- Matured observations: 20
- Eligible for model-change review: False
- [INFO] regime / CONSTRUCTIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

## 8. 開発状況 / 復旧準備
- System version: v2.10
- Development: operational; private Drive history, valuation, monthly attribution v1.1, dynamic cash/tax friction and anti-FOMO execution controls active
- Stable fallback branch: `stable-report-v2.6`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 9. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
