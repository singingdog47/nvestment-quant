# Exception Alerts v1.9.1

Generated: 2026-09-30T01:19:55+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 10
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: 信越化、今期配当を20円増額修正 - 株探
  - New company event detected for 信越化学工業.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、日本郵便とドローン事業で連携 全国の郵便局に発着拠点 - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、次世代の法人向けネットワーク基盤「AccelWaves」構想発表、AI本格導入に向け“つぎはぎ状態”の解消をアピール - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、AI時代の企業ネットワーク基盤「AccelWaves」構想を発表 SASE一体型サービスや自律型ネットワークを展開 - クラウド Watch
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループの英国現代奴隷法への対応 : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - 日経クロステック
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECなど5社、総務省の令和8年度「ワット・ビット連携関連実証」に採択 (2026年9月30日): プレスリリース - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC（日本電気）の50代後半・部長級の年収は？【1万件の口コミ情報データ】 - ダイヤモンド・オンライン
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECが「AI自律型組織」を新設 「従業員はいらなくなる？」の問いに、CAXOはどう答えたか（ITmedia エンタープライズ） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス ＡＩ向け半導体特化 故障解析装置 新たな主力 顧客開拓狙う - 静岡新聞DIGITAL
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス、AI半導体向け倒立型エミッション顕微鏡を発売 - optronics-media.com
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
