# Exception Alerts v1.9.1

Generated: 2026-10-28T15:29:58+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [NEC]: ＮＥＣ[6701]：2027年3月期 第2四半期（中間期）決算短信〔IFRS〕（連結） 2026年10月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for NEC.
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [ほくほくフィナンシャルグループ]: ほくほくFG（8377）、グループ設立来の最高益を達成 中期経営計画を上方修正、最終年度に純利益650億円を目指す - ログミーFinance
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: (株)ほくほくフィナンシャルグループ【8377】：決算情報 - Yahoo!ファイナンス
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券[8622]：健康優良企業「金の認定」の更新について 2026年10月22日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸、非開示だった上期経常は2.2倍増益へ - 株探
  - New company event detected for 水戸証券.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
