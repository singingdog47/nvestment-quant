# Exception Alerts v1.9.1

Generated: 2026-11-03T03:30:30+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 17
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [東京海上ホールディングス]: 東京海上、今期配当を実質増額修正 - 株探
  - New company event detected for 東京海上ホールディングス.
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [KDDI]: KDDI、顧客情報2万人分漏洩か ライフネット生命への不正アクセスで - 日本経済新聞
  - New company event detected for KDDI.
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [KDDI]: KDDI顧客情報漏えいか ライフネットへの不正アクセスで - NHKニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ(株)【5032】：決算説明会書き起こし - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: にじさんじ家長むぎの“なりすまし”で店舗が集客する事案が発生 ANYCOLOR社が対応を報告 - KAI-YOU
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: 【インフォグラフィック】 - ダナンでは10ヶ月間で5,032の新規事業が設立されました。 - Vietnam.vn
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI傘下、社内のAI活用事例113件を無料公開 「Gemini Notebook」で稟議データのチェック支援も - ITmedia
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC川崎 vs 刈谷｜SV.LEAGUE 公式サイト - svleague.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: 株式会社ほくほくフィナンシャルグループと北海道との「こどもまんなか」の推進に係る連携と協力に関する協定 - 北海道のホームページ
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『DOAXVV』 9周年直前！公式ミニ放送「ブイなま！！」 - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『三國志 覇道』11月度公式生放送 #ハドウへの道 - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『DOAXVV』 「オーナーさん大集合！ヴィーナスだらけの9周年メモリアルパーティー！」 - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: マセラティ『グラントゥーリズモ』改良新型、日本限定2台「ローンチエディション」発売…3099万円 - carview!
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 株式会社三越伊勢丹ホールディングスが、クラウドサービスのセキュリティ信用評価「Assuredクラウド評価」を導入 - Assured（アシュアード）
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 伊勢丹創業140周年プロジェクト始動。「WAKU WAKU TO YOU!」を掲げ、次の150年へ - PR TIMES
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス・小池昌洋社長「保険の枠を超えて安心安全を設計」 - 日経BP
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 2026水戸証券チャレンジフェスティバル開催のお知らせ《7/27情報更新》 - 水戸ホーリーホック公式サイト
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス株式会社さま - 中部電力ミライズ
  - New company event detected for 浜松ホトニクス.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
