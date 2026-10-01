# Exception Alerts v1.9.1

Generated: 2026-10-01T01:19:43+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 8
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Scorpio Tankers Inc. Common Shares]: SEC 6-K filing
  - New company event detected for Scorpio Tankers Inc. Common Shares.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: カカクコム、KDDIと資本提携解消（時事通信） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 楽天モバイル、携帯「独り立ち」へ正念場 ＫＤＤＩの回線貸し出し縮小―基地局整備、ライバルに遅れ - 時事ドットコム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 「Xperia 10 VIII」をauから10月8日に発売 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 障がい者雇用を、採用から定着・育成まで支える「NECグループ障がい者雇用相談センター」を開設 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、富士通を20年ぶり逆転 AIと安全保障で挑む森田改革の正念場 - nikkei.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECなど5社、総務省「ワット・ビット連携関連実証」に採択 - INTERNET Watch
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：板気配 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [浜松ホトニクス]: ＜人事＞浜松ホトニクス - 産経ニュース
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
