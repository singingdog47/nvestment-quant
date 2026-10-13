# Exception Alerts v1.9.1

Generated: 2026-10-13T15:16:46+00:00
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
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
