# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-06T15:07:54+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **DEFENSIVE**
- Score: 39.99
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 24.290000915527344
- Treasury realized-vol proxy (not ICE MOVE): 85.159 bps annualized; percentile=0.8532
- Flags: THIN_LIQUIDITY

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=23.1%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] 信越化学工業: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] KDDI: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] NEC: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] 浜松ホトニクス: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] ライフドリンク カンパニー: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [JP] FOOD & LIFE COMPANIES: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Financial Institutions, Inc. - Common Stock: SHORT_CROWDING
- [JP] Strike Group Co.,Ltd.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: RANGE_OR_UNDECIDED; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_UNDECIDED; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=1, Brier=0.20249999999999996（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 22, 'WARNING': 8, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / ＫＤＤＩ[9433]：自己株式の取得状況に関するお知らせ 2026年11月6日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 半期報告書－第22期(2026/04/01－2026/09/30)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WARNING] COMPANY_EVENT / 半期報告書－第28期(2026/04/01－2027/03/31)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WARNING] LIQUIDITY / Thin liquidity flag active

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Toranvia Co.,Ltd. 545A.T | market_rank=1.0 | raw=75.1559294571698 | cross_pct=100.0
- 2. Strike Group Co.,Ltd. 6196.T | market_rank=2.0 | raw=73.50183606128718 | cross_pct=99.94949494949495
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=73.33081849714675 | cross_pct=99.8989898989899
- 4. Mito Securities Co.,Ltd. 8622.T | market_rank=4.0 | raw=73.08270901063638 | cross_pct=99.84848484848486
- 5. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=73.01278959211145 | cross_pct=99.79797979797979

### 米国株（市場内順位）
- 1. LTC Properties, Inc. Common Stock LTC | market_rank=1.0 | raw=85.3410511240247 | cross_pct=100.0
- 2. Financial Institutions, Inc. - Common Stock FISI | market_rank=2.0 | raw=84.64791511895389 | cross_pct=99.96938150642988
- 3. Carter Bankshares, Inc. - Common Stock CARE | market_rank=3.0 | raw=83.91181519398195 | cross_pct=99.93876301285977
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=5.0 | raw=82.7137311437538 | cross_pct=99.87752602571953
- 5. TORM plc - Class A Common Stock TRMD | market_rank=9.0 | raw=82.15038160254315 | cross_pct=99.75505205143907

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] LTC Properties, Inc. Common Stock | cross_pct=100.0 | raw=85.3410511240247
- 2. [JP] Toranvia Co.,Ltd. | cross_pct=100.0 | raw=75.1559294571698
- 3. [US] Financial Institutions, Inc. - Common Stock | cross_pct=99.96938150642988 | raw=84.64791511895389
- 4. [JP] Strike Group Co.,Ltd. | cross_pct=99.94949494949495 | raw=73.50183606128718
- 5. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=99.93876301285977 | raw=83.91181519398195
- 6. [JP] Akatsuki Inc. | cross_pct=99.8989898989899 | raw=73.33081849714675
- 7. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.87752602571953 | raw=82.7137311437538
- 8. [JP] Mito Securities Co.,Ltd. | cross_pct=99.84848484848486 | raw=73.08270901063638
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.79797979797979 | raw=73.01278959211145
- 10. [US] TORM plc - Class A Common Stock | cross_pct=99.75505205143907 | raw=82.15038160254315
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 929
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは50.7点だが確認閾値未達
- 上位: スタンダード 50.7 / 金（ゴールド） 41.1 / ビットコイン 37.9
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
