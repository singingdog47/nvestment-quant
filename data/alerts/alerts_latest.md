# Exception Alerts v1.9.1

Generated: 2026-10-12T16:47:01+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 5
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Imperial Petroleum Inc. - Common Shares]: SEC 6-K filing
  - New company event detected for Imperial Petroleum Inc. - Common Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Imperial Petroleum Inc. - Common Shares]: SEC 6-K filing
  - New company event detected for Imperial Petroleum Inc. - Common Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Imperial Petroleum Inc. - Common Shares]: SEC 6-K filing
  - New company event detected for Imperial Petroleum Inc. - Common Shares.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 人とAIで実現する次世代セキュリティ｜KDDI SUMMIT 2026 | イベント・セミナー | LAC WATCH - 株式会社ラック
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: au PAY アプリ上から使える暗号資産ウォレットを提供開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.
- **WATCH** REGIME/REGIME_CHANGE: Market regime changed
  - Market regime changed from RISK_ON to CONSTRUCTIVE.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
