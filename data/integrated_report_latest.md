# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-26T15:31:48+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 48.33
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 17.899999618530273
- Treasury realized-vol proxy (not ICE MOVE): 89.332 bps annualized; percentile=0.9325
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=69.2%, short-interest=25.0%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] FOOD & LIFE COMPANIES: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] IwaiCosmo Holdings,Inc.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Equity Bancshares, Inc. Class A Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 4, 'WARNING': 5, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / キヤノン、信越化学工業も…「下落が怖い」人向け"高配当"半導体・AI株7銘柄の実名 - 現代ビジネス
- [WARNING] COMPANY_EVENT / 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] LIQUIDITY / Market liquidity is weak
- [WARNING] LIQUIDITY / Thin liquidity flag active
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / ほくほくＦＧ、今期経常は10％増で2期連続最高益、40円増配へ - 株探
- [WATCH] COMPANY_EVENT / 500mlボトルが約50円。低価格でも“増収増益”の成長を続けるライフドリンク カンパニーが重要視する3つの戦略 - ネットショップ担当者フォーラム
- [WATCH] COMPANY_EVENT / 創業100周年の信越化学工業 上越市と新潟県に計1億円寄付 - 上越妙高タウン情報

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Marusan Securities Co.,Ltd. 8613.T | market_rank=1.0 | raw=81.82089165646359 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=80.14274102169676 | cross_pct=99.94837377387714
- 3. ELECOM CO.,LTD. 6750.T | market_rank=5.0 | raw=73.37224254904736 | cross_pct=99.79349509550852
- 4. Akatsuki Inc. 3932.T | market_rank=6.0 | raw=73.33319827364109 | cross_pct=99.74186886938566
- 5. KOEI TECMO HOLDINGS CO.,LTD. 3635.T | market_rank=8.0 | raw=71.91551274458453 | cross_pct=99.6386164171399

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.55578397058096 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.30766258814461 | cross_pct=99.96986136226641
- 3. Norwood Financial Corp. - Common Stock NWFL | market_rank=3.0 | raw=82.68308722611523 | cross_pct=99.93972272453286
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=5.0 | raw=82.37840583722836 | cross_pct=99.87944544906571
- 5. DHT Holdings, Inc. DHT | market_rank=6.0 | raw=82.28940061498778 | cross_pct=99.84930681133213

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.55578397058096
- 2. [JP] Marusan Securities Co.,Ltd. | cross_pct=100.0 | raw=81.82089165646359
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.96986136226641 | raw=83.30766258814461
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.94837377387714 | raw=80.14274102169676
- 5. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.93972272453286 | raw=82.68308722611523
- 6. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.87944544906571 | raw=82.37840583722836
- 7. [US] DHT Holdings, Inc. | cross_pct=99.84930681133213 | raw=82.28940061498778
- 8. [JP] ELECOM CO.,LTD. | cross_pct=99.79349509550852 | raw=73.37224254904736
- 9. [JP] Akatsuki Inc. | cross_pct=99.74186886938566 | raw=73.33319827364109
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.66847498493068 | raw=81.61030028935936
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 674
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは64.9点だが確認閾値未達
- 上位: スタンダード 64.9 / テクノロジー 61.9 / ビットコイン 46.4
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
