# Exception Alerts v1.9.1

Generated: 2026-10-26T15:30:31+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 5
- WATCH: 4
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: キヤノン、信越化学工業も…「下落が怖い」人向け"高配当"半導体・AI株7銘柄の実名 - 現代ビジネス
  - New company event detected for 信越化学工業.
- **WARNING** COMPANY_EVENT/EVENT_EARNINGS [水戸証券]: 水戸証券[8622]：2026年３月期決算短信〔日本基準〕(非連結) 2026年4月28日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WARNING** LIQUIDITY/LIQUIDITY_WEAK: Market liquidity is weak
  - Liquidity component fell below 25/100.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: ほくほくＦＧ、今期経常は10％増で2期連続最高益、40円増配へ - 株探
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: 500mlボトルが約50円。低価格でも“増収増益”の成長を続けるライフドリンク カンパニーが重要視する3つの戦略 - ネットショップ担当者フォーラム
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [信越化学工業]: 創業100周年の信越化学工業 上越市と新潟県に計1億円寄付 - 上越妙高タウン情報
  - New company event detected for 信越化学工業.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券株式会社 | 導入事例 | 法人のお客さま | ソフトバンク - ソフトバンク
  - New company event detected for 水戸証券.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
