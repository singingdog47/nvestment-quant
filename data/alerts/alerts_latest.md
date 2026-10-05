# Exception Alerts v1.9.1

Generated: 2026-10-05T17:26:40+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 2
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [ほくほくフィナンシャルグループ]: ほくほくフィナンシャルグループ[8377]：2027年3月期 第1四半期決算短信〔日本基準〕（連結） 2026年7月29日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for ほくほくフィナンシャルグループ.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: ほくほくフィナンシャルグループ (8377) : 今後の予想・売買予想・AI株価診断 [HFG] - みんかぶ
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
