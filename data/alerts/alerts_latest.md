# Exception Alerts v1.9.1

Generated: 2026-11-03T15:13:38+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 5
- WATCH: 14
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [信越化学工業]: 信越化学工業[4063]：2027年３月期 第２四半期（中間期）決算短信〔日本基準〕（連結） 2026年10月27日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ◎〔決算〕ほくほくＦＧ、連結純利益４２０億円に上方修正 - 時事通信ニュース
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ほくほくフィナンシャルグループ[8377]：業績予想および配当予想の修正に関するお知らせ 2026年11月2日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** COMPANY_EVENT/EVENT_REGULATORY [KDDI]: KDDI、2万2541件の顧客情報漏えいか ライフネット生命への不正アクセスで（アスキー） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: ＡＮＹＣＯＬＯＲ、「にじさんじ」が韓国の大型イベントに出展 - https://kabu-ir.com/
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: お仕事手帖 翻訳業務編 多彩な表現で“生きたニュアンス”を世界へ届ける - ANYCOLOR MAGAZINE
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 国内初、850MHz帯Wi-Fi HaLowを活用したロボットトラクターの無線遠隔監視・制御の実証に成功 ～自動運転の運用範囲拡大による農作業の自動化・省力化を推進 - NECネッツエスアイ
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 東地区首位・富山がNEC川崎に連勝、西地区首位のSAGA久光は開幕6連勝。SVリーグ女子第3節の結果 - J SPORTSコラム＆ニュース
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: ライフドリンクカンパニー株価ストップ高 営業益の高進捗評価 - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: Ｌドリンク - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: マーケット速報 - 北國新聞
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: マセラティ『グラントゥーリズモ』改良新型、日本限定2台「ローンチエディション」発売…3099万円 - レスポンス（Response.jp）
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 株式会社三越伊勢丹ホールディングス 会社説明会【IR広告】 - トウシル
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス(株)【6965】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 宇宙の謎に挑む琥珀色 浜松ホトニクス豊岡製作所玄関の光電子増倍管 ハイパーカミオカンデで期待：ニュース - 中日BIZナビ
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 「人類の未知未踏追求に貢献していく」 ノーベル物理学賞、重要機器製造の浜松ホトニクス - 産経ニュース
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.
- **WATCH** VOLATILITY/VIX_WATCH: VIX requires monitoring
  - VIX exceeded the watch threshold.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
