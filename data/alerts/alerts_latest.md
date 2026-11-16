# Exception Alerts v1.9.1

Generated: 2026-11-16T02:14:26+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 6
- WATCH: 1
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [National Health Investors, Inc. Common Stock]: SEC 8-K filing
  - New company event detected for National Health Investors, Inc. Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Nippon Shinyaku Co.,Ltd.]: 半期報告書－第164期(2026/04/01－2027/03/31)
  - New company event detected for Nippon Shinyaku Co.,Ltd..
- **WARNING** COMPANY_EVENT/EVENT_FILING [Nippon Shinyaku Co.,Ltd.]: 確認書
  - New company event detected for Nippon Shinyaku Co.,Ltd..
- **WARNING** COMPANY_EVENT/EVENT_FILING [ほくほくフィナンシャルグループ]: 半期報告書－第24期(2026/04/01－2027/03/31)
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** COMPANY_EVENT/EVENT_FILING [ほくほくフィナンシャルグループ]: 確認書
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** REGIME/REGIME_CHANGE: Market regime changed
  - Market regime changed from DEFENSIVE to NEUTRAL.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
