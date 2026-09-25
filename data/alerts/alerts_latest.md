# Exception Alerts v1.9.1

Generated: 2026-09-25T12:49:20+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 1
- INFO: 0

## Alerts
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** REGIME/REGIME_CHANGE: Market regime changed
  - Market regime changed from CONSTRUCTIVE to RISK_ON.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
