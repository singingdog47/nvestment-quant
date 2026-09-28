# Exception Alerts v1.9.1

Generated: 2026-09-28T17:37:49+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 10
- INFO: 0

## Alerts
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: カカクコム、KDDIと資本提携解消（時事通信） - news.yahoo.co.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 【アナリスト評価】ＫＤＤＩ、レーティング強気を継続、目標株価3,500円に引上げ（日系大手証券）(アイフィス株予報) - finance.yahoo.co.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループの英国現代奴隷法への対応 : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: サイバー攻撃のリスクから事業継続を考える - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 光通信衛星を数百基整備 NEC計画 - news.yahoo.co.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：板気配 - finance.yahoo.co.jp
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：決算情報 - finance.yahoo.co.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - finance.yahoo.co.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [浜松ホトニクス]: ＜人事＞浜松ホトニクス - sankei.com
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [浜松ホトニクス]: 浜松ホトニクス[6965]：取締役候補者の選任及び執行役員人事（予定）に関するお知らせ 2026年9月25日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
