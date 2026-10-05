# Exception Alerts v1.9.1

Generated: 2026-10-05T16:22:37+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 3
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: 定款 2026/10/01 投稿日時： 2026/10/01 10:10[適時開示] - みんかぶ
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 先端半導体の後工程向け…浜松ホトニクス、故障解析装置の機能 - newswitch.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
