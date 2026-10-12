# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-12T18:59:14+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 65.6
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.260000228881836
- Treasury realized-vol proxy (not ICE MOVE): 87.562 bps annualized; percentile=0.9246
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=28.8%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] Innoviva, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Imperial Petroleum Inc. - Common Shares: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 2, 'WARNING': 2, 'CRITICAL': 0}
- [WARNING] LIQUIDITY / Thin liquidity flag active
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / (株)三越伊勢丹ホールディングス【3099】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
- [WATCH] LIQUIDITY / Market liquidity is soft

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=75.55503873052794 | cross_pct=100.0
- 2. Akatsuki Inc. 3932.T | market_rank=2.0 | raw=75.41784043512763 | cross_pct=99.94824016563147
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=74.2002557581231 | cross_pct=99.89648033126294
- 4. Tokai Tokyo Financial Holdings,Inc. 8616.T | market_rank=4.0 | raw=74.1558453580007 | cross_pct=99.84472049689441
- 5. ELECOM CO.,LTD. 6750.T | market_rank=7.0 | raw=72.93745210275051 | cross_pct=99.68944099378882

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=85.12062181134284 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.33473955026568 | cross_pct=99.97041420118343
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.91139851631753 | cross_pct=99.94082840236686
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.35697124418533 | cross_pct=99.88165680473374
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.84265813159391 | cross_pct=99.85207100591717

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=85.12062181134284
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=75.55503873052794
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97041420118343 | raw=83.33473955026568
- 4. [JP] Akatsuki Inc. | cross_pct=99.94824016563147 | raw=75.41784043512763
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94082840236686 | raw=82.91139851631753
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89648033126294 | raw=74.2002557581231
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88165680473374 | raw=82.35697124418533
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85207100591717 | raw=81.84265813159391
- 9. [JP] Tokai Tokyo Financial Holdings,Inc. | cross_pct=99.84472049689441 | raw=74.1558453580007
- 10. [US] TORM plc - Class A Common Stock | cross_pct=99.70414201183432 | raw=80.55980149052539
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 487
- Eligible for model-change review: True
- [WATCH] regime / CONSTRUCTIVE|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top3|1m: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が1.6点で優位性が弱い
- 上位: スタンダード 79.2 / テクノロジー 77.5 / ビットコイン 66.1
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
