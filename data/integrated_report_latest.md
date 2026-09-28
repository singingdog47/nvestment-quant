# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-28T17:39:21+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 66.88
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.9399995803833
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
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 10, 'WARNING': 1, 'CRITICAL': 0}
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / カカクコム、KDDIと資本提携解消（時事通信） - news.yahoo.co.jp
- [WATCH] COMPANY_EVENT / 【アナリスト評価】ＫＤＤＩ、レーティング強気を継続、目標株価3,500円に引上げ（日系大手証券）(アイフィス株予報) - finance.yahoo.co.jp
- [WATCH] COMPANY_EVENT / NECグループの英国現代奴隷法への対応 : 企業情報 - NEC
- [WATCH] COMPANY_EVENT / サイバー攻撃のリスクから事業継続を考える - NEC
- [WATCH] COMPANY_EVENT / 光通信衛星を数百基整備 NEC計画 - news.yahoo.co.jp
- [WATCH] COMPANY_EVENT / 信越化学工業(株)【4063】：板気配 - finance.yahoo.co.jp
- [WATCH] COMPANY_EVENT / 浜松ホトニクス(株)【6965】：決算情報 - finance.yahoo.co.jp

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. IwaiCosmo Holdings,Inc. 8707.T | market_rank=1.0 | raw=75.31101586297011 | cross_pct=100.0
- 2. OKASAN SECURITIES GROUP INC. 8609.T | market_rank=2.0 | raw=75.03358574331655 | cross_pct=99.94871794871794
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=74.9195792249367 | cross_pct=99.8974358974359
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=74.81515076865507 | cross_pct=99.7948717948718
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.31859504548693 | cross_pct=99.64102564102564

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.2815288348109 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.80115187221789 | cross_pct=99.97068308413955
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.3429265746105 | cross_pct=99.9413661682791
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.30223680079172 | cross_pct=99.88273233655819
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.84265150414032 | cross_pct=99.85341542069774

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.2815288348109
- 2. [JP] IwaiCosmo Holdings,Inc. | cross_pct=100.0 | raw=75.31101586297011
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97068308413955 | raw=83.80115187221789
- 4. [JP] OKASAN SECURITIES GROUP INC. | cross_pct=99.94871794871794 | raw=75.03358574331655
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9413661682791 | raw=83.3429265746105
- 6. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.8974358974359 | raw=74.9195792249367
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88273233655819 | raw=82.30223680079172
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85341542069774 | raw=81.84265150414032
- 9. [JP] Akatsuki Inc. | cross_pct=99.7948717948718 | raw=74.81515076865507
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73614775725594 | raw=81.22038956228035
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

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは76.9点だが確認閾値未達
- 上位: ビットコイン 76.9 / スタンダード 72.8 / テクノロジー 72.3
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
