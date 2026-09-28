# Exception Alerts v1.9.1

Generated: 2026-09-28T15:32:54+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 5
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: 信越化、今期配当を20円増額修正 - 株探
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [浜松ホトニクス]: 浜松ホトニクスは2026年9月29日に1株配当金0.1672USDを支払う予定 - Moomoo
  - New company event detected for 浜松ホトニクス.
- **WARNING** COMPANY_EVENT/EVENT_FILING [ACNB Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for ACNB Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Japan Investment Adviser Co.,Ltd.]: 発行登録書（株券､社債券等）
  - New company event detected for Japan Investment Adviser Co.,Ltd..
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: カカクコム、KDDIと資本提携解消（時事通信） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 【アナリスト評価】ＫＤＤＩ、レーティング強気を継続、目標株価3,500円に引上げ（日系大手証券）(アイフィス株予報) - finance.yahoo.co.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 日本郵便とKDDI、ドローン社会基盤化へ基本合意書を締結し、郵便局をドローンポート拠点とする実証を開始 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、日本郵便とドローン事業で連携 全国の郵便局に発着拠点 - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: カカクコムとＫＤＤＩが資本提携解消、第2位株主の地位変わらず - reuters.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ【6701】：今の株価の理由は？値動きの背景をAIが解説 - finance.yahoo.co.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: サイバー攻撃のリスクから事業継続を考える - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC保有の「カーボンナノチューブを発見した電子顕微鏡」が日本物理遺産に認定 | 日本電気株式会社のプレスリリース - PR TIMES
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：板気配 - finance.yahoo.co.jp
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学のストックオプション発行に対し、投資家はどのように反応しているか - simplywall.st
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：決算情報 - finance.yahoo.co.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス[6965]の株価・株主優待など。 - 日本経済新聞
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - finance.yahoo.co.jp
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
