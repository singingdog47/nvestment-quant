# Exception Alerts v1.9.1

Generated: 2026-09-22T00:53:16+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Millrose Properties, Inc. Class A Common Stock]: SEC 8-K filing
  - New company event detected for Millrose Properties, Inc. Class A Common Stock.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: つくば市で自動運転バスの本格運行を10月2日から開始 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 昨季発生、NECグリーンロケッツ東葛の不祥事2件に懲罰。複数選手・スタッフも関与。チームの責任、過失も明らかに - rugby-rp.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業 化学品銘柄からAI銘柄へ 斉藤社長に聞く【大浜見聞録】 - テレ東BIZ
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: マーケット速報 - 北國新聞
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
