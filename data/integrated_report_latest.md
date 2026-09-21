# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-21T15:54:32+00:00

## 1. 結論 / 今日の優先アクション
- **SELECTIVE REVIEW OF TOP CANDIDATES**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.8
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 14.779999732971191
- Treasury realized-vol proxy (not ICE MOVE): 74.744 bps annualized; percentile=0.7817
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=47.2%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] International Seaways, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [JP] KDDI: VOLUME_EXPANSION
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER
- [US] Norwood Financial Corp. - Common Stock: SHORT_INTEREST_RISING

## 4. 例外検知 / アラート
- Highest severity: **WATCH**
- Counts: {'INFO': 0, 'WATCH': 1, 'WARNING': 0, 'CRITICAL': 0}
- [WATCH] LIQUIDITY / Market liquidity is soft

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=76.31712249308279 | cross_pct=100.0
- 2. IwaiCosmo Holdings,Inc. 8707.T | market_rank=2.0 | raw=75.32052070536537 | cross_pct=99.94884910485933
- 3. Tokai Tokyo Financial Holdings,Inc. 8616.T | market_rank=3.0 | raw=75.0312079410746 | cross_pct=99.89769820971867
- 4. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=74.99470947362886 | cross_pct=99.846547314578
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.12291366010886 | cross_pct=99.64194373401534

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.97752287298992 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.16835463308888 | cross_pct=99.97078586035641
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.10634181850784 | cross_pct=99.94157172071283
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=4.0 | raw=82.57346986140112 | cross_pct=99.91235758106923
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=7.0 | raw=81.86720841149413 | cross_pct=99.82471516213847

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.97752287298992
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=76.31712249308279
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97078586035641 | raw=83.16835463308888
- 4. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.94884910485933 | raw=75.32052070536537
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94157172071283 | raw=83.10634181850784
- 6. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.91235758106923 | raw=82.57346986140112
- 7. [JP] Tokai Tokyo Financial Holdings,Inc. | cross_pct=99.89769820971867 | raw=75.0312079410746
- 8. [JP] Akatsuki Inc. | cross_pct=99.846547314578 | raw=74.99470947362886
- 9. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.82471516213847 | raw=81.86720841149413
- 10. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.76628688285129 | raw=81.386424141395
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 92
- Eligible for model-change review: True
- [INFO] action / REVIEW|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
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

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が0.8点で優位性が弱い
- 上位: スタンダード 78.7 / ビットコイン 77.9 / テクノロジー 76.8
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
