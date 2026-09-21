# Exception Alerts v1.9.1

Generated: 2026-09-21T15:21:55+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [HCI Group, Inc. Common Stock]: SEC 10-Q filing
  - New company event detected for HCI Group, Inc. Common Stock.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: つくば市で自動運転バスの本格運行を10月2日から開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 昨季発生、NECグリーンロケッツ東葛の不祥事2件に懲罰。複数選手・スタッフも関与。チームの責任、過失も明らかに - ラグビーリパブリック
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス－ＳＭＢＣ日興が投資評価引き下げ 業績回復により期待は織り込まれた - TradingView
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
