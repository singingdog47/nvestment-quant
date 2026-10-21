# Exception Alerts v1.9.1

Generated: 2026-10-21T00:39:58+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [NEC]: NEC 委託先へのサイバー攻撃で個人情報漏えい - TBS NEWS DIG
  - New company event detected for NEC.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ(株)【5032】：決算情報 - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: NIJISANJI EN Announces “NØVA -Cosmic Stage-” - ANYCOLOR株式会社
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: (株)ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ【3563】：決算情報 - Yahoo!ファイナンス
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ（3563）の株主優待｜国内株式 - SBI証券
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: モンゴルの自然保護区で大規模火災、出火原因は日系企業 - オルタナ
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: モンゴルで大規模草原火災 日系企業の車が原因か（共同通信） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI財団、京大大学院理学研究科主催小学生向けイベント共催 科学の面白さ伝える - 電波新聞デジタル
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、委託先にサイバー攻撃（時事通信） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『信長の野望 覇道』公式生放送 - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 三越伊勢丹が見つける、日本の知られざる価値「think good」秋のキャンペーンを10月7日(水)から開催 - PR TIMES
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 2026.10.20 貨物列車（3099列車）秋田駅発車 秋田駅約2分遅れ - YouTube
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業、東京エレクトロン…エヌビディア、サムスンが熱視線を送る日本企業の基盤技術 - JBpress
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: M2X、東京海上ホールディングスと業務提携…製造業の設備保全DXを共同推進 - レスポンス（Response.jp）
  - New company event detected for 東京海上ホールディングス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
