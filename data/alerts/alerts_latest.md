# Exception Alerts v1.9.1

Generated: 2026-10-19T16:26:41+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 4
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Scorpio Tankers Inc. Common Shares]: SEC 6-K filing
  - New company event detected for Scorpio Tankers Inc. Common Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Scorpio Tankers Inc. Common Shares]: SEC 6-K filing
  - New company event detected for Scorpio Tankers Inc. Common Shares.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 都市部でKDDIローミング縮小、楽天モバイルに問われる通信品質と収益改善 - 日経クロステック
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ハセットNEC委員長、インフレになお政策対応必要との見方示す－CNBC - Bloomberg.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: (株)ライフドリンクカンパニー【2585】：決算説明会書き起こし - Yahoo!ファイナンス
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
