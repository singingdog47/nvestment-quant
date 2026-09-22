# Exception Alerts v1.9.1

Generated: 2026-09-22T12:39:10+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Imperial Petroleum Inc. - Common Shares]: SEC 6-K filing
  - New company event detected for Imperial Petroleum Inc. - Common Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Imperial Petroleum Inc. - Common Shares]: SEC 6-K filing
  - New company event detected for Imperial Petroleum Inc. - Common Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Millrose Properties, Inc. Class A Common Stock]: SEC 8-K filing
  - New company event detected for Millrose Properties, Inc. Class A Common Stock.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: リテールロボットを活用した分散型データセンター実証を開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECと住友電工、ペタビット級海底ケーブルでメタと協業（時事通信） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC川崎が好きな選手のサイン入りグッズが当たるキャンペーンを開始！ - バレーボールキング
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - finance.yahoo.co.jp
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
