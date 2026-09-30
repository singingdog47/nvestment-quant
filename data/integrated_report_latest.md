# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-09-30T13:49:45+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 62.67
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.819999694824219
- Treasury realized-vol proxy (not ICE MOVE): 86.133 bps annualized; percentile=0.9365
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

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
- [US] Hercules Capital, Inc. Common Stock: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 11, 'WARNING': 9, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 訂正有価証券報告書－第161期(2025/04/01－2026/03/31)
- [WARNING] COMPANY_EVENT / 確認書
- [WARNING] COMPANY_EVENT / 訂正臨時報告書
- [WARNING] COMPANY_EVENT / 訂正有価証券届出書（参照方式）
- [WARNING] COMPANY_EVENT / 信越化学工業[4063]：取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ 2026年9月30日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / 信越化(4063) 取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ - みんかぶ
- [WARNING] LIQUIDITY / Thin liquidity flag active

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=74.76337759178585 | cross_pct=100.0
- 2. IwaiCosmo Holdings,Inc. 8707.T | market_rank=2.0 | raw=74.61026046660234 | cross_pct=99.94855967078189
- 3. OKASAN SECURITIES GROUP INC. 8609.T | market_rank=3.0 | raw=74.2507153193694 | cross_pct=99.8971193415638
- 4. Akatsuki Inc. 3932.T | market_rank=5.0 | raw=73.34392459091389 | cross_pct=99.79423868312757
- 5. ELECOM CO.,LTD. 6750.T | market_rank=8.0 | raw=72.08883101804898 | cross_pct=99.63991769547324

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.0057114371289 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.77669969947178 | cross_pct=99.97059688326962
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=83.17347958772051 | cross_pct=99.94119376653924
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=81.79694518083528 | cross_pct=99.88238753307851
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=6.0 | raw=81.62977097405346 | cross_pct=99.85298441634814

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.0057114371289
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=74.76337759178585
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97059688326962 | raw=83.77669969947178
- 4. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.94855967078189 | raw=74.61026046660234
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94119376653924 | raw=83.17347958772051
- 6. [JP] OKASAN SECURITIES GROUP INC. | cross_pct=99.8971193415638 | raw=74.2507153193694
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88238753307851 | raw=81.79694518083528
- 8. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.85298441634814 | raw=81.62977097405346
- 9. [JP] Akatsuki Inc. | cross_pct=99.79423868312757 | raw=73.34392459091389
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73537194942665 | raw=80.57964691858004
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 236
- Eligible for model-change review: True
- [INFO] regime / CONSTRUCTIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

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

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは79.3点だが確認閾値未達
- 上位: ビットコイン 79.3 / スタンダード 77.1 / テクノロジー 76.4
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
