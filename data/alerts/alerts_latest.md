# Exception Alerts v1.9

Generated: 2026-08-23T13:16:45+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 7
- INFO: 0

## Alerts
- **WARNING** DATA_QUALITY/NOT_ACTIONABLE: Data quality blocks investment conclusions
  - Data quality is not actionable; missing data must not be converted into buy/sell conclusions.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ(株)【9433】：掲示板 - Yahoo!ファイナンス
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＮＥＣ【6701】：掲示板 - Yahoo!ファイナンス
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC、大学・学術機関や研究機関での次世代AI・HPC環境構築支援に向けCornelisと協業拡大 - EnterpriseZine
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECとNECソリューションイノベータの社員7名が2026 OCI Top Partner Engineersに認定 - PR TIMES
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：掲示板 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業(株)【4063】：今の株価の理由は？値動きの背景をAIが解説 - Yahoo!ファイナンス
  - New company event detected for 信越化学工業.
- **WATCH** SCREENING/RANK_JUMP [Arbutus Biopharma Corporation - Common Stock]: Screening rank jumped
  - Arbutus Biopharma Corporation - Common Stock improved by at least 15 ranks.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
