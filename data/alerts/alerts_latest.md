# Exception Alerts v1.9.1

Generated: 2026-10-14T12:55:18+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 6
- WATCH: 13
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [水戸証券]: 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WARNING** COMPANY_EVENT/EVENT_FILING [ACNB Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for ACNB Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [FinTech Global Incorporated]: 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
  - New company event detected for FinTech Global Incorporated.
- **WARNING** COMPANY_EVENT/EVENT_FILING [メディアドゥ]: 半期報告書－第28期(2026/03/01－2027/02/28)
  - New company event detected for メディアドゥ.
- **WARNING** COMPANY_EVENT/EVENT_FILING [メディアドゥ]: 確認書
  - New company event detected for メディアドゥ.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: 『労働新聞』最新号（3563号）を労働新聞電子版に掲載しました。｜お知らせ - 労働新聞社
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが韓国LG CNSと基本合意書、AI・スマートシティなどAPACの4分野で協業を検討へ - ビジネス+IT
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 【11/12・13開催】法人向けメッセージ配信サービス KDDI Message Cast、「コールセンター/CRM デモ&コンファレンス 2026 in 東京」に出展・登壇 〜Salesforceと共同登壇し、AI×RCSで入電を減らす顧客対応をライブデモで紹介 - supership.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIと韓国のLG CNS、AIやスマートシティなど4領域で協業 APACでの事業拡大へ - ビジネスネットワーク
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: (株)コーエーテクモホールディングス【3635】：決算情報 - Yahoo!ファイナンス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 空き店舗活用支援事業補助金のご案内 - 木更津市
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 「安さのその先へ」──ライフドリンク カンパニーの成長を支える「脱付加価値戦略」とは - ECのミカタ
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: (株)三越伊勢丹ホールディングス【3099】：板気配 - Yahoo!ファイナンス
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 銀座三越で『ラヴィット！』初のグルメイベント「ラヴィット！グルメフェスティバル」を開催 - PR TIMES
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: M2X、東京海上ホールディングスと業務提携…製造業の設備保全DXを共同推進 - レスポンス（Response.jp）
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 13：15ごろ～☎水戸証券・野坂晃一さん補足資料｜マーケット・テラス｜マネー・投資 - ラジオNIKKEI
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: ノーベル賞受賞貢献は3度目「当たり前のようにやってきたことが大きなことになり非常に誇り」 研究支えた浜松ホトニクスの技術＝静岡 | 静岡のニュース | SBSNEWS | 静岡放送 (1ページ) - TBS NEWS DIG
  - New company event detected for 浜松ホトニクス.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
