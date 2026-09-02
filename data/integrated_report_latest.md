# Investment Quant Daily Integrated Report v2.10

Generated (UTC): 2026-09-02T07:29:35+00:00

## 1. 結論 / 今日の優先アクション
- **RISK REVIEW BEFORE NEW ACTION**
- Decision gate: `OPEN_FOR_ANALYSIS`
- Screening / intelligence data actionable: `True`
- Regime context actionable: `True`
- Overall analysis mode: `OPEN_FOR_ANALYSIS`

## 2. 市場レジーム
- Regime: **CONSTRUCTIVE**
- Score: 65.71
- Confidence: 1.0
- Data status: ok
- Actionability reasons: none
- VIX: 16.34000015258789
- Treasury realized-vol proxy (not ICE MOVE): 70.498 bps annualized; percentile=0.6389
- Flags: none

## 3. 例外検知 / アラート
- Highest severity: **WARNING**
- Counts: {'INFO': 0, 'WATCH': 9, 'WARNING': 4, 'CRITICAL': 0}
- [WARNING] COMPANY_EVENT / SEC 10-Q filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / SEC 8-K filing
- [WARNING] COMPANY_EVENT / 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
- [WATCH] COMPANY_EVENT / NTT、KDDI、楽天モバイルなど、NW設計を共同で国際標準化 - ケータイ Watch
- [WATCH] COMPANY_EVENT / 山口県とKDDI、地域課題の解決に向けた包括連携協定を締結 - KDDI ニュースルーム
- [WATCH] COMPANY_EVENT / KDDI、7GHz帯で6G向け実証 ダウンリンク3.6Gbpsを達成 - EnterpriseZine
- [WATCH] COMPANY_EVENT / NECよどこへ行く 森田改革の成否 - xtech.nikkei.com

## 4. スクリーニング上位候補

### 日本株（市場内順位）
- 1. Mito Securities Co.,Ltd. 8622.T | market_rank=1.0 | raw=77.81548825399197 | cross_pct=100.0
- 2. Ichiyoshi Securities Co.,Ltd. 8624.T | market_rank=2.0 | raw=76.87747622240465 | cross_pct=99.94892747701736
- 3. Akatsuki Inc. 3932.T | market_rank=3.0 | raw=76.47277114841758 | cross_pct=99.89785495403473
- 4. IwaiCosmo Holdings,Inc. 8707.T | market_rank=5.0 | raw=75.97510792220683 | cross_pct=99.79570990806947
- 5. ELECOM CO.,LTD. 6750.T | market_rank=9.0 | raw=73.29934561734898 | cross_pct=99.59141981613891

### 米国株（市場内順位）
- 1. Carter Bankshares, Inc. - Common Stock CARE | market_rank=1.0 | raw=84.05397409180718 | cross_pct=100.0
- 2. Millrose Properties, Inc. Class A Common Stock MRP | market_rank=2.0 | raw=83.49741068442289 | cross_pct=99.97071742313324
- 3. International Seaways, Inc. Common Stock  INSW | market_rank=3.0 | raw=82.80940193552783 | cross_pct=99.94143484626647
- 4. Okeanis Eco Tankers Corp. Common Stock ECO | market_rank=5.0 | raw=82.29513627727107 | cross_pct=99.88286969253294
- 5. Norwood Financial Corp. - Common Stock NWFL | market_rank=8.0 | raw=81.60589842764803 | cross_pct=99.79502196193265

### 市場横断リサーチ候補（市場内パーセンタイル比較）
- 1. [US] Carter Bankshares, Inc. - Common Stock | cross_pct=100.0 | raw=84.05397409180718
- 2. [JP] Mito Securities Co.,Ltd. | cross_pct=100.0 | raw=77.81548825399197
- 3. [US] Millrose Properties, Inc. Class A Common Stock | cross_pct=99.97071742313324 | raw=83.49741068442289
- 4. [JP] Ichiyoshi Securities Co.,Ltd. | cross_pct=99.94892747701736 | raw=76.87747622240465
- 5. [US] International Seaways, Inc. Common Stock  | cross_pct=99.94143484626647 | raw=82.80940193552783
- 6. [JP] Akatsuki Inc. | cross_pct=99.89785495403473 | raw=76.47277114841758
- 7. [US] Okeanis Eco Tankers Corp. Common Stock | cross_pct=99.88286969253294 | raw=82.29513627727107
- 8. [JP] IwaiCosmo Holdings,Inc. | cross_pct=99.79570990806947 | raw=75.97510792220683
- 9. [US] Norwood Financial Corp. - Common Stock | cross_pct=99.79502196193265 | raw=81.60589842764803
- 10. [US] Adamas Trust, Inc. - Common Stock | cross_pct=99.70717423133236 | raw=80.87427042454644
- 注: cross_pct は各市場内での相対順位。日米の絶対的な割安度・事業品質が同一尺度という意味ではありません。

## 5. 過去判断の検証 / 学習
- Matured observations: 25
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
