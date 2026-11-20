# Exception Alerts v1.9.1

Generated: 2026-11-20T03:21:40+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 16
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Equity Bancshares, Inc. Class A Common Stock]: SEC 8-K filing
  - New company event detected for Equity Bancshares, Inc. Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [味の素]: 発行登録追補書類（株券､社債券等）
  - New company event detected for 味の素.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: にじさんじ「甘やかし同居ボイス」2026年11月26日(木)18時より発売決定！ - ANYCOLOR株式会社
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ[5032]：自己株券買付状況報告書（法２４条の６第１項に基づくもの） (有価証券報告書) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが示す勤務間インターバル定着の道筋 導入義務化にはなお高いハードル - 日経ビジネス電子版
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI新「INFOBAR」発表 8年ぶり - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ「インフォバー」８年ぶり新モデル…ネットやＳＮＳ非対応、「スマホから距離置きたい人」向け - 読売新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 川崎市、水道管24キロをセンサーで点検 NECの漏水検知技術活用 - 日本経済新聞
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECグループとフルタイムシステム、スマートロッカーとマンション内ロボット宅配を連携させる実証開始 - LOGI-BIZ online
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 【KT App Original】『DEAD OR ALIVE 6 Last Round』DLCコスチューム制作秘話 第8弾(抜粋版) - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『軒轅剣三 雲と山の彼方』コラボ開催を記念し500円分の「えらべるPayⓇ」が当たるプレゼントキャンペーンを開催！ - www.gamecity.ne.jp
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: ライフドリンクカンパニー、上期売上高26％増・営業利益12％増 飲料増産と自動販売機事業の拡大を推進 - みんかぶ
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 三越伊勢丹ホールディングス FY2026 Q2 決算説明会 - BigGo ファイナンス
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングスが自己株買い好感し4日ぶり反発 - 四季報オンライン
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上、上期最終は8％増益で着地 - 株探
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券株式会社 | 導入事例 | 法人のお客さま - ソフトバンク
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクスがストップ高気配､26年9月期15％増益に修正 - 四季報オンライン
  - New company event detected for 浜松ホトニクス.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
