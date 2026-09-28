# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-28T15:35:16+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 64.77
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.299999237060547
- Treasury realized-vol proxy (not ICE MOVE): 86.431 bps annualized; percentile=0.9405
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=41.7%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] Norwood Financial Corp. - Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 14, 'WARNING': 5, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 信越化、今期配当を20円増額修正 - 株探
- [WARNING] COMPANY_EVENT / 浜松ホトニクスは2026年9月29日に1株配当金0.1672USDを支払う予定 - Moomoo
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 発行登録書（株券､社債券等）
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / カカクコム、KDDIと資本提携解消（時事通信） - Yahoo!ニュース
- [WATCH] COMPANY_EVENT / 【アナリスト評価】ＫＤＤＩ、レーティング強気を継続、目標株価3,500円に引上げ（日系大手証券）(アイフィス株予報) - finance.yahoo.co.jp
- [WATCH] COMPANY_EVENT / 日本郵便とKDDI、ドローン社会基盤化へ基本合意書を締結し、郵便局をドローンポート拠点とする実証を開始 - newsroom.kddi.com

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. IwaiCosmo Holdings,Inc. 8707.T | market_rank=1.0 | raw=75.31101586297011 | cross_pct=100.0
- 2. OKASAN SECURITIES GROUP INC. 8609.T | market_rank=2.0 | raw=75.03358574331655 | cross_pct=99.94871794871794
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=74.9195792249367 | cross_pct=99.8974358974359
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=74.81515076865507 | cross_pct=99.7948717948718
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.31859504548693 | cross_pct=99.64102564102564

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.25625946558647 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.9468584510699 | cross_pct=99.97068308413955
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.33243052591867 | cross_pct=99.9413661682791
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.40209833355122 | cross_pct=99.88273233655819
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.98234075649786 | cross_pct=99.85341542069774

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.25625946558647
- 2. [JP] IwaiCosmo Holdings,Inc. | cross_pct=100.0 | raw=75.31101586297011
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97068308413955 | raw=83.9468584510699
- 4. [JP] OKASAN SECURITIES GROUP INC. | cross_pct=99.94871794871794 | raw=75.03358574331655
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9413661682791 | raw=83.33243052591867
- 6. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.8974358974359 | raw=74.9195792249367
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88273233655819 | raw=82.40209833355122
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85341542069774 | raw=81.98234075649786
- 9. [JP] Akatsuki Inc. | cross_pct=99.7948717948718 | raw=74.81515076865507
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73614775725594 | raw=81.19434736833152
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 187
- Eligible for model-change review: True
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.

## 7. データ品質 / 反証
- Quality score: 0.745
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.0
- Secondary fundamental coverage: 1.0
- Effective fundamental coverage: 0.65
- Fundamental evidence tier: secondary_only
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは75.9点だが確認閾値未達
- 上位: ビットコイン 75.9 / テクノロジー 71.9 / スタンダード 65.7
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
