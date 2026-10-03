# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-03T00:22:53+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 68.65
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.3100004196167
- Treasury realized-vol proxy (not ICE MOVE): 90.387 bps annualized; percentile=0.9643
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.2%, short-interest=28.8%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] Norwood Financial Corp. - Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 0, 'WARNING': 1, 'CRITICAL': 0}
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=75.07058339824687 | cross_pct=100.0
- 2. IwaiCosmo Holdings,Inc. 8707.T | market_rank=2.0 | raw=74.49861051553215 | cross_pct=99.94821336095288
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=74.46374509899414 | cross_pct=99.89642672190575
- 4. Tokai Tokyo Financial Holdings,Inc. 8616.T | market_rank=4.0 | raw=74.28128670401912 | cross_pct=99.84464008285863
- 5. ELECOM CO.,LTD. 6750.T | market_rank=7.0 | raw=72.5033827161758 | cross_pct=99.68928016571724

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.69684105926085 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.78869904182535 | cross_pct=99.97064866451424
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.15433867884956 | cross_pct=99.94129732902847
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.0856678744423 | cross_pct=99.88259465805695
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=7.0 | raw=81.39869713426933 | cross_pct=99.82389198708542

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.69684105926085
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=75.07058339824687
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97064866451424 | raw=83.78869904182535
- 4. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.94821336095288 | raw=74.49861051553215
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94129732902847 | raw=83.15433867884956
- 6. [JP] Akatsuki Inc. | cross_pct=99.89642672190575 | raw=74.46374509899414
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88259465805695 | raw=82.0856678744423
- 8. [JP] Tokai Tokyo Financial Holdings,Inc. | cross_pct=99.84464008285863 | raw=74.28128670401912
- 9. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.82389198708542 | raw=81.39869713426933
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73583798062812 | raw=80.89611863598716
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 266
- Eligible for model-change review: True
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

## 7. データ品質 / 反証
- Quality score: 0.735
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.077
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.577
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは78.2点だが確認閾値未達
- 上位: ビットコイン 78.2 / テクノロジー 72.9 / スタンダード 65.9
- 数か月スイングのため日次は監視、週次でまとめて再評価。WAITを常に有効な選択肢とします。
- 暗号資産コースはスプレッド負担をコストスコアに反映しています。
<!-- PAYPAY_SWING_END -->

## 9. 開発状況 / 復旧準備
- System version: v2.13
- Development: operational; private Drive history, valuation, monthly attribution v1.1, dynamic cash/tax friction, anti-FOMO execution controls, PayPay swing research monitor, non-directional major-SQ execution timing overlay, and monitored-security supply/demand context active
- Stable fallback branch: `stable-report-v2.6`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 10. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
