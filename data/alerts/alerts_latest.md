# Exception Alerts v1.9.1

Generated: 2026-09-29T15:07:07+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 1
- INFO: 0

## Alerts
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが挑んだ「デジタルマーケティング内製化」7年の軌跡！人材育成とコスト削減を実現した組織改革の全貌 - ダイヤモンド・オンライン
  - New company event detected for KDDI.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
