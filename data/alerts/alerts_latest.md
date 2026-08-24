# Exception Alerts v1.9

Generated: 2026-08-24T00:37:31+00:00
Highest severity: **WATCH**

## Counts
- CRITICAL: 0
- WARNING: 0
- WATCH: 2
- INFO: 0

## Alerts
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ(株)【9433】：株主優待 - Yahoo!ファイナンス
  - New company event detected for KDDI.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
