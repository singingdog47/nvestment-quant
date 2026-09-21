# Exception Alerts v1.9.1

Generated: 2026-09-21T15:06:31+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 4
- WATCH: 5
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [Norwood Financial Corp. - Common Stock]: SEC 10-Q filing
  - New company event detected for Norwood Financial Corp. - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Norwood Financial Corp. - Common Stock]: SEC 8-K filing
  - New company event detected for Norwood Financial Corp. - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Norwood Financial Corp. - Common Stock]: SEC 8-K filing
  - New company event detected for Norwood Financial Corp. - Common Stock.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: つくば市で自動運転バスの本格運行を10月2日から開始 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループの英国現代奴隷法への対応 : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 昨季発生、NECグリーンロケッツ東葛の不祥事2件に懲罰。複数選手・スタッフも関与。チームの責任、過失も明らかに - rugby-rp.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
