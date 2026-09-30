# Exception Alerts v1.9.1

Generated: 2026-09-30T13:48:01+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 9
- WATCH: 11
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [ACNB Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for ACNB Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Shionogi & Co.,Ltd.]: 訂正有価証券報告書－第161期(2025/04/01－2026/03/31)
  - New company event detected for Shionogi & Co.,Ltd..
- **WARNING** COMPANY_EVENT/EVENT_FILING [Shionogi & Co.,Ltd.]: 確認書
  - New company event detected for Shionogi & Co.,Ltd..
- **WARNING** COMPANY_EVENT/EVENT_FILING [信越化学工業]: 訂正臨時報告書
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_FILING [信越化学工業]: 訂正有価証券届出書（参照方式）
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_FINANCING [信越化学工業]: 信越化学工業[4063]：取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ 2026年9月30日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_FINANCING [信越化学工業]: 信越化(4063) 取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ - みんかぶ
  - New company event detected for 信越化学工業.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: カカクコム、KDDIと資本提携解消（時事通信） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、企業のデータ容量をAIで最適化へ（時事通信） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: au PAY アプリ上から使える暗号資産ウォレットを提供開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、10月から楽天へ回線貸し縮小 横浜・神戸など18政令市の市街地 - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、全国基地局の現地保守支援システムに「テックタッチ」採用 データ入力の誤りを10分の1に削減 - EnterpriseZine
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - 日経クロステック（xTECH）
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 地方でGPUを共同利用へ NECなど5社、APNで地域分散型データセンターを実証（電波タイムズ） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECとシュナイダー、電力・通信設備管理「ArcFM」を国内提供--GISで設計から運用まで一元化 - ZDNET Japan
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ、仏シュナイダーのＧＩＳを活用したソリューション提供 速報 - kabushiki.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 半導体部品の故障を高い精度で特定 浜松ホトニクス、解析装置の受注開始：ニュース - biz.chunichi.co.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
