# Exception Alerts v1.9.1

Generated: 2026-10-27T15:19:36+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 6
- WATCH: 12
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [水戸証券]: 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Hercules Capital, Inc. Common Stock]: SEC 8-K filing
  - New company event detected for Hercules Capital, Inc. Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [Hercules Capital, Inc. Common Stock]: SEC 8-K filing
  - New company event detected for Hercules Capital, Inc. Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: 証券各社レーティング（目標株価変更）：SHIFT、ANYCOLORなど4社(フィスコ) - Yahoo!ファイナンス
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ－岩井コスモが目標株価引き下げ 再評価されるまで少し時間かかる - TradingView
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: FOOD & LIFE COMPANIES､1Q好発進も北京で発生の不安材料 - 四季報オンライン
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIとELYZA、AIロボットの新会社設立 300億円投資、2030年度までに1000台導入へ - CNET Japan
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: VLMでライブカメラ映像から現場状況をスコア化し、災害予兆を早期に発見できるAIを新たに開発 - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業、東京エレクトロン…エヌビディア、サムスンが熱視線を送る日本企業の基盤技術 - JBpress
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: 東京海上ホールディングス フィジカルAI搭載ロボの保険開始 - ABEMA
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [東京海上ホールディングス]: マーケット速報 - 山陽新聞
  - New company event detected for 東京海上ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券株式会社 | 導入事例 | 法人のお客さま | ソフトバンク - ソフトバンク
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 【アナリスト予想】浜松ホトニクス、26年9月期経常予想。対前週4%上昇。(アイフィス株予報) - Yahoo!ファイナンス
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
