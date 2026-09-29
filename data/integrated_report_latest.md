# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-29T15:45:35+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 63.31
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.3799991607666
- Treasury realized-vol proxy (not ICE MOVE): 85.54 bps annualized; percentile=0.9365
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=41.7%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [JP] Mito Securities Co.,Ltd.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Norwood Financial Corp. - Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 3, 'WARNING': 2, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 発行登録書（株券､社債券等）
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / KDDIが自律型ネットワーク構想を発表、パロアルトと協業しSASE提供 - ZDNET Japan
- [WATCH] COMPANY_EVENT / NECグループの英国現代奴隷法への対応 : 企業情報 - group.nec
- [WATCH] COMPANY_EVENT / NECよどこへ行く 森田改革の成否 - xtech.nikkei.com

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. OKASAN SECURITIES GROUP INC. 8609.T | market_rank=1.0 | raw=74.8893359879362 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=74.84573140211728 | cross_pct=99.94858611825192
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=74.64879176683814 | cross_pct=99.89717223650385
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=73.4787063775807 | cross_pct=99.79434447300771
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=72.63196592151318 | cross_pct=99.6401028277635

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=83.97089148198145 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.74170840334254 | cross_pct=99.97063142437592
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.2494274743587 | cross_pct=99.94126284875183
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.0008827152939 | cross_pct=99.88252569750367
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.85704802598681 | cross_pct=99.85315712187959

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=83.97089148198145
- 2. [JP] OKASAN SECURITIES GROUP INC. | cross_pct=100.0 | raw=74.8893359879362
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97063142437592 | raw=83.74170840334254
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.94858611825192 | raw=74.84573140211728
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94126284875183 | raw=83.2494274743587
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89717223650385 | raw=74.64879176683814
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88252569750367 | raw=82.0008827152939
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85315712187959 | raw=81.85704802598681
- 9. [JP] Akatsuki Inc. | cross_pct=99.79434447300771 | raw=73.4787063775807
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73568281938327 | raw=80.87887052245995
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 227
- Eligible for model-change review: True
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

## 7. データ品質 / 反証
- Quality score: 0.745
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.0
- Secondary fundamental coverage: 1.0
- Effective fundamental coverage: 0.65
- Fundamental evidence tier: secondary_only
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは76.7点だが確認閾値未達
- 上位: ビットコイン 76.7 / テクノロジー 71.7 / スタンダード 65.5
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
