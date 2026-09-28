# Exception Alerts v1.9.1

Generated: 2026-09-28T00:49:50+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 12
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: 信越化学工業[4063]：創立100周年記念配当の実施 及び 配当予想の修正に関するお知らせ 2026年9月15日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_FILING [LTC Properties, Inc. Common Stock]: SEC 8-K filing
  - New company event detected for LTC Properties, Inc. Common Stock.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが「SMS共通番号」の利用を開始、10月6日から - ケータイ Watch
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、豪州でも衛星通信利用可能に 日本人旅行者向け - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 次世代シアター「Immersive Zero」に出演者動作連動型3D音響を導入 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - 日経クロステック
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 数百基の光通信衛星で大容量通信を実現へ、ＮＥＣが整備計画…日本独自の衛星網で経済安保強化 - 読売新聞
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 遠隔通信なのにまるで対面しているよう…NECネッツ、3Dビデオ機器投入 - ニュースイッチ by 日刊工業新聞社
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学のストックオプション発行に対し、投資家はどのように反応しているか - simplywall.st
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 【半導体人材の未来】〈42〉「浜松ホトニクスが目標」 台湾の大学連合ブースから世界市場へ - 電波新聞デジタル
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [浜松ホトニクス]: 浜松ホトニクス[6965]：取締役候補者の選任及び執行役員人事（予定）に関するお知らせ 2026年9月25日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [浜松ホトニクス]: ＜人事＞浜松ホトニクス - 産経ニュース
  - New company event detected for 浜松ホトニクス.
- **WATCH** REGIME/REGIME_CHANGE: Market regime changed
  - Market regime changed from RISK_ON to CONSTRUCTIVE.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
