# Exception Alerts v1.9.1

Generated: 2026-09-30T15:53:31+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 9
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FINANCING [信越化学工業]: 信越化学工業[4063]：取締役、執行役員及び従業員に対するストックオプション（新株予約権）の払込金額確定のお知らせ 2026年9月30日(適時開示) ：日経会社情報DIGITAL - nikkei.com
  - New company event detected for 信越化学工業.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: au PAY アプリ上から使える暗号資産ウォレットを提供開始 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、10月から楽天へ回線貸し縮小 横浜・神戸など18政令市の市街地 - nikkei.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、全国基地局の現地保守支援システムに「テックタッチ」採用 データ入力の誤りを10分の1に削減 - enterprisezine.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - xtech.nikkei.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECとシュナイダー、電力・通信設備管理「ArcFM」を国内提供--GISで設計から運用まで一元化 - japan.zdnet.com
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：板気配 - finance.yahoo.co.jp
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス、先端半導体の動作解析向け顕微鏡 AIチップに対応 - nikkei.com
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 半導体部品の故障を高い精度で特定 浜松ホトニクス、解析装置の受注開始：ニュース - 中日BIZナビ
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
