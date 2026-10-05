# Exception Alerts v1.9.1

Generated: 2026-10-05T17:07:39+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 5
- INFO: 0

## Alerts
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、150ジョブ「図鑑」でキャリア磨き 職務定義書はあえて大ざっぱ - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、欧州にセキュリティ監視センターを設置--24時間の監視体制 - ZDNET Japan
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 「安さのその先へ」──ライフドリンク カンパニーの成長を支える「脱付加価値戦略」とは - ecnomikata.com
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 先端半導体の後工程向け…浜松ホトニクス、故障解析装置の機能 - ニュースイッチ by 日刊工業新聞社
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
