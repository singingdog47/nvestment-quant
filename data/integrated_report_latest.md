# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-20T16:12:58+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **DEFENSIVE**
- Score: 33.96
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 30.030000686645508
- Treasury realized-vol proxy (not ICE MOVE): 106.356 bps annualized; percentile=0.9881
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=25.0%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] KDDI: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [JP] SHINAGAWA REFRA CO.,LTD.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
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
- Counts: {'INFO': 0, 'WATCH': 20, 'WARNING': 12, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 水戸証券(8622)、4期連続となる「増配」を発表し、配当利回り5.9％に！ 年間配当は4年で3.0倍に増加、2026年3月期は前期比13円増の｢1株あたり43円｣に！ - ダイヤモンド・オンライン
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 水戸証券[8622]：2027年３月期第２四半期（中間期）決算短信〔日本基準〕(非連結) 2026年10月29日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 訂正有価証券届出書（参照方式）
- [WARNING] COMPANY_EVENT / 訂正有価証券届出書（参照方式）

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. MAEZAWA Holdings CO.,LTD. 575A.T | market_rank=1.0 | raw=79.54625344444302 | cross_pct=100.0
- 2. Strike Group Co.,Ltd. 6196.T | market_rank=2.0 | raw=75.75014758105922 | cross_pct=99.9498997995992
- 3. MIZUHO MEDY CO.,LTD. 4595.T | market_rank=3.0 | raw=74.87476264729716 | cross_pct=99.8997995991984
- 4. Mito Securities Co.,Ltd. 8622.T | market_rank=4.0 | raw=73.95208798558035 | cross_pct=99.8496993987976
- 5. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=72.93194658615718 | cross_pct=99.79959919839679

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.73008590629814 | cross_pct=100.0
- 2. LTC Properties, Inc. Common Stock LTC | market_rank=2.0 | raw=84.37128072061492 | cross_pct=99.96869129618034
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=82.97718105925757 | cross_pct=99.93738259236068
- 4. Horizon Bancorp, Inc. - Common Stock HBNC | market_rank=4.0 | raw=82.55063423963179 | cross_pct=99.90607388854102
- 5. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=5.0 | raw=82.41576752230944 | cross_pct=99.87476518472135

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.73008590629814
- 2. [JP] MAEZAWA Holdings CO.,LTD. | cross_pct=100.0 | raw=79.54625344444302
- 3. [US] LTC Properties, Inc. Common Stock | cross_pct=99.96869129618034 | raw=84.37128072061492
- 4. [JP] Strike Group Co.,Ltd. | cross_pct=99.9498997995992 | raw=75.75014758105922
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.93738259236068 | raw=82.97718105925757
- 6. [US] Horizon Bancorp, Inc. - Common Stock | cross_pct=99.90607388854102 | raw=82.55063423963179
- 7. [JP] MIZUHO MEDY CO.,LTD. | cross_pct=99.8997995991984 | raw=74.87476264729716
- 8. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.87476518472135 | raw=82.41576752230944
- 9. [JP] Mito Securities Co.,Ltd. | cross_pct=99.8496993987976 | raw=73.95208798558035
- 10. [US] DHT Holdings, Inc. | cross_pct=99.81214777708203 | raw=81.6425474893419
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 1100
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは31.9点だが確認閾値未達
- 上位: スタンダード 31.9 / 金（ゴールド） 31.0 / テクノロジー 26.6
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
