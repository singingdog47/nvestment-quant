# Exception Alerts v1.9.1

Generated: 2026-11-18T03:44:35+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 20
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [ANYCOLOR]: 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞
  - New company event detected for ANYCOLOR.
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [信越化学工業]: 信越化学工業[4063]：自己株式取得に係る事項の決定に関するお知らせ 2026年11月13日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ(株)【5032】：決算説明会書き起こし - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ROF-MAOインタビュー 新たな形でまた歩み出す、彼らの「前進宣言」 - ANYCOLOR MAGAZINE
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: NIJISANJI EN アルバーン・ノックス、サニー・ブリスコーの「WANNYANZ」グッズが登場 11/19 11時から販売開始 - PANORA
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: にじさんじから「にじたうん もけもけますこっと に」が登場！2026年11月18日(水)19時から販売開始！ - PR TIMES
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ（3563）の3か月間の株価はどう動き、高値・安値はどこだった？【2026年5月28日】（LIMO） - Yahoo!ニュース
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: 京樽を5年で売却した「スシロー」主力事業に集中し売上収益1兆円超の達成を3～4年前倒し - au Webポータル
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: FOOD＆LIFE（3563）FY2026 月次情報 (8月期) - 四季報オンライン
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 「INFOBAR ZERO」をau Flex Styleから12月25日に発売 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、通話・SMSなどシンプルな機能に特化した携帯電話「INFOBAR ZERO」発売へ - ビジネスネットワーク
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、シンプル携帯「INFOBAR ZERO」発表！ 12月25日発売 - GAME Watch
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、「INFOBAR ZERO」発売 初代デザイン継承、ネット非対応で3万2780円 - ASCII.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: IT／ネットワーク統合ソリューション「UNIVERGE」特集 : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 地上デジタル放送特集 : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: Vol.58 No.5（2005年9月） – ユビキタス環境を活用し，企業競争力を向上させる「UNIVERGE」特集 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC跡地に複合施設 JR一ノ関駅東口 一関市が土地利用のイメージ示す - 岩手日報
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: JPモルガン・アセット・マネジメント株式会社とJPモルガン証券株式会社他1者が株式会社ライフドリンク　カンパニー＜2585＞株式の変更報告書を提出 - ｄメニューニュース
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 三越伊勢丹ホールディングス FY2026 Q2 決算説明会 - BigGo ファイナンス
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業[4063]：半期報告書－第150期(2026/04/01－2027/03/31) (有価証券報告書) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 【アナリスト評価】信越化学工業、レーティング強気を継続、目標株価8,300円に引上げ（米系大手証券）(アイフィス株予報) - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
