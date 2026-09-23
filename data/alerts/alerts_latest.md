# Exception Alerts v1.9.1

Generated: 2026-09-23T00:37:57+00:00
Highest severity: **WATCH**

## Counts
- CRITICAL: 0
- WARNING: 0
- WATCH: 3
- INFO: 0

## Alerts
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 攻撃者より先に動くサイバーセキュリティへ - kddi-research.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC川崎「日本一を」 女子バレー SVリーグ来月開幕 - 東京新聞
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: マーケット速報 - 北國新聞
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
