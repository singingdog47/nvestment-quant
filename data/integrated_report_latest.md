# Investment Quant Daily Integrated Report v2.13

Generated (UTC): 2026-10-05T16:07:10+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 63.17
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.59000015258789
- Treasury realized-vol proxy (not ICE MOVE): 90.387 bps annualized; percentile=0.9643
- Flags: THIN_LIQUIDITY, TREASURY_VOLATILITY_SHOCK

## 3. 個別銘柄の需給コンテキスト
- Data status: partial
- Scope: public watchlist plus screening leaders; private portfolio excluded
- Coverage: free-float=73.1%, short-interest=28.8%, current/average volume=76.9%
- 用途は監視・執行注意・退出流動性の確認に限定し、銘柄順位・ファンダメンタルズ評価・投資仮説は変更しません。
- [US] Carter Bankshares, Inc. - Common Stock: SHORT_CROWDING
- [US] Norwood Financial Corp. - Common Stock: SHORT_CROWDING
- [US] First Busey Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [US] WesBanco, Inc. - Common Stock: SHORT_CROWDING
- [US] LTC Properties, Inc. Common Stock: SHORT_CROWDING
- [US] ACNB Corporation - Common Stock: SHORT_CROWDING|SHORT_INTEREST_RISING
- [JP] ANYCOLOR: HIGH_FLOAT_TURNOVER
- [JP] ほくほくフィナンシャルグループ: VOLUME_EXPANSION

## 4. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 28, 'WARNING': 5, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / ほくほくフィナンシャルグループ[8377]：2027年3月期 第1四半期決算短信〔日本基準〕（連結） 2026年7月29日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] LIQUIDITY / Thin liquidity flag active
- [WARNING] VOLATILITY / Treasury yield volatility is unusually high
- [WATCH] COMPANY_EVENT / ＡＮＹＣＯＬＯＲ(株)【5032】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
- [WATCH] COMPANY_EVENT / 【にじさんじ】「Kuzuha One-Man Live "Bloody Alexandrite"」開催記念！葛葉の複製直筆メッセージ入り駅広告が全国４７都道府県に登場！ - ANYCOLOR株式会社
- [WATCH] COMPANY_EVENT / ANYCOLOR(5032)株価下落の理由｜1Q決算と今後の見通し - 日本投資機構株式会社

## 5. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Akatsuki Inc. 3932.T | market_rank=1.0 | raw=75.09342685576989 | cross_pct=100.0
- 2. Mito Securities Co.,Ltd. 8622.T | market_rank=2.0 | raw=74.7511302119329 | cross_pct=99.94805194805195
- 3. IwaiCosmo Holdings,Inc. 8707.T | market_rank=3.0 | raw=74.39831898259196 | cross_pct=99.8961038961039
- 4. Tokai Tokyo Financial Holdings,Inc. 8616.T | market_rank=4.0 | raw=74.12732642601766 | cross_pct=99.84415584415585
- 5. ELECOM CO.,LTD. 6750.T | market_rank=7.0 | raw=72.2050044831736 | cross_pct=99.6883116883117

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.6831177654017 | cross_pct=100.0
- 2. Scorpio Tankers Inc. Common Shares STNG | market_rank=2.0 | raw=83.79182008446546 | cross_pct=99.97055359246173
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.93498773622414 | cross_pct=99.94110718492344
- 4. Norwood Financial Corp. - Common Stock NWFL | market_rank=5.0 | raw=82.17904216161385 | cross_pct=99.88221436984688
- 5. Tsakos Energy Navigation Ltd Common Shares TEN | market_rank=7.0 | raw=81.46554148915395 | cross_pct=99.82332155477032

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.6831177654017
- 2. [JP] Akatsuki Inc. | cross_pct=100.0 | raw=75.09342685576989
- 3. [US] Scorpio Tankers Inc. Common Shares | cross_pct=99.97055359246173 | raw=83.79182008446546
- 4. [JP] Mito Securities Co.,Ltd. | cross_pct=99.94805194805195 | raw=74.7511302119329
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94110718492344 | raw=82.93498773622414
- 6. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.8961038961039 | raw=74.39831898259196
- 7. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.88221436984688 | raw=82.17904216161385
- 8. [JP] Tokai Tokyo Financial Holdings,Inc. | cross_pct=99.84415584415585 | raw=74.12732642601766
- 9. [US] Tsakos Energy Navigation Ltd Common Shares | cross_pct=99.82332155477032 | raw=81.46554148915395
- 10. [US] First Busey Corporation - Common Stock | cross_pct=99.73498233215548 | raw=80.69584984855514
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 6. 過去判断の検証 / 学習
- Matured observations: 291
- Eligible for model-change review: True
- [WATCH] regime / NEUTRAL|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [WATCH] rank_bucket / top1|1w: Benchmark-relative performance is historically weak; review assumptions before increasing its influence.
- [INFO] rank_bucket / top3|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

## 7. データ品質 / 反証
- Quality score: 0.735
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.077
- Secondary fundamental coverage: 0.769
- Effective fundamental coverage: 0.577
- Fundamental evidence tier: mixed
- Missing data must not be converted into unsupported buy/sell conclusions.

## 8. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

<!-- PAYPAY_SWING_START -->
## PayPay Swing

- 監視判定: **WAIT_RESEARCH** — 首位ビットコインは79.8点だが確認閾値未達
- 上位: ビットコイン 79.8 / スタンダード 77.1 / テクノロジー 76.0
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
