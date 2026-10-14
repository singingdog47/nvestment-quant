# Exception Alerts v1.9.1

Generated: 2026-10-14T01:16:06+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 10
- WATCH: 10
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: キヤノン、信越化学工業も…「下落が怖い」人向け"高配当"半導体・AI株7銘柄の実名 - 現代ビジネス
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [水戸証券]: 水戸証券[8622]：期末配当（予定）および創業105周年記念配当（予定）に関するお知らせ 2026年3月6日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WARNING** COMPANY_EVENT/EVENT_FILING [CMB.TECH NV Ordinary Shares]: SEC 6-K filing
  - New company event detected for CMB.TECH NV Ordinary Shares.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Expand Energy Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for Expand Energy Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [First Busey Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for First Busey Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [TORM plc - Class A Common Stock]: SEC 6-K filing
  - New company event detected for TORM plc - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [三越伊勢丹ホールディングス]: 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
  - New company event detected for 三越伊勢丹ホールディングス.
- **WARNING** LIQUIDITY/LIQUIDITY_WEAK: Market liquidity is weak
  - Liquidity component fell below 25/100.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ(株)【5032】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: (株)ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ【3563】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: JR西日本SC開発とKDDIが共同でAIサービス 商業施設開発を一貫で支援 - 繊研新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: LG CNSとアジア太平洋地域での事業拡大に向けた基本合意書を締結 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 現場画像に小さく写る被害を高精度に把握し、新たな被災事象にも対応できるVLM技術を開発 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECネクサソリューションズ、承認ワークフロー「EXPLANNER/FLII」の画面を刷新 - IT Leaders
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: (株)コーエーテクモホールディングス【3635】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス(株)【8766】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
