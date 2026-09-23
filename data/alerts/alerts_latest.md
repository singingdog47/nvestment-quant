# Exception Alerts v1.9.1

Generated: 2026-09-23T12:47:48+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 2
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Millrose Properties, Inc. Class A Common Stock]: SEC 8-K filing
  - New company event detected for Millrose Properties, Inc. Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FINANCING [信越化学工業]: 信越化学工業[4063]：ストックオプション（新株予約権）の割当てに関するお知らせ 2026年9月15日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 通信事業者間での5Gミリ波の利用エリア拡大に向けた共同検討を開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
