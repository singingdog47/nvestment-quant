# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-25T12:50:52+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **RISK_ON**
- Score: 70.29
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.180000305175781
- Treasury realized-vol proxy (not ICE MOVE): 83.46 bps annualized; percentile=0.9246
- Flags: TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=44.4%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING|VOLUME_EXPANSION
- [US] Norwood Financial Corp. - Common Stock: SHORT_CROWDING|VOLUME_EXPANSION
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING|VOLUME_EXPANSION
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] SiriusPoint Ltd. Common Shares: SHORT_CROWDING|VOLUME_EXPANSION
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 1, 'WARNING': 1, 'CRITICAL': 0}
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] REGIME / Market regime changed

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=76.27662922327875 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=75.2532051721871 | cross_pct=99.94884910485933
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=75.21252652889879 | cross_pct=99.89769820971867
- 4. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=75.00063502248385 | cross_pct=99.846547314578
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.13103196911995 | cross_pct=99.64194373401534

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.45593495959231 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=82.92755967999022 | cross_pct=99.97085397843193
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.86768151000015 | cross_pct=99.9417079568639
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.11223041950973 | cross_pct=99.88341591372777
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=8.0 | raw=81.33541606379312 | cross_pct=99.79597784902361

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.45593495959231
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=76.27662922327875
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97085397843193 | raw=82.92755967999022
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94884910485933 | raw=75.2532051721871
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.9417079568639 | raw=82.86768151000015
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.89769820971867 | raw=75.21252652889879
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88341591372777 | raw=82.11223041950973
- 8. [JP] Akatsuki Inc. | cross_pct=99.846547314578 | raw=75.00063502248385
- 9. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.79597784902361 | raw=81.33541606379312
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.76683182745555 | raw=81.00427456034922
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 164
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

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が1.1点で優位性が弱い
- 上位: スタンダード 76.9 / ビットコイン 75.8 / テクノロジー 75.1
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
