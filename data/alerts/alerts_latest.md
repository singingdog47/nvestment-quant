# Exception Alerts v1.9.1

Generated: 2026-10-12T16:59:56+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 2
- INFO: 0

## Alerts
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: (株)ほくほくフィナンシャルグループ【8377】：板気配 - Yahoo!ファイナンス
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
