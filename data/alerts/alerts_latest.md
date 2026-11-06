# Exception Alerts v1.9.1

Generated: 2026-11-06T02:29:54+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 10
- WATCH: 12
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [ANYCOLOR]: 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞
  - New company event detected for ANYCOLOR.
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [東京海上ホールディングス]: 東京海上ホールディングス[8766]：自己株式の取得状況に関するお知らせ 2026年11月6日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 東京海上ホールディングス.
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [東京海上ホールディングス]: 東京海上HD(8766)、7期連続の「増配」を発表し、配当利回り3.1％に！ 年間配当は7年で3.2倍に増加、2027年3月期は前期比27円増の｢1株あたり245円｣に - ダイヤモンド・オンライン
  - New company event detected for 東京海上ホールディングス.
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [Carter Bankshares, Inc. - Common Stock]: SEC 10-Q filing
  - New company event detected for Carter Bankshares, Inc. - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [First Busey Corporation - Common Stock]: SEC 10-Q filing
  - New company event detected for First Busey Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [ZERIA PHARMACEUTICAL CO.,LTD.]: 半期報告書－第73期(2026/04/01－2027/03/31)
  - New company event detected for ZERIA PHARMACEUTICAL CO.,LTD..
- **WARNING** COMPANY_EVENT/EVENT_FILING [ZERIA PHARMACEUTICAL CO.,LTD.]: 確認書
  - New company event detected for ZERIA PHARMACEUTICAL CO.,LTD..
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [KDDI]: 「au自転車サポート」で顧客情報漏えいの可能性、委託先に不正アクセス（ケータイ Watch） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [KDDI]: KDDI「au自転車サポート」で顧客情報漏えいの可能性 委託先 プレステージ・コアソリューションに不正アクセス、対象件数は調査中|セキュリティニュースのセキュリティ対策Lab - 合同会社ロケットボーイズ
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: 全国初のシロアマダイ陸上養殖化へ F&LC、山口県、安藤建設などによるコンソーシアムを設立、共同研究を開始 - PR TIMES
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ（Ｆ＆ＬＣ）【3563】｜開示情報｜株探（かぶたん） - 株探
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ドコモ社長、5G基地局がKDDIやソフトバンクより少ない理由を説明 - CNET Japan
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ギークプラス 日通NECロジが棚搬送型ロボ導入 | ロジスティクス | ニュース - Daily Cargo電子版
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 異形の「防衛企業」NECが磨くデュアルユース 勝ち筋はセキュリティー - 日経クロステック Active
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 【バレー】NEC川崎・シルビア・チネロ・ヌワカロール「セットの終盤で自分たちで決めて終わらせるところで決めきれなかった」 SV女子会見（バレーボールマガジン） - Yahoo!ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: ほくほくフィナンシャルグループが株式10分割 優待制度も見直し - 日本経済新聞
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: (株)ほくほくフィナンシャルグループ【8377】：決算情報 - Yahoo!ファイナンス
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: Ｌドリンク - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [KDDI]: KDDIアイレット、社内のAI活用事例113件を無料公開 営業・人事など50件、プロンプトや時短の工夫も紹介 - Ledge.ai
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_MANAGEMENT [水戸証券]: 水戸証券[8622]：人事異動のお知らせ 2026年10月13日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
