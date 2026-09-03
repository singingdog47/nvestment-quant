# Investment Quant Daily Integrated Report v2.10

Generated (UTC): 2026-09-03T07:30:46+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 64.52
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 15.199999809265137
- Treasury realized-vol proxy (not ICE MOVE): 70.338 bps annualized; percentile=0.631
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 12, 'WARNING': 2, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / 臨時報告書
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WATCH] COMPANY_EVENT / 「KDDI」の株主優待は、最大3000円相当のPontaポイントがもらえてお得！ 受け取った「Pontaポイント」は、ローソンなどで現金同様に使えるのも魅力！ - diamond.jp
- [WATCH] COMPANY_EVENT / KDDIとローソン、コンビニ横でリチウムイオン電池を回収 - Impress Watch
- [WATCH] COMPANY_EVENT / 「オフィスローソン」を京セラ本社の食堂2フロアに導入（KDDI/ローソン） - ペイメントナビ
- [WATCH] COMPANY_EVENT / 山口県とKDDI、地域課題の解決に向けた包括連携協定を締結 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / 日本企業の生存戦略：KDDI髙橋氏、オリックス宮内氏、平井卓也氏が語るスタートアップ共創とAI実装 - Biz/Zine
- [WATCH] COMPANY_EVENT / 三菱重工業、株価反発 NECと防衛ドローンで連携 - 日本経済新聞

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.8603449462594 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=76.91809720496848 | cross_pct=99.94884910485933
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=76.59858190537834 | cross_pct=99.89769820971867
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=4.0 | raw=76.22432133536792 | cross_pct=99.846547314578
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=73.2935569988791 | cross_pct=99.59079283887468

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.00517413160702 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.33184409152624 | cross_pct=99.97080291970802
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.92762189703669 | cross_pct=99.94160583941606
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=4.0 | raw=82.37775876643708 | cross_pct=99.91240875912408
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=8.0 | raw=81.80204249501882 | cross_pct=99.7956204379562

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.00517413160702
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.8603449462594
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97080291970802 | raw=83.33184409152624
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94884910485933 | raw=76.91809720496848
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94160583941606 | raw=82.92762189703669
- 6. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.91240875912408 | raw=82.37775876643708
- 7. [JP] Akatsuki Inc. | cross_pct=99.89769820971867 | raw=76.59858190537834
- 8. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.846547314578 | raw=76.22432133536792
- 9. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.7956204379562 | raw=81.80204249501882
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.7080291970803 | raw=80.79508831956039
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 5. 過去判断の検証 / 学習
- Matured observations: 29
- Eligible for model-change review: False
- [INFO] regime / CONSTRUCTIVE|1w: Benchmark-relative performance is historically positive; retain for monitoring, not automatic promotion.

## 6. データ品質 / 反証
- Quality score: 0.745
- Primary source health (configured feeds only): 1.0
- Primary fundamental coverage: 0.0
- Secondary fundamental coverage: 1.0
- Effective fundamental coverage: 0.65
- Fundamental evidence tier: secondary_only
- Missing data must not be converted into unsupported buy/sell conclusions.

## 7. ポートフォリオ
- 公開版には保有情報・私有リスク値を保存しません。
- 同一実行内で private engine が成功した場合、リスク・バリュエーション・月次寄与度を私有版に統合します。
- 残高増減はTWRとして扱わず、入出金境界データが不足する場合は運用成績を withheld にします。

## 8. 開発状況 / 復旧準備
- System version: v2.10
- Development: operational; private Drive history, valuation, monthly attribution v1.1, dynamic cash/tax friction and anti-FOMO execution controls active
- Stable fallback branch: `stable-report-v2.6`
- Rollback ready: `True`
- 新版で障害が起きても、固定安定版から公開レポートを生成できる経路を維持します。

## 9. ガードレール
- このレポートは売買指示ではなく、意思決定支援です。
- 自動発注・自動因子ウェイト変更は行いません。
- 『何もしない / 待つ』を常に有効な選択肢として扱います。
