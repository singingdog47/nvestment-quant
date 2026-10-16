# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-16T12:30:23+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.68
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.030000686645508
- Treasury realized-vol proxy (not ICE MOVE): 93.704 bps annualized; percentile=0.9762
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=26.9%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] DHT Holdings, Inc.: HIGH_FLOAT_TURNOVER|SHORT_CROWDING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Frontline Plc Ordinary Shares: HIGH_FLOAT_TURNOVER|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING|VOLUME_EXPANSION
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] NEC: VOLUME_EXPANSION|PRICE_UP_ON_VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 21, 'WARNING': 7, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 三越伊勢丹ホールディングス[3099]：自己株式の取得状況（途中経過）に関するお知らせ 2026年10月1日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 東京海上ホールディングス[8766]：自己株式の取得状況に関するお知らせ 2026年10月7日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 6-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / ＡＮＹＣＯＬＯＲ(株)【5032】：決算説明会書き起こし - Yahoo!ファイナンス

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. KYOKUTO SECURITIES CO.,LTD. 8706.T | market_rank=1.0 | raw=76.14652155216699 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=75.63533206984974 | cross_pct=99.94861253854059
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=75.19113981965789 | cross_pct=99.8972250770812
- 4. ELECOM CO.,LTD. 6750.T | market_rank=4.0 | raw=73.37324638904626 | cross_pct=99.84583761562179
- 5. IwaiCosmo Holdings,Inc. 8707.T | market_rank=8.0 | raw=71.5914416099828 | cross_pct=99.64028776978418

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.77389009559437 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=83.1821817934462 | cross_pct=99.97014925373135
- 3. DHT Holdings, Inc. DHT | market_rank=3.0 | raw=82.42240932717269 | cross_pct=99.94029850746269
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.29584089807152 | cross_pct=99.88059701492537
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.78199589161828 | cross_pct=99.85074626865672

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.77389009559437
- 2. [JP] KYOKUTO SECURITIES CO.,LTD. | cross_pct=100.0 | raw=76.14652155216699
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.97014925373135 | raw=83.1821817934462
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.94861253854059 | raw=75.63533206984974
- 5. [US] DHT Holdings, Inc. | cross_pct=99.94029850746269 | raw=82.42240932717269
- 6. [JP] Akatsuki Inc. | cross_pct=99.8972250770812 | raw=75.19113981965789
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88059701492537 | raw=82.29584089807152
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85074626865672 | raw=81.78199589161828
- 9. [JP] ELECOM CO.,LTD. | cross_pct=99.84583761562179 | raw=73.37324638904626
- 10. [US] TORM plc - Class A Common Stock | cross_pct=99.82089552238807 | raw=81.73999123621057
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 520
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

- 監視判定: **REVIEW_LEADER** — スタンダードが79.0点、2位との差9.6点。週次レビュー候補
- 上位: スタンダード 79.0 / テクノロジー 69.4 / ビットコイン 67.0
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
