# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-20T12:47:51+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 52.02
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 19.100000381469727
- Treasury realized-vol proxy (not ICE MOVE): 87.824 bps annualized; percentile=0.9127
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=69.8%, short-interest=26.4%, current/average volume=75.5%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [JP] IwaiCosmo Holdings,Inc.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Equity Bancshares, Inc. Class A Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING|VOLUME_EXPANSION
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Frontline Plc Ordinary Shares: HIGH_FLOAT_TURNOVER|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: TWO_WAY_WITH_RATES_VOLATILITY_RISK; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_RISK_REVIEW; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- [未校正予測] DHT 1w relative negative vs SPY; p=0.55 (研究上の事前確率)
- [未校正予測] 3635.T 1w relative positive vs 1306.T; p=0.55 (研究上の事前確率)
- 事後検証: n=0, Brier=None（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 18, 'WARNING': 4, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / NEC、システム開発の委託先にサイバー攻撃 顧客3社の情報漏洩 - 日本経済新聞
- [WARNING] COMPANY_EVENT / ふるさとチョイス、情報流出445万件 NECは委託先から漏洩 - 朝日新聞
- [WARNING] COMPANY_EVENT / ＮＥＣ委託先にサイバー攻撃、顧客企業３社の情報が漏えい…２社では個人情報漏えいを確認 - 読売新聞
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / ＡＮＹＣＯＬＯＲ(株)【5032】：決算説明会書き起こし - Yahoo!ファイナンス
- [WATCH] COMPANY_EVENT / にじさんじから「Y4T4 Half Anniversary」グッズを2026年10月21日(水)19時から販売開始！ - PR TIMES
- [WATCH] COMPANY_EVENT / NIJISANJI EN、「Anime Festival Asia Singapore 2026」に出展 サニー・ブリスコーら4人が11/28にステージ出演 - MEDIAMIXI
- [WATCH] COMPANY_EVENT / 都市部でKDDIローミング縮小、楽天モバイルに問われる通信品質と収益改善 - 日経クロステック

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Marusan Securities Co.,Ltd. 8613.T | market_rank=1.0 | raw=81.79417995277478 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=77.72635269833718 | cross_pct=99.94807892004154
- 3. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=75.09961503175845 | cross_pct=99.84423676012462
- 4. ELECOM CO.,LTD. 6750.T | market_rank=6.0 | raw=73.76552894166254 | cross_pct=99.74039460020768
- 5. KOEI TECMO HOLDINGS CO.,LTD. 3635.T | market_rank=7.0 | raw=73.10905279926214 | cross_pct=99.68847352024922

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.3421608074132 | cross_pct=100.0
- 2. Norwood Financial Corp. - Common Stock NWFL | market_rank=2.0 | raw=82.52234904067241 | cross_pct=99.96996094923401
- 3. First Busey Corporation - Common Stock BUSE | market_rank=4.0 | raw=81.34014482992788 | cross_pct=99.90988284770201
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=5.0 | raw=81.26807172469351 | cross_pct=99.87984379693602
- 5. DHT Holdings, Inc. DHT | market_rank=6.0 | raw=81.24562018224353 | cross_pct=99.84980474617002

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.3421608074132
- 2. [JP] Marusan Securities Co.,Ltd. | cross_pct=100.0 | raw=81.79417995277478
- 3. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.96996094923401 | raw=82.52234904067241
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94807892004154 | raw=77.72635269833718
- 5. [US] First Busey Corporation - Common Stock | cross_pct=99.90988284770201 | raw=81.34014482992788
- 6. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.87984379693602 | raw=81.26807172469351
- 7. [US] DHT Holdings, Inc. | cross_pct=99.84980474617002 | raw=81.24562018224353
- 8. [JP] Akatsuki Inc. | cross_pct=99.84423676012462 | raw=75.09961503175845
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.74039460020768 | raw=73.76552894166254
- 10. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.69960949234004 | raw=80.34155366917675
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 575
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.858
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.358
- Secondary fundamental coverage: 0.755
- Effective fundamental coverage: 0.849
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは59.2点だが確認閾値未達
- 上位: スタンダード 59.2 / ビットコイン 57.2 / テクノロジー 56.7
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
