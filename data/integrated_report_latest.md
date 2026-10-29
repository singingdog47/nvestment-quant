# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-29T14:26:09+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 53.3
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.65999984741211
- Treasury realized-vol proxy (not ICE MOVE): 84.03 bps annualized; percentile=0.8413
- Flags: THIN_LIQUIDITY

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.2%, short-interest=25.0%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] KeePer Technical Laboratory Co.,Ltd.: TIGHT_FLOAT|HIGH_FLOAT_TURNOVER|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION|TIGHT_FLOAT_HIGH_TURNOVER
- [JP] コーエーテクモホールディングス: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] NEC: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [JP] KDDI: VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: RANGE_OR_UNDECIDED; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_UNDECIDED; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 24, 'WARNING': 19, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 東京海上ホールディングス[8766]：株式分割、株主優待制度の導入、株式分割に伴う定款の一部変更、配当予想の修正および自己株式取得に係る事項の変更に関するお知らせ 2026年8月25日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=80.02085583104324 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=77.5772264469597 | cross_pct=99.94895354772844
- 3. Toranvia Co.,Ltd. 545A.T | market_rank=4.0 | raw=74.04209558707976 | cross_pct=99.8468606431853
- 4. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=73.36976462634544 | cross_pct=99.79581419091373
- 5. Akatsuki Inc. 3932.T | market_rank=6.0 | raw=72.7364112352089 | cross_pct=99.74476773864215

### 米国株（市場内順位）
- 1. Scorpio Tankers Inc. Common Shares STNG | market_rank=1.0 | raw=84.60568765755718 | cross_pct=100.0
- 2. Carter Bankshares, Inc. - Common Stock CARE | market_rank=2.0 | raw=84.59739993181459 | cross_pct=99.96996996996998
- 3. Horizon Bancorp, Inc. - Common Stock HBNC | market_rank=3.0 | raw=82.8646847891432 | cross_pct=99.93993993993993
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=82.40210962349806 | cross_pct=99.84984984984985
- 5. DHT Holdings, Inc. DHT | market_rank=7.0 | raw=82.26720201333518 | cross_pct=99.81981981981983

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Scorpio Tankers Inc. Common Shares | cross_pct=100.0 | raw=84.60568765755718
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=80.02085583104324
- 3. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=99.96996996996998 | raw=84.59739993181459
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94895354772844 | raw=77.5772264469597
- 5. [US] Horizon Bancorp, Inc. - Common Stock | cross_pct=99.93993993993993 | raw=82.8646847891432
- 6. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.84984984984985 | raw=82.40210962349806
- 7. [JP] Toranvia Co.,Ltd. | cross_pct=99.8468606431853 | raw=74.04209558707976
- 8. [US] DHT Holdings, Inc. | cross_pct=99.81981981981983 | raw=82.26720201333518
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.79581419091373 | raw=73.36976462634544
- 10. [JP] Akatsuki Inc. | cross_pct=99.74476773864215 | raw=72.7364112352089
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 759
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] action / REVIEW|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.864
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.365
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.865
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **REVIEW_LEADER** — スタンダードが72.9点、2位との差12.0点。週次レビュー候補
- 上位: スタンダード 72.9 / テクノロジー 60.9 / ビットコイン 46.5
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
