# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-14T12:56:58+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 68.01
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.770000457763672
- Treasury realized-vol proxy (not ICE MOVE): 88.52 bps annualized; percentile=0.9325
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=71.2%, short-interest=28.8%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Imperial Petroleum Inc. - Common Shares: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Tsakos Energy Navigation Ltd Common Shares: SHORT_INTEREST_RISING|VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 13, 'WARNING': 6, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WARNING] COMPANY_EVENT / 半期報告書－第28期(2026/03/01－2027/02/28)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / 『労働新聞』最新号（3563号）を労働新聞電子版に掲載しました。｜お知らせ - 労働新聞社
- [WATCH] COMPANY_EVENT / KDDIが韓国LG CNSと基本合意書、AI・スマートシティなどAPACの4分野で協業を検討へ - ビジネス+IT

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=75.7624147615239 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=75.45004276804677 | cross_pct=99.94845360824742
- 3. ELECOM CO.,LTD. 6750.T | market_rank=3.0 | raw=73.9670519286138 | cross_pct=99.89690721649484
- 4. OKASAN SECURITIES GROUP INC. 8609.T | market_rank=4.0 | raw=73.28073826302914 | cross_pct=99.84536082474227
- 5. IwaiCosmo Holdings,Inc. 8707.T | market_rank=5.0 | raw=73.15179211601726 | cross_pct=99.79381443298969

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.09760259751701 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.54548086751316 | cross_pct=99.9702823179792
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.01312609410535 | cross_pct=99.9405646359584
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.31808194383906 | cross_pct=99.88112927191679
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.7923301586522 | cross_pct=99.85141158989599

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.09760259751701
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=75.7624147615239
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.9702823179792 | raw=83.54548086751316
- 4. [JP] Akatsuki Inc. | cross_pct=99.94845360824742 | raw=75.45004276804677
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9405646359584 | raw=83.01312609410535
- 6. [JP] ELECOM CO.,LTD. | cross_pct=99.89690721649484 | raw=73.9670519286138
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88112927191679 | raw=82.31808194383906
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85141158989599 | raw=81.7923301586522
- 9. [JP] OKASAN SECURITIES GROUP INC. | cross_pct=99.84536082474227 | raw=73.28073826302914
- 10. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.79381443298969 | raw=73.15179211601726
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 512
- Eligible for model-change review: True
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top10|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
- [WATCH] rank_bucket / top3|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.873
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.385
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.885
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が1.7点で優位性が弱い
- 上位: スタンダード 79.4 / テクノロジー 77.7 / ビットコイン 67.9
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
