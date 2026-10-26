# Exception Alerts v1.9.1

Generated: 2026-10-26T16:05:48+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 9
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_GUIDANCE [コーエーテクモホールディングス]: コーテクＨＤ、今期経常を21％上方修正、配当も8円増額 - 株探
  - New company event detected for コーエーテクモホールディングス.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: ＦＯＯＤ ＆ ＬＩＦＥ ＣＯＭＰＡＮＩＥＳ（3563）の3か月間の株価はどう動き、高値・安値はどこだった？【2026年5月28日】（LIMO） - Yahoo!ニュース
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [FOOD & LIFE COMPANIES]: FOOD & LIFE COMPANIES､1Q好発進も北京で発生の不安材料 - 四季報オンライン
  - New company event detected for FOOD & LIFE COMPANIES.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: モンゴル保護区火災が中国に拡大 KDDI「社員の車両から発煙」謝罪 釣り疑惑は否定（テレビ朝日系（ANN）） - Yahoo!ニュース
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ほくほくフィナンシャルグループ]: ほくほくフィナンシャルグループとの半導体サプライチェーン強化に関する連携協定の締結について - 西日本新聞me
  - New company event detected for ほくほくフィナンシャルグループ.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: Ｌドリンク - 日本経済新聞
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ライフドリンク カンパニー]: (株)ライフドリンクカンパニー【2585】：決算情報 - Yahoo!ファイナンス
  - New company event detected for ライフドリンク カンパニー.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券 (8622) : 今後の予想・売買予想・AI株価診断 [Mito Securities Co.,] - みんかぶ
  - New company event detected for 水戸証券.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [水戸証券]: 水戸証券[8622]：健康優良企業「金の認定」の更新について 2026年10月22日(適時開示) ：日経会社情報DIGITAL - 日本経済新聞
  - New company event detected for 水戸証券.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
