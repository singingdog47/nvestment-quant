# Exception Alerts v1.9.1

Generated: 2026-09-25T00:35:25+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 4
- WATCH: 10
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: 信越化学工業[4063]：創立100周年記念配当の実施 及び 配当予想の修正に関するお知らせ 2026年9月15日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_FILING [TORM plc - Class A Common Stock]: SEC 6-K filing
  - New company event detected for TORM plc - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [浜松ホトニクス]: 決算:浜松ホトニクス、26年9月期の純利益23%増 半導体関連伸び上方修正 - 日本経済新聞
  - New company event detected for 浜松ホトニクス.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: コンビニの品出しはロボットに? KDDI×韓国RLWRLDが挑む「フィジカルAI」 - Impress Watch
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: NTTデータ、KDDI、日立、JR東が語る「判断の再設計」メソッド、AIとデータどう活用？ - ビジネス+IT
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIら、つくば市で自動運転バスが本格運行へ 筑波大学循環で10月2日開始 - LIGARE（リガーレ）
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 海底ケーブルは「P（ペタ）bpsの時代」へ、NECが大容量化などの取り組みを説明 - INTERNET Watch
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: Meta、NEC、住友電工の3社、ペタビット級海底ケーブル「Petal」の構築に向け協業（クラウド Watch） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: CMP初の認証取得アプリケーション 「ProChemist/CMP」 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - 日経クロステック
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学のストックオプション発行に対し、投資家はどのように反応しているか - simplywall.st
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 【特許】浜松ホトニクス、反射型エンコーダーの精度向上 - 日本経済新聞
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
