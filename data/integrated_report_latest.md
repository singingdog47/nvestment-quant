# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-19T14:45:26+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 52.11
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 17.68000030517578
- Treasury realized-vol proxy (not ICE MOVE): 90.011 bps annualized; percentile=0.9444
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.7%, short-interest=26.4%, current/average volume=75.5%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Equity Bancshares, Inc. Class A Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Tsakos Energy Navigation Ltd Common Shares: SHORT_INTEREST_RISING

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 25, 'WARNING': 10, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：業績予想の修正に関するお知らせ 2026年10月19日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Marusan Securities Co.,Ltd. 8613.T | market_rank=1.0 | raw=81.8655829027422 | cross_pct=100.0
- 2. KYOKUTO SECURITIES CO.,LTD. 8706.T | market_rank=2.0 | raw=76.00098141590935 | cross_pct=99.9484004127967
- 3. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=75.12075512633331 | cross_pct=99.84520123839009
- 4. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=73.73520117418616 | cross_pct=99.79360165118679
- 5. KOEI TECMO HOLDINGS CO.,LTD. 3635.T | market_rank=9.0 | raw=71.38207054582386 | cross_pct=99.58720330237358

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.639423738651 | cross_pct=100.0
- 2. Norwood Financial Corp. - Common Stock NWFL | market_rank=2.0 | raw=82.47897783029211 | cross_pct=99.96990671080349
- 3. DHT Holdings, Inc. DHT | market_rank=4.0 | raw=81.68619907099148 | cross_pct=99.90972013241047
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=5.0 | raw=81.50538408805832 | cross_pct=99.87962684321397
- 5. First Busey Corporation - Common Stock BUSE | market_rank=7.0 | raw=81.33848537400674 | cross_pct=99.81944026482094

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.639423738651
- 2. [JP] Marusan Securities Co.,Ltd. | cross_pct=100.0 | raw=81.8655829027422
- 3. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.96990671080349 | raw=82.47897783029211
- 4. [JP] KYOKUTO SECURITIES CO.,LTD. | cross_pct=99.9484004127967 | raw=76.00098141590935
- 5. [US] DHT Holdings, Inc. | cross_pct=99.90972013241047 | raw=81.68619907099148
- 6. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.87962684321397 | raw=81.50538408805832
- 7. [JP] Akatsuki Inc. | cross_pct=99.84520123839009 | raw=75.12075512633331
- 8. [US] First Busey Corporation - Common Stock | cross_pct=99.81944026482094 | raw=81.33848537400674
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.79360165118679 | raw=73.73520117418616
- 10. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.72916039723142 | raw=80.54562926290906
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 550
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.867
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.377
- Secondary fundamental coverage: 0.755
- Effective fundamental coverage: 0.868
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは59.1点だが確認閾値未達
- 上位: スタンダード 59.1 / ビットコイン 59.0 / テクノロジー 56.4
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
