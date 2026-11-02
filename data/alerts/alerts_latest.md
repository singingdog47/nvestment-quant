# Exception Alerts v1.9.1

Generated: 2026-11-02T17:26:40+00:00
Highest severity: **WATCH**

## Counts
- CRITICAL: 0
- WARNING: 0
- WATCH: 4
- INFO: 0

## Alerts
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 【出演情報】吉俣良 ４５周年Anniversary Concert Supported by KDDI ｜soyokaze - fan.pia.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIと米国Wingが提携、27年にローソン商品などドローン配送へ - ドローンジャーナル
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ【6701】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス フィジカルAI搭載ロボの保険開始 - ABEMA
  - New company event detected for 東京海上ホールディングス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
