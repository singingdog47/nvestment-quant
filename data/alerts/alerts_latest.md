# Exception Alerts v1.9.1

Generated: 2026-10-01T15:26:13+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 1
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 楽天モバイル、携帯「独り立ち」へ正念場 ＫＤＤＩの回線貸し出し縮小―基地局整備、ライバルに遅れ - 時事ドットコム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 「Xperia 10 VIII」をauから10月8日に発売 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 半導体部品の故障を高い精度で特定 浜松ホトニクス、解析装置の受注開始：ニュース - 中日BIZナビ
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
