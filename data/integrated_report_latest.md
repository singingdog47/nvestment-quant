# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-19T16:38:00+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **DEFENSIVE**
- Score: 35.47
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 25.34000015258789
- Treasury realized-vol proxy (not ICE MOVE): 106.012 bps annualized; percentile=0.9841
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=23.1%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
- [JP] コーエーテクモホールディングス: TIGHT_FLOAT
- [JP] ライフドリンク カンパニー: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_INTEREST_RISING

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=1, Brier=0.20249999999999996（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 24, 'WARNING': 9, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 信越化学工業－反発 1000万株・500億円を上限に自社株買い 割合0.55％(トレーダーズ・ウェブ) - Yahoo!ファイナンス
- [WARNING] COMPANY_EVENT / 東京海上ホールディングス[8766]：自己株式取得に係る事項の決定に関するお知らせ 2026年11月19日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 半期報告書－第25期(2026/04/01－2027/03/31)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] COMPANY_EVENT / 決算:浜松ホトニクス、26年9月期の純利益23%増 半導体関連伸び上方修正 - 日本経済新聞
- [WARNING] LIQUIDITY / Thin liquidity flag active

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. MAEZAWA Holdings CO.,LTD. 575A.T | market_rank=1.0 | raw=79.58966448547972 | cross_pct=100.0
- 2. Strike Group Co.,Ltd. 6196.T | market_rank=2.0 | raw=75.8466392670235 | cross_pct=99.9501246882793
- 3. MIZUHO MEDY CO.,LTD. 4595.T | market_rank=3.0 | raw=74.45069947711517 | cross_pct=99.9002493765586
- 4. Mito Securities Co.,Ltd. 8622.T | market_rank=4.0 | raw=73.56054542268669 | cross_pct=99.85037406483791
- 5. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=73.45369857043326 | cross_pct=99.80049875311721

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.61641543836927 | cross_pct=100.0
- 2. LTC Properties, Inc. Common Stock LTC | market_rank=2.0 | raw=83.4691866283678 | cross_pct=99.96892479801119
- 3. Horizon Bancorp, Inc. - Common Stock HBNC | market_rank=3.0 | raw=82.60917384966267 | cross_pct=99.93784959602237
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=4.0 | raw=82.51623565085264 | cross_pct=99.90677439403356
- 5. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=5.0 | raw=82.02695482401055 | cross_pct=99.87569919204475

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.61641543836927
- 2. [JP] MAEZAWA Holdings CO.,LTD. | cross_pct=100.0 | raw=79.58966448547972
- 3. [US] LTC Properties, Inc. Common Stock | cross_pct=99.96892479801119 | raw=83.4691866283678
- 4. [JP] Strike Group Co.,Ltd. | cross_pct=99.9501246882793 | raw=75.8466392670235
- 5. [US] Horizon Bancorp, Inc. - Common Stock | cross_pct=99.93784959602237 | raw=82.60917384966267
- 6. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.90677439403356 | raw=82.51623565085264
- 7. [JP] MIZUHO MEDY CO.,LTD. | cross_pct=99.9002493765586 | raw=74.45069947711517
- 8. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.87569919204475 | raw=82.02695482401055
- 9. [JP] Mito Securities Co.,Ltd. | cross_pct=99.85037406483791 | raw=73.56054542268669
- 10. [JP] ELECOM CO.,LTD. | cross_pct=99.80049875311721 | raw=73.45369857043326
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 1095
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] action / REVIEW|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.838
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.308
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.808
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは36.5点だが確認閾値未達
- 上位: スタンダード 36.5 / テクノロジー 33.2 / 金（ゴールド） 31.4
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
