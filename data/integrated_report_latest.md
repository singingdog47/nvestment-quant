# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-14T07:33:33+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 58.46
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 17.5
- Treasury realized-vol proxy (not ICE MOVE): 70.94 bps annualized; percentile=0.6746
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=47.2%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Imperial Petroleum Inc. - Common Shares: SHORT_CROWDING|VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION|POTENTIAL_SHORT_SQUEEZE_CONTEXT
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] International Seaways, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING|VOLUME_EXPANSION
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Tsakos Energy Navigation Ltd Common Shares: SHORT_INTEREST_FALLING|VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 10, 'WARNING': 6, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WATCH] COMPANY_EVENT / 日産自動車、Moplus、KDDI、自動運転車両10台による通信技術実証を実施 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / 攻撃者より先に動くサイバーセキュリティへ - kddi-research.jp

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=76.98877548250931 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=76.58286118549049 | cross_pct=99.94887525562373
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=75.78535962683704 | cross_pct=99.89775051124744
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=75.51765325588468 | cross_pct=99.84662576687117
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=72.92518355771705 | cross_pct=99.64212678936605

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.45668161973387 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=84.51353012734442 | cross_pct=99.9706916764361
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=84.12331162912602 | cross_pct=99.94138335287221
- 4. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=82.97644117327948 | cross_pct=99.85345838218053
- 5. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=7.0 | raw=82.66781958746738 | cross_pct=99.82415005861665

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.45668161973387
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=76.98877548250931
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9706916764361 | raw=84.51353012734442
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94887525562373 | raw=76.58286118549049
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.94138335287221 | raw=84.12331162912602
- 6. [JP] Akatsuki Inc. | cross_pct=99.89775051124744 | raw=75.78535962683704
- 7. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85345838218053 | raw=82.97644117327948
- 8. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.84662576687117 | raw=75.51765325588468
- 9. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.82415005861665 | raw=82.66781958746738
- 10. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.79484173505276 | raw=82.04062565840852
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 66
- Eligible for model-change review: True
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

- 監視判定: **WAIT_RESEARCH** — 首位スタンダードは65.6点だが確認閾値未達
- 上位: スタンダード 65.6 / テクノロジー 62.8 / ビットコイン 58.9
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
