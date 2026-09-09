# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-09T07:32:42+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 60.99
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.65999984741211
- Treasury realized-vol proxy (not ICE MOVE): 62.979 bps annualized; percentile=0.4048
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=47.2%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] International Seaways, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Frontline Plc Ordinary Shares: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] TORM plc - Class A Common Stock: SHORT_INTEREST_RISING|VOLUME_EXPANSION
- [JP] Helios Techno Holding Co.,Ltd.: VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 11, 'WARNING': 9, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / ＫＤＤＩ[9433]：自己株式の取得状況に関するお知らせ 2026年9月9日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.13382937087879 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=76.8562806866957 | cross_pct=99.94887525562373
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=75.77354588344772 | cross_pct=99.89775051124744
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=75.03972680054474 | cross_pct=99.79550102249489
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=72.31814909767523 | cross_pct=99.59100204498978

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.43214063829907 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.56066671474454 | cross_pct=99.97085397843193
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.5205408757257 | cross_pct=99.9417079568639
- 4. Scorpio Tankers Inc. Common Shares STNG | market_rank=4.0 | raw=82.79618115668501 | cross_pct=99.91256193529583
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=8.0 | raw=81.74675524356293 | cross_pct=99.79597784902361

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.43214063829907
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.13382937087879
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97085397843193 | raw=83.56066671474454
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94887525562373 | raw=76.8562806866957
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9417079568639 | raw=83.5205408757257
- 6. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.91256193529583 | raw=82.79618115668501
- 7. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89775051124744 | raw=75.77354588344772
- 8. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.79597784902361 | raw=81.74675524356293
- 9. [JP] Akatsuki Inc. | cross_pct=99.79550102249489 | raw=75.03972680054474
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.67939376275139 | raw=81.03867278172973
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 46
- Eligible for model-change review: False
- [INFO] regime / CONSTRUCTIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が2.8点で優位性が弱い
- 上位: テクノロジー 73.0 / ビットコイン 70.2 / スタンダード 67.5
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
