# Exception Alerts v1.9.1

Generated: 2026-10-13T15:56:01+00:00
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
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIと連携し店付近でモバイルバッテリー等の回収を都内1カ所で実施｜ローソン公式サイト - LAWSON
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 「安さのその先へ」──ライフドリンク カンパニーの成長を支える「脱付加価値戦略」とは - ECのミカタ
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
