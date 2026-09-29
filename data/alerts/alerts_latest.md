# Exception Alerts v1.9.1

Generated: 2026-09-29T15:44:11+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 3
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Japan Investment Adviser Co.,Ltd.]: 発行登録書（株券､社債券等）
  - New company event detected for Japan Investment Adviser Co.,Ltd..
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが自律型ネットワーク構想を発表、パロアルトと協業しSASE提供 - ZDNET Japan
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループの英国現代奴隷法への対応 : 企業情報 - group.nec
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - xtech.nikkei.com
  - New company event detected for NEC.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
