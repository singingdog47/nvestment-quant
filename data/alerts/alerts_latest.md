# Exception Alerts v1.9.1

Generated: 2026-10-06T02:20:56+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 5
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [ANYCOLOR]: 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞
  - New company event detected for ANYCOLOR.
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [水戸証券]: 水戸証券(8622)、4期連続となる「増配」を発表し、配当利回り5.9％に！ 年間配当は4年で3.0倍に増加、2026年3月期は前期比13円増の｢1株あたり43円｣に！ - diamond.jp
  - New company event detected for 水戸証券.
- **WARNING** COMPANY_EVENT/EVENT_FILING [TORM plc - Class A Common Stock]: SEC 6-K filing
  - New company event detected for TORM plc - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_MNA [ライフドリンク カンパニー]: ライフドリンクカンパニー、新設子会社を通じてスキマデパートからSDネクストおよびSDボトラーズを買収 - marr.jp
  - New company event detected for ライフドリンク カンパニー.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: NIJISANJI EN Announces “NØVA -Cosmic Stage-” - ANYCOLOR株式会社
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: (株)ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ【3563】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIのローミング縮小でも「やめる理由にはならない」 楽天モバイルユーザー4人が語る本音と“経済圏”の囲い込み - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: sXGPでクレーン無線の混信抑制 NEC通信システム・竹中工務店が開発 - ビジネスネットワーク
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『三國志 覇道』10月度公式生放送 #ハドウへの道 - gamecity.ne.jp
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 「安さのその先へ」──ライフドリンク カンパニーの成長を支える「脱付加価値戦略」とは - ECのミカタ
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - diamond.jp
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: マーケット速報 - 北國新聞
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: M2X、東京海上ホールディングスと業務提携…製造業の設備保全DXを共同推進 - response.jp
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上HD、株主優待を新設！ 3月末に100株を3年以上保有で2027年3月は7500円分、2028年以降も継続保有すると2500円分の電子マネーなどがもらえる！ - diamond.jp
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 2026水戸証券チャレンジフェスティバル開催のお知らせ《7/27情報更新》 - mito-hollyhock.net
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 先進半導体パッケージの故障解析、浜松ホトニクスが新装置 (EE Times Japan) - Yahoo!ニュース
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 半導体部品の故障を高い精度で特定 浜松ホトニクス、解析装置の受注開始：ニュース - 中日BIZナビ
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
