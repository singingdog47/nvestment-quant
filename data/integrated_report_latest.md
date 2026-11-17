# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-17T16:57:18+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **DEFENSIVE**
- Score: 37.01
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 26.5
- Treasury realized-vol proxy (not ICE MOVE): 107.315 bps annualized; percentile=0.996
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.2%, short-interest=23.1%, current/average volume=76.9%
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
- Counts: {'INFO': 0, 'WATCH': 28, 'WARNING': 4, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 信越化学、自社株買いを500億円上積み 27年3月期の還元総額3000億円へ - BigGo ファイナンス
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] LIQUIDITY / Thin liquidity flag active
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / ＦＯＯＤ＆ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ[3563]：2026年9月期 通期 決算説明資料 2026年11月6日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WATCH] COMPANY_EVENT / 「AQUOS sense11」をauから11月26日に発売 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / ispaceとの連携をNTT・KDDIが相次ぎ発表｜各社の技術と月面インフラ構想を解説 - SPACE CONNECT
- [WATCH] COMPANY_EVENT / KDDIなど、5G対応スマホ「AQUOS sense11」をauから発売 - 日本経済新聞

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Toranvia Co.,Ltd. 545A.T | market_rank=1.0 | raw=76.82827048763203 | cross_pct=100.0
- 2. Strike Group Co.,Ltd. 6196.T | market_rank=2.0 | raw=75.92108581143017 | cross_pct=99.95014955134596
- 3. MIZUHO MEDY CO.,LTD. 4595.T | market_rank=3.0 | raw=74.75911769466765 | cross_pct=99.90029910269193
- 4. ELECOM CO.,LTD. 6750.T | market_rank=4.0 | raw=73.56075777865016 | cross_pct=99.85044865403788
- 5. Mito Securities Co.,Ltd. 8622.T | market_rank=5.0 | raw=73.55915153410982 | cross_pct=99.80059820538385

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.1323345681581 | cross_pct=100.0
- 2. LTC Properties, Inc. Common Stock LTC | market_rank=2.0 | raw=83.4106881443743 | cross_pct=99.9689633767846
- 3. Horizon Bancorp, Inc. - Common Stock HBNC | market_rank=3.0 | raw=82.66827268812722 | cross_pct=99.9379267535692
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=4.0 | raw=82.3690598269219 | cross_pct=99.90689013035382
- 5. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=5.0 | raw=81.91001364903444 | cross_pct=99.87585350713843

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.1323345681581
- 2. [JP] Toranvia Co.,Ltd. | cross_pct=100.0 | raw=76.82827048763203
- 3. [US] LTC Properties, Inc. Common Stock | cross_pct=99.9689633767846 | raw=83.4106881443743
- 4. [JP] Strike Group Co.,Ltd. | cross_pct=99.95014955134596 | raw=75.92108581143017
- 5. [US] Horizon Bancorp, Inc. - Common Stock | cross_pct=99.9379267535692 | raw=82.66827268812722
- 6. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.90689013035382 | raw=82.3690598269219
- 7. [JP] MIZUHO MEDY CO.,LTD. | cross_pct=99.90029910269193 | raw=74.75911769466765
- 8. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.87585350713843 | raw=81.91001364903444
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.85044865403788 | raw=73.56075777865016
- 10. [JP] Mito Securities Co.,Ltd. | cross_pct=99.80059820538385 | raw=73.55915153410982
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 1080
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは36.7点だが確認閾値未達
- 上位: スタンダード 36.7 / 金（ゴールド） 34.8 / テクノロジー 32.2
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
