# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-11-04T15:32:28+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 48.8
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.979999542236328
- Treasury realized-vol proxy (not ICE MOVE): 81.856 bps annualized; percentile=0.8056
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=23.1%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [JP] 信越化学工業: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Financial Institutions, Inc. - Common Stock: SHORT_CROWDING
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [JP] Akatsuki Inc.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] コーエーテクモホールディングス: TIGHT_FLOAT
- [JP] ほくほくフィナンシャルグループ: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 3a. 短中長期の需給仮説（研究用）
- short / 1-2 weeks: RANGE_OR_UNDECIDED; 仮説=Volume-supported directional continuation is plausible for individually flagged watchlist names; cross-market risk can override.; 反証=A contrary relative return at the predetermined endpoint or worsening rates/credit stress.; 方針=Existing orders unchanged. New purchase only after liquidity, risk and human review.
- medium / 1-3 months: CONDITIONAL_UNDECIDED; 仮説=Sector and positioning rotation may outlast an index bounce; corporate earnings and revised guidance must corroborate.; 反証=Rotation reverses for several weeks or earnings/credit assumptions change materially.; 方針=Review 1-in-1-out replacements, position concentration, and portfolio correlations; no model-driven orders.
- long / 1-3 years: FUNDAMENTALS_NOT_ESTABLISHED; 仮説=Long-run outcomes depend on earnings power, capital allocation, valuation and structural demand, not weekly order flow.; 反証=Thesis deterioration, adverse cash-flow revisions, or lasting competitive disadvantage.; 方針=Core accumulation and strategic holdings require separate cash-flow and thesis checks; no long-term directional forecast without evidence.
- 検証可能な新規需給シグナルなし。欠損を方向予測に変換しません。
- 事後検証: n=1, Brier=0.20249999999999996（未校正）

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 21, 'WARNING': 6, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 東京海上、今期配当を実質増額修正 - 株探
- [WARNING] COMPANY_EVENT / 水戸証券(8622)、4期連続となる「増配」を発表し、配当利回り5.9％に！ 年間配当は4年で3.0倍に増加、2026年3月期は前期比13円増の｢1株あたり43円｣に！ - ダイヤモンド・オンライン
- [WARNING] COMPANY_EVENT / コーエーテクモホールディングス[3635]：令和９年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月26日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WARNING] COMPANY_EVENT / 信越化学工業(4063) 電子材料部門の想定以上の好調を受け、業績予想を上方修正 - QUICK Money World
- [WARNING] COMPANY_EVENT / KDDI、顧客情報2万人分漏洩か ライフネット生命への不正アクセスで - 日本経済新聞
- [WATCH] COMPANY_EVENT / ANYCOLORデザイン部 初期メンバー座談会 「ライバーのため」を突き詰めたデザインが、業界の文化になるまで - ANYCOLOR MAGAZINE
- [WATCH] COMPANY_EVENT / ANYCOLOR、にじさんじ所属「叢雲カゲツ」への権利侵害で示談成立―匿名掲示板の投稿者を特定し100万円の損害賠償 - インサイド

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Strike Group Co.,Ltd. 6196.T | market_rank=1.0 | raw=74.69807732244485 | cross_pct=100.0
- 2. Toranvia Co.,Ltd. 545A.T | market_rank=2.0 | raw=74.30595330113545 | cross_pct=99.94934143870314
- 3. ELECOM CO.,LTD. 6750.T | market_rank=3.0 | raw=73.2982928920055 | cross_pct=99.89868287740629
- 4. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=72.9074511259042 | cross_pct=99.84802431610942
- 5. Mito Securities Co.,Ltd. 8622.T | market_rank=5.0 | raw=72.90391064578496 | cross_pct=99.79736575481256

### 米国株（市場内順位）
- 1. Financial Institutions, Inc. - Common Stock FISI | market_rank=1.0 | raw=84.1160081973627 | cross_pct=100.0
- 2. Carter Bankshares, Inc. - Common Stock CARE | market_rank=2.0 | raw=83.2951841383638 | cross_pct=99.96959562176954
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=4.0 | raw=82.77381308931324 | cross_pct=99.90878686530861
- 4. DHT Holdings, Inc. DHT | market_rank=10.0 | raw=81.17625938382385 | cross_pct=99.72636059592581
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=12.0 | raw=80.73023858250389 | cross_pct=99.66555183946488

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Financial Institutions, Inc. - Common Stock | cross_pct=100.0 | raw=84.1160081973627
- 2. [JP] Strike Group Co.,Ltd. | cross_pct=100.0 | raw=74.69807732244485
- 3. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=99.96959562176954 | raw=83.2951841383638
- 4. [JP] Toranvia Co.,Ltd. | cross_pct=99.94934143870314 | raw=74.30595330113545
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.90878686530861 | raw=82.77381308931324
- 6. [JP] ELECOM CO.,LTD. | cross_pct=99.89868287740629 | raw=73.2982928920055
- 7. [JP] Akatsuki Inc. | cross_pct=99.84802431610942 | raw=72.9074511259042
- 8. [JP] Mito Securities Co.,Ltd. | cross_pct=99.79736575481256 | raw=72.90391064578496
- 9. [JP] KOEI TECMO HOLDINGS CO.,LTD. | cross_pct=99.7467071935157 | raw=71.99577852932696
- 10. [US] DHT Holdings, Inc. | cross_pct=99.72636059592581 | raw=81.17625938382385
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 879
- Eligible for model-change review: True
- [WATCH] action / REVIEW|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] action / REVIEW|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.847
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.327
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.827
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは59.6点だが確認閾値未達
- 上位: スタンダード 59.6 / テクノロジー 52.9 / ビットコイン 52.8
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
