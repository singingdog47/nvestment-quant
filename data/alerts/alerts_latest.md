# Exception Alerts v1.9.1

Generated: 2026-10-26T15:09:36+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 4
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [信越化学工業]: 信越化学工業[4063]：2026年３月期決算短信〔日本基準〕（連結） 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 信越化学工業.
- **WARNING** LIQUIDITY/LIQUIDITY_WEAK: Market liquidity is weak
  - Liquidity component fell below 25/100.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: モンゴルの自然保護区を焼失させたKDDI子会社 地元メディアの反応は（クーリエ・ジャポン） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: モンゴルで大規模な草原火災 KDDI現地子会社の車から出火か - 朝日新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業、東京エレクトロン…エヌビディア、サムスンが熱視線を送る日本企業の基盤技術 - JBpress
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 信越化学工業株価が続伸 樹脂製品値上げ - 日本経済新聞
  - New company event detected for 信越化学工業.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
