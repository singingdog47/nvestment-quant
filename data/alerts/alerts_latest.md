# Exception Alerts v1.9.1

Generated: 2026-10-13T15:06:32+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 8
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_BUYBACK [ANYCOLOR]: 決算:ANYCOLOR、最大70億円の自社株買い 5〜7月税引き利益11%減 - 日本経済新聞
  - New company event detected for ANYCOLOR.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Expand Energy Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for Expand Energy Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Expand Energy Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for Expand Energy Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Expand Energy Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for Expand Energy Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Expand Energy Corporation - Common Stock]: SEC 8-K filing
  - New company event detected for Expand Energy Corporation - Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [東京海上ホールディングス]: 自己株券買付状況報告書（法２４条の６第１項に基づくもの）
  - New company event detected for 東京海上ホールディングス.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ(株)【5032】：決算説明会書き起こし - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: にじさんじから「NIJISANJI Replay Mode Type:Ibrahim&Ex Albio」グッズが登場！2026年10月14日(水)19時から販売開始！ - PR TIMES
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: AIキャラ会話サービス「zeta」でにじさんじVTuberを無断生成 ANYCOLOR社が削除要請 - KAI-YOU
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: スタートアップに会いたい！Vol.111-日本郵政 - MUGENLABO Magazine
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 東レ滋賀 vs NEC川崎｜SV.LEAGUE 公式サイト - svleague.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ【6701】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECスペーステクノロジー、第70回宇宙科学技術連合講演会企業展示に出展します - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 10月31日(土) ご来場者プレゼント KUROBEアクアフェアリーズ富山戦 | ニュース - NECレッドロケッツ川崎公式サイト
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: (株)コーエーテクモホールディングス【3635】：決算情報 - Yahoo!ファイナンス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: (株)ライフドリンクカンパニー【2585】：株主優待 - Yahoo!ファイナンス
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: マーケット速報 - 北國新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 2026.10.13 貨物列車（3099列車）秋田駅発車 - YouTube
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 手元資金1.6兆円超なのに「借入金」が急増…それでも信越化学工業の財務は盤石といえるワケ - ダイヤモンド・オンライン
  - New company event detected for 信越化学工業.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
