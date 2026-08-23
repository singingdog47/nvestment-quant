# Exception Alerts v1.9

Generated: 2026-08-23T22:28:38+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 5
- INFO: 0

## Alerts
- **WARNING** DATA_QUALITY/NOT_ACTIONABLE: Data quality blocks investment conclusions
  - Data quality is not actionable; missing data must not be converted into buy/sell conclusions.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ(株)【9433】：株価・株式情報（夜間PTS含む） - Yahoo!ファイナンス
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIからの独り立ちを目指す楽天モバイル、ローミング交渉の現在地――両社の考えを整理 - ITmedia Mobile - ITmedia
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ【6701】：株価・株式情報（夜間PTS含む） - Yahoo!ファイナンス
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: 【無料公開】《スクープ》三菱電機、日立、NEC、オムロンなどが主導したIoTプラットフォーム「エッジクロスコンソーシアム」が終了へ！ - ダイヤモンド・オンライン
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：株価・株式情報（夜間PTS含む） - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
