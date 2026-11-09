# 売買判断優先・市場急変チェック

生成（UTC）：2026-11-09T01:48:51.790781+00:00
**危機判定：CRITICAL**
**判断：RISK_REDUCTION_REVIEW**

## 急変要因
- 日経円建て先物(CME)が-5%以下
- 日経円建て先物(CME)が-3%以下
- 日経円建て先物(CME)が-1.5%以下

## データ基準時刻・品質
- NIKKEI_FUT: OK / -7.151% / 2026-11-09T01:38:46+00:00 / 
- NASDAQ: UNVERIFIED / N/A% / 2026-11-06T22:15:59+00:00 / stale or future timestamp; excluded from decisions
- SP500: UNVERIFIED / N/A% / 2026-11-06T21:37:09+00:00 / stale or future timestamp; excluded from decisions
- VIX: UNVERIFIED / N/A% / 2026-11-06T21:15:01+00:00 / stale or future timestamp; excluded from decisions

## 売買判断まとめ
- 新規買い停止
- 既存買い指値の取消を優先審査
- 下落に弱い保有銘柄の利益確定・縮小を寄り前に審査
- 防衛資金維持

**個別銘柄・数量・成行/指値は非公開PF、注文履歴、最新板を照合して決定。自動売買なし。**
