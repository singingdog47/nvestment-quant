# Exception Alerts v1.9.1

Generated: 2026-10-28T15:05:09+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 6
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [東京海上ホールディングス]: 東京海上、今期配当を実質増額修正 - 株探
  - New company event detected for 東京海上ホールディングス.
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [水戸証券]: 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: FOOD＆LIFE（3563）FY2026 月次情報 (9月期) - 四季報オンライン
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス(株)【8766】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス[8766]の株価・株主優待など。 - 日本経済新聞
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上HD、株主優待を新設！ 3月末に100株を3年以上保有で2027年3月は7500円分、2028年以降も継続保有すると2500円分の電子マネーなどがもらえる！ - ダイヤモンド・オンライン
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券株式会社 | 導入事例 | 法人のお客さま | ソフトバンク - ソフトバンク
  - New company event detected for 水戸証券.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
