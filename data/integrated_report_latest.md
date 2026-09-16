# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-16T07:32:25+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **NEUTRAL**
- Score: 56.21
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 17.200000762939453
- Treasury realized-vol proxy (not ICE MOVE): 69.604 bps annualized; percentile=0.627
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=44.4%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] International Seaways, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING|VOLUME_EXPANSION
- [JP] Ichiyoshi Securities Co.,Ltd.: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Imperial Petroleum Inc. - Common Shares: SHORT_CROWDING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 11, 'WARNING': 5, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 信越化学工業、創立１００周年記念配当２０円を実施へ、年間配当予想１３６円に増額 - kabu-ir.com
- [WARNING] COMPANY_EVENT / 信越化学が堅調､第2四半期末に記念配当20円実施へ - shikiho.toyokeizai.net
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WATCH] COMPANY_EVENT / つくば市で自動運転バスの本格運行を10月2日から開始 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / KDDI株価が反発 事業説明会にアナリストから評価の声 - 日本経済新聞
- [WATCH] COMPANY_EVENT / KDDIスマートドローン／国内初、国土交通省航空局の「UTMサービスプロバイダID」を取得 - lnews.jp

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.0538565480208 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=76.02041094979744 | cross_pct=99.94874423372629
- 3. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=3.0 | raw=75.89760885367666 | cross_pct=99.89748846745259
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=75.66245691574116 | cross_pct=99.84623270117888
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.47314714234713 | cross_pct=99.64120963608406

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.4455268929331 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=84.04016038189992 | cross_pct=99.9706916764361
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=83.78615289495177 | cross_pct=99.94138335287221
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=4.0 | raw=82.94994341260137 | cross_pct=99.91207502930833
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=6.0 | raw=82.91674224412587 | cross_pct=99.85345838218053

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.4455268929331
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.0538565480208
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9706916764361 | raw=84.04016038189992
- 4. [JP] Akatsuki Inc. | cross_pct=99.94874423372629 | raw=76.02041094979744
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.94138335287221 | raw=83.78615289495177
- 6. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.91207502930833 | raw=82.94994341260137
- 7. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.89748846745259 | raw=75.89760885367666
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.85345838218053 | raw=82.91674224412587
- 9. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.84623270117888 | raw=75.66245691574116
- 10. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.82415005861665 | raw=82.525154930583
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 76
- Eligible for model-change review: True
- [INFO] regime / CONSTRUCTIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
- [INFO] rank_bucket / top10|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは57.3点だが確認閾値未達
- 上位: スタンダード 57.3 / ビットコイン 55.4 / テクノロジー 53.6
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
