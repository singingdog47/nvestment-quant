# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-03T15:15:16+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 46.64
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 20.829999923706055
- Treasury realized-vol proxy (not ICE MOVE): 80.713 bps annualized; percentile=0.7937
- Flags: THIN_LIQUIDITY

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=23.1%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Financial Institutions, Inc. - Common Stock: SHORT_CROWDING
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] コーエーテクモホールディングス: TIGHT_FLOAT
- [JP] Strike Group Co.,Ltd.: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [JP] Akatsuki Inc.: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: RANGE_OR_UNDECIDED; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_UNDECIDED; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=1, Brier=0.20249999999999996（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 14, 'WARNING': 5, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / ◎〔決算〕ほくほくＦＧ、連結純利益４２０億円に上方修正 - 時事通信ニュース
- [WARNING] COMPANY_EVENT / ほくほくフィナンシャルグループ[8377]：業績予想および配当予想の修正に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / KDDI、2万2541件の顧客情報漏えいか ライフネット生命への不正アクセスで（アスキー） - Yahoo!ニュース
- [WARNING] LIQUIDITY / Thin liquidity flag active
- [WATCH] COMPANY_EVENT / ＡＮＹＣＯＬＯＲ、「にじさんじ」が韓国の大型イベントに出展 - https://kabu-ir.com/
- [WATCH] COMPANY_EVENT / お仕事手帖 翻訳業務編 多彩な表現で“生きたニュアンス”を世界へ届ける - ANYCOLOR MAGAZINE
- [WATCH] COMPANY_EVENT / 国内初、850MHz帯Wi-Fi HaLowを活用したロボットトラクターの無線遠隔監視・制御の実証に成功 ～自動運転の運用範囲拡大による農作業の自動化・省力化を推進 - NECネッツエスアイ

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Strike Group Co.,Ltd. 6196.T | market_rank=1.0 | raw=74.97650749000053 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=74.22550621714534 | cross_pct=99.9490575649516
- 3. Toranvia Co.,Ltd. 545A.T | market_rank=3.0 | raw=73.90367306956388 | cross_pct=99.8981151299032
- 4. ELECOM CO.,LTD. 6750.T | market_rank=4.0 | raw=73.304371833606 | cross_pct=99.84717269485482
- 5. Mito Securities Co.,Ltd. 8622.T | market_rank=5.0 | raw=72.15144650467884 | cross_pct=99.79623025980642

### 米国株（市場内順位）
- 1. Financial Institutions, Inc. - Common Stock FISI | market_rank=1.0 | raw=84.20573396109813 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.28349342098119 | cross_pct=99.96949359365466
- 3. Carter Bankshares, Inc. - Common Stock CARE | market_rank=3.0 | raw=83.23779775257876 | cross_pct=99.93898718730934
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=10.0 | raw=81.71512196684077 | cross_pct=99.72544234289201
- 5. DHT Holdings, Inc. DHT | market_rank=11.0 | raw=81.69608740877507 | cross_pct=99.69493593654668

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Financial Institutions, Inc. - Common Stock | cross_pct=100.0 | raw=84.20573396109813
- 2. [JP] Strike Group Co.,Ltd. | cross_pct=100.0 | raw=74.97650749000053
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.96949359365466 | raw=83.28349342098119
- 4. [JP] Akatsuki Inc. | cross_pct=99.9490575649516 | raw=74.22550621714534
- 5. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=99.93898718730934 | raw=83.23779775257876
- 6. [JP] Toranvia Co.,Ltd. | cross_pct=99.8981151299032 | raw=73.90367306956388
- 7. [JP] ELECOM CO.,LTD. | cross_pct=99.84717269485482 | raw=73.304371833606
- 8. [JP] Mito Securities Co.,Ltd. | cross_pct=99.79623025980642 | raw=72.15144650467884
- 9. [JP] KOEI TECMO HOLDINGS CO.,LTD. | cross_pct=99.74528782475802 | raw=71.80923670127234
- 10. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.72544234289201 | raw=81.71512196684077
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 869
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] action / REVIEW|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは55.3点だが確認閾値未達
- 上位: スタンダード 55.3 / テクノロジー 49.0 / ビットコイン 40.7
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
