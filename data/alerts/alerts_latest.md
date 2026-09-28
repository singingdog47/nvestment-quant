# Exception Alerts v1.9.1

Generated: 2026-09-28T16:45:11+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 2
- WATCH: 3
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_MNA [KDDI]: 買収・争奪戦になっているカカクコム、ＫＤＤＩとの資本提携を解消…業務提携は継続 - 読売新聞
  - New company event detected for KDDI.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 日本郵便とKDDI、ドローン社会基盤化へ基本合意書を締結し、郵便局をドローンポート拠点とする実証を開始 - newsroom.kddi.com
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: サイバー攻撃のリスクから事業継続を考える - NEC
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECよどこへ行く 森田改革の成否 - 日経クロステック
  - New company event detected for NEC.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
