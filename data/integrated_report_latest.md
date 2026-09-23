# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-23T12:49:28+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 66.2
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 14.300000190734863
- Treasury realized-vol proxy (not ICE MOVE): 76.104 bps annualized; percentile=0.8016
- Flags: none

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=97.2%, short-interest=47.2%, current/average volume=100.0%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] International Seaways, Inc. Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] Scorpio Tankers Inc. Common Shares: HIGH_FLOAT_TURNOVER|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Tsakos Energy Navigation Ltd Common Shares: SHORT_INTEREST_FALLING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] Millrose Properties, Inc. Class A Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING
- [US] Frontline Plc Ordinary Shares: VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION
- [US] TORM plc - Class A Common Stock: SHORT_INTEREST_RISING|VOLUME_EXPANSION|PRICE_DOWN_ON_VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 2, 'WARNING': 2, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：ストックオプション（新株予約権）の割当てに関するお知らせ 2026年9月15日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WATCH] COMPANY_EVENT / 通信事業者間での5Gミリ波の利用エリア拡大に向けた共同検討を開始 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=76.31712249308279 | cross_pct=100.0
- 2. IwaiCosmo Holdings,Inc. 8707.T | market_rank=2.0 | raw=75.32052070536537 | cross_pct=99.94884910485933
- 3. Tokai Tokyo Financial Holdings,Inc. 8616.T | market_rank=3.0 | raw=75.0312079410746 | cross_pct=99.89769820971867
- 4. Akatsuki Inc. 3932.T | market_rank=4.0 | raw=74.99470947362886 | cross_pct=99.846547314578
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=73.12291366010886 | cross_pct=99.64194373401534

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.33803783428812 | cross_pct=100.0
- 2. International Seaways, Inc. Common Stock  INSW | market_rank=2.0 | raw=82.66650814699295 | cross_pct=99.97095556200988
- 3. Scorpio Tankers Inc. Common Shares STNG | market_rank=3.0 | raw=82.50605391523797 | cross_pct=99.94191112401975
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=4.0 | raw=82.46133342641309 | cross_pct=99.91286668602962
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=8.0 | raw=81.36496567362 | cross_pct=99.79668893406912

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.33803783428812
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=76.31712249308279
- 3. [US] International Seaways, Inc. Common Stock  | cross_pct=99.97095556200988 | raw=82.66650814699295
- 4. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.94884910485933 | raw=75.32052070536537
- 5. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.94191112401975 | raw=82.50605391523797
- 6. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.91286668602962 | raw=82.46133342641309
- 7. [JP] Tokai Tokyo Financial Holdings,Inc. | cross_pct=99.89769820971867 | raw=75.0312079410746
- 8. [JP] Akatsuki Inc. | cross_pct=99.846547314578 | raw=74.99470947362886
- 9. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.79668893406912 | raw=81.36496567362
- 10. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.767644496079 | raw=80.7872152923969
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

- 監視判定: **WAIT_RESEARCH** — 首位と2位の差が2.0点で優位性が弱い
- 上位: スタンダード 78.6 / テクノロジー 76.6 / ビットコイン 75.7
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
