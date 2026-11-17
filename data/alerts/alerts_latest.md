# Exception Alerts v1.9.1

Generated: 2026-11-17T04:32:21+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 11
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [NEC]: 大阪公立大学、委託先であるNECの個人情報漏えいについて発表、機密性の高い個人情報を削除せず保持 - Yahoo!ニュース
  - New company event detected for NEC.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: NIJISANJI ENから「WANNYANZ」グッズが登場！2026年11月19日(木)11時(JST)から販売開始！ - ANYCOLOR株式会社
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: NIJISANJI ENから「WANNYANZ」グッズが登場！2026年11月19日(木)11時(JST)から販売開始！ - PR TIMES
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: ＦＯＯＤ＆ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ[3563]：中期経営計画「F&LC MTP 27-29－うまいすしを世界へ－」 2026年11月6日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: APN実現に向けたNECの取り組み ～APN製品（WXシリーズ）の特⻑～ : 企業情報 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECと日本IBM、国内初方式のハイブリッド型量子安全通信技術の実証に成功 (2026年11月17日): プレスリリース - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、最大容量を従来比2倍に拡大したテープストレージ「iStorage T560」 - クラウド Watch
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 【決算速報】ライフドリンクＣ---27年3月期2Qは増益、経常利益は3％増(フィスコ) - Yahoo!ファイナンス
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 静岡：浜松ホトニクス 売上高過去最高：地域ニュース - 読売新聞
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：決算情報 - Yahoo!ファイナンス
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
