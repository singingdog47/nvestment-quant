# Exception Alerts v1.9.1

Generated: 2026-10-15T00:34:23+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 10
- INFO: 0

## Alerts
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: 【にじさんじ ANYCOLOR社 が削除要請】AIキャラ会話サービス「zeta」でにじさんじVTuberを無断生成【zeta（ゼタ）】 - YouTube
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ、韓国ＬＧグループ傘下ＩＴ企業と協業へ…「ＡＩエージェント」やロボット管理などサービス提供 - 読売新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、広島で再生プラの動静脈データ連携実証を開始。情報流通基盤「PLA-NETJ」でトレーサビリティ確保を支援 - Circular Economy Hub
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: アンソロピックがNEC・日立・富士通らと組む理由。「何十年もやりきれなかった」システム刷新への期待 - Business Insider Japan
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: マーケット速報 - 佐賀新聞
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: (株)コーエーテクモホールディングス【3635】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 2026.10.13 貨物列車（3099列車）秋田駅発車 - YouTube
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 先端半導体の後工程向け…浜松ホトニクス、故障解析装置の機能 - ニュースイッチ by 日刊工業新聞社
  - New company event detected for 浜松ホトニクス.
- **WATCH** REGIME/REGIME_CHANGE: Market regime changed
  - Market regime changed from CONSTRUCTIVE to NEUTRAL.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
