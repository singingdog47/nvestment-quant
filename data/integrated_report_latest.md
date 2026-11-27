# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-27T17:31:37+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **DEFENSIVE**
- Score: 33.69
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 24.889999389648438
- Treasury realized-vol proxy (not ICE MOVE): 100.661 bps annualized; percentile=0.9762
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=75.0%, short-interest=26.9%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] National Health Investors, Inc. Common Stock: SHORT_CROWDING
- [US] Ironwood Pharmaceuticals, Inc. - Class A Common Stock: SHORT_CROWDING
- [US] Radian Group Inc. Common Stock: SHORT_CROWDING
- [JP] コーエーテクモホールディングス: TIGHT_FLOAT
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=1, Brier=0.20249999999999996（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 25, 'WARNING': 9, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / ライフドリンクカンパニー[2585]：取締役等に対する譲渡制限付株式としての自己株式処分の払込完了に関するお知らせ 2026年7月24日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 日経平均が全面安の日に、なぜ東京海上（8766）は大商いで急反発したのか？発行済み9.6%の自社株買い、バフェット提携、業界初のAIロボット保険…“王者”に資金が殺到した本当の理由｜日本個別株デューデリジェンスセンター - note
- [WARNING] COMPANY_EVENT / 水戸証券[8622]：自己株式の取得状況に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2026年３月期決算短信〔日本基準〕（連結） 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：業績予想及び配当予想の修正に関するお知らせ 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] LIQUIDITY / Thin liquidity flag active

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. MAEZAWA Holdings CO.,LTD. 575A.T | market_rank=1.0 | raw=79.8912339228375 | cross_pct=100.0
- 2. MIZUHO MEDY CO.,LTD. 4595.T | market_rank=2.0 | raw=75.087148778453 | cross_pct=99.95054401582591
- 3. Strike Group Co.,Ltd. 6196.T | market_rank=3.0 | raw=74.89982515871733 | cross_pct=99.90108803165182
- 4. TRADERS HOLDINGS CO.,LTD. 8704.T | market_rank=4.0 | raw=73.77000808893469 | cross_pct=99.85163204747775
- 5. Mito Securities Co.,Ltd. 8622.T | market_rank=5.0 | raw=73.58009082200357 | cross_pct=99.80217606330366

### 米国株（市場内順位）
- 1. LTC Properties, Inc. Common Stock LTC | market_rank=1.0 | raw=84.28924716151286 | cross_pct=100.0
- 2. Carter Bankshares, Inc. - Common Stock CARE | market_rank=2.0 | raw=84.21739155810138 | cross_pct=99.9691548426897
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=82.30310910392697 | cross_pct=99.9383096853794
- 4. DHT Holdings, Inc. DHT | market_rank=4.0 | raw=81.78512351121552 | cross_pct=99.90746452806908
- 5. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=5.0 | raw=81.53564053879767 | cross_pct=99.87661937075879

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] LTC Properties, Inc. Common Stock | cross_pct=100.0 | raw=84.28924716151286
- 2. [JP] MAEZAWA Holdings CO.,LTD. | cross_pct=100.0 | raw=79.8912339228375
- 3. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=99.9691548426897 | raw=84.21739155810138
- 4. [JP] MIZUHO MEDY CO.,LTD. | cross_pct=99.95054401582591 | raw=75.087148778453
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.9383096853794 | raw=82.30310910392697
- 6. [US] DHT Holdings, Inc. | cross_pct=99.90746452806908 | raw=81.78512351121552
- 7. [JP] Strike Group Co.,Ltd. | cross_pct=99.90108803165182 | raw=74.89982515871733
- 8. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.87661937075879 | raw=81.53564053879767
- 9. [JP] TRADERS HOLDINGS CO.,LTD. | cross_pct=99.85163204747775 | raw=73.77000808893469
- 10. [US] River City Bank - Common stock | cross_pct=99.8149290561382 | raw=81.01821556637249
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 1248
- Eligible for model-change review: True
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] regime / DEFENSIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top10|1m: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは37.4点だが確認閾値未達
- 上位: スタンダード 37.4 / テクノロジー 32.3 / 金（ゴールド） 31.5
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
