# Exception Alerts v1.9.1

Generated: 2026-09-30T15:21:31+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Aurinia Pharmaceuticals Inc - Common Shares]: SEC 8-K filing
  - New company event detected for Aurinia Pharmaceuticals Inc - Common Shares.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: au PAY アプリ上から使える暗号資産ウォレットを提供開始 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、楽天モバイルへのローミング状況を公開 9月末から大幅減 10月から新たな枠組み（ITmedia Mobile） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 東大・東芝・NECら、反射板とDASを活用した高速道路向けローカル5Gの実証 - ビジネスネットワーク
  - New company event detected for NEC.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
