# Exception Alerts v1.9.1

Generated: 2026-09-21T14:13:55+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 8
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: 信越化、今期配当を20円増額修正 - 株探
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [Mechanics Bancorp - Class A Common Stock]: SEC 10-Q filing
  - New company event detected for Mechanics Bancorp - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Mechanics Bancorp - Class A Common Stock]: SEC 8-K filing
  - New company event detected for Mechanics Bancorp - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Mechanics Bancorp - Class A Common Stock]: SEC 8-K filing
  - New company event detected for Mechanics Bancorp - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Tokai Tokyo Financial Holdings,Inc.]: 訂正臨時報告書
  - New company event detected for Tokai Tokyo Financial Holdings,Inc..
- **WARNING** COMPANY_EVENT/EVENT_FILING [Tokai Tokyo Financial Holdings,Inc.]: 訂正発行登録書
  - New company event detected for Tokai Tokyo Financial Holdings,Inc..
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [浜松ホトニクス]: 浜松ホトニクス---ストップ高、1-3月期増益転換で通期予想を上方修正 - 株探
  - New company event detected for 浜松ホトニクス.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIローミング終了に揺れる楽天モバイルと銀行業に期待がかかるドコモ - ケータイ Watch
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループの英国現代奴隷法への対応 : 企業情報 - group.nec
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - diamond.jp
  - New company event detected for 信越化学工業.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
