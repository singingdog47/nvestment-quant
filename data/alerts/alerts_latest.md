# Exception Alerts v1.9.1

Generated: 2026-11-19T03:33:44+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [TORM plc - Class A Common Stock]: SEC 6-K filing
  - New company event detected for TORM plc - Class A Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [WesBanco, Inc. - Common Stock]: SEC 8-K filing
  - New company event detected for WesBanco, Inc. - Common Stock.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ROF-MAO、再始動第1弾楽曲「/SLASH」が本日11/16に配信 デジタルキャンペーンも開始 - PANORA
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: スシロー×可哀想に！第3回コラボ開催！限定コラボイラストで「おぱんちゅうさぎ」「んぽちゃむ」たちが海のなかまに！ - PR TIMES
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: スマホから離れたいニーズ？KDDI「INFOBAR」新機種発表 ネット使えない電話・メッセージだけの“ガラケー”に若者の反応は - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: JAXAの探査機「みお」、22日に水星軌道へ NECなど初挑戦支え - 日本経済新聞
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: レバレッジvs無借金／「20年ぶり」NECの売上高が富士通を逆転の謎 - 月刊FACTA
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: 「こどもまんなか社会」の実現へ ほくほくフィナンシャルグループが道と連携協定（2026年10月29日掲載）｜STV NEWS NNN - 日テレNEWS NNN
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 『信長の野望 覇道』4周年直前生放送 - コーエーテクモゲームス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: 【KT App Original】『DEAD OR ALIVE 6 Last Round』DLCコスチューム制作秘話 第8弾(抜粋版) - www.gamecity.ne.jp
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: ライフドリンクカンパニー[2585]：確認書 (有価証券報告書) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: Ｌドリンク - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 三越伊勢丹ホールディングス FY2026 Q2 決算説明会 - BigGo ファイナンス
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 三越伊勢丹 - 日本経済新聞
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
