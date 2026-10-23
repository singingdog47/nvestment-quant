# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-23T12:41:24+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 53.43
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 19.700000762939453
- Treasury realized-vol proxy (not ICE MOVE): 90.419 bps annualized; percentile=0.9524
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.2%, short-interest=23.1%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] ほくほくフィナンシャルグループ: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] IwaiCosmo Holdings,Inc.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Equity Bancshares, Inc. Class A Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Norwood Financial Corp. - Common Stock: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- [未校正予測] NWFL 1w relative positive vs SPY; p=0.55 (研究上の事前確率)
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 24, 'WARNING': 6, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞
- [WARNING] COMPANY_EVENT / 東京海上ホールディングス[8766]：自己株式の取得状況に関するお知らせ 2026年10月7日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / 剣持刀也【虚空狂宴】ライブレポート 音楽フェスと虚空教が交差！ 星街すいせい、葛葉、ピーナッツくんが駆けつける - ANYCOLOR MAGAZINE
- [WATCH] COMPANY_EVENT / 葛葉“Bloody Alexandrite”レポート その歩みこそ王道、現実と魔界の二面性で魅せたアーティストとしての真骨頂 - ANYCOLOR MAGAZINE

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Marusan Securities Co.,Ltd. 8613.T | market_rank=1.0 | raw=82.27647442012973 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=80.85876765440281 | cross_pct=99.9482669425763
- 3. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=74.59751147108904 | cross_pct=99.79306777030523
- 4. ELECOM CO.,LTD. 6750.T | market_rank=6.0 | raw=73.6657769262101 | cross_pct=99.74133471288154
- 5. KOEI TECMO HOLDINGS CO.,LTD. 3635.T | market_rank=8.0 | raw=71.50795480685609 | cross_pct=99.63786859803415

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.31238021910197 | cross_pct=100.0
- 2. Norwood Financial Corp. - Common Stock NWFL | market_rank=2.0 | raw=82.55613811885985 | cross_pct=99.96998799519808
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=82.50504255331944 | cross_pct=99.93997599039616
- 4. DHT Holdings, Inc. DHT | market_rank=4.0 | raw=82.23821394600498 | cross_pct=99.90996398559425
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=8.0 | raw=81.79583112176068 | cross_pct=99.78991596638656

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.31238021910197
- 2. [JP] Marusan Securities Co.,Ltd. | cross_pct=100.0 | raw=82.27647442012973
- 3. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.96998799519808 | raw=82.55613811885985
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.9482669425763 | raw=80.85876765440281
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.93997599039616 | raw=82.50504255331944
- 6. [US] DHT Holdings, Inc. | cross_pct=99.90996398559425 | raw=82.23821394600498
- 7. [JP] Akatsuki Inc. | cross_pct=99.79306777030523 | raw=74.59751147108904
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.78991596638656 | raw=81.79583112176068
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.74133471288154 | raw=73.6657769262101
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.72989195678271 | raw=81.70574011927975
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 634
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは60.8点だが確認閾値未達
- 上位: スタンダード 60.8 / テクノロジー 58.0 / ビットコイン 48.2
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
