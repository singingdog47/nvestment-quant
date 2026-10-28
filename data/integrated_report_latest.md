# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-28T14:05:53+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 51.21
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 17.59000015258789
- Treasury realized-vol proxy (not ICE MOVE): 81.9 bps annualized; percentile=0.8214
- Flags: THIN_LIQUIDITY

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=69.2%, short-interest=26.9%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING
- [US] Innoviva, Inc. - Common Stock: SHORT_CROWDING
- [JP] コーエーテクモホールディングス: VOLUME_EXPANSION
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Tsakos Energy Navigation Ltd Common Shares: SHORT_INTEREST_RISING

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: RANGE_OR_UNDECIDED; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_UNDECIDED; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 19, 'WARNING': 13, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 臨時報告書
- [WARNING] COMPANY_EVENT / 発行登録書（株券､社債券等）

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Marusan Securities Co.,Ltd. 8613.T | market_rank=1.0 | raw=81.02063993331618 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=80.21821538842293 | cross_pct=99.94858611825192
- 3. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=73.30241651611102 | cross_pct=99.79434447300771
- 4. ELECOM CO.,LTD. 6750.T | market_rank=6.0 | raw=72.61031965106193 | cross_pct=99.74293059125964
- 5. KOEI TECMO HOLDINGS CO.,LTD. 3635.T | market_rank=9.0 | raw=71.06032324392784 | cross_pct=99.58868894601542

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.89877934990488 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.42703674969152 | cross_pct=99.9699157641396
- 3. Norwood Financial Corp. - Common Stock NWFL | market_rank=3.0 | raw=83.07034735427123 | cross_pct=99.93983152827917
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=82.22928521002727 | cross_pct=99.84957882069796
- 5. DHT Holdings, Inc. DHT | market_rank=7.0 | raw=82.20674784500733 | cross_pct=99.81949458483754

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.89877934990488
- 2. [JP] Marusan Securities Co.,Ltd. | cross_pct=100.0 | raw=81.02063993331618
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.9699157641396 | raw=83.42703674969152
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.94858611825192 | raw=80.21821538842293
- 5. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.93983152827917 | raw=83.07034735427123
- 6. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.84957882069796 | raw=82.22928521002727
- 7. [US] DHT Holdings, Inc. | cross_pct=99.81949458483754 | raw=82.20674784500733
- 8. [JP] Akatsuki Inc. | cross_pct=99.79434447300771 | raw=73.30241651611102
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.74293059125964 | raw=72.61031965106193
- 10. [US] TORM plc - Class A Common Stock | cross_pct=99.6690734055355 | raw=81.20980863234738
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 699
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

- 監視判定: **REVIEW_LEADER** — スタンダードが73.3点、2位との差11.6点。週次レビュー候補
- 上位: スタンダード 73.3 / テクノロジー 61.7 / ビットコイン 46.8
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
