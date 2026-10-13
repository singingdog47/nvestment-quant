# Exception Alerts v1.9.1

Generated: 2026-10-13T03:05:23+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 3
- WATCH: 11
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_DIVIDEND [信越化学工業]: キヤノン、信越化学工業も…「下落が怖い」人向け"高配当"半導体・AI株7銘柄の実名 - 現代ビジネス
  - New company event detected for 信越化学工業.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: にじさんじ「ハロウィンゾンビボイス」2026年10月15日(木)17時より発売決定！ - PR TIMES
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: すぷれあ“先生”対談 「かわいいに全力」なアイドルたちの素顔 - ANYCOLOR MAGAZINE
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [ANYCOLOR]: AIキャラ会話サービス「zeta」でにじさんじVTuberを無断生成 ANYCOLORが削除要請 - KAI-YOU
  - New company event detected for ANYCOLOR.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI金融子会社がナッジと提携 若年層カード発行で - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが日本郵便と連携し、ドローンポートの郵便局に！設置されると何がどうなる？ - @DIME アットダイム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ＫＤＤＩ ａｕ Ｓｔａｒｌｉｎｋ ＳｔａｔｉｏｎをＮＥＴＩＳ登録 - 建通新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: A山形 vs NEC川崎｜SV.LEAGUE 公式サイト - svleague.jp
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [コーエーテクモホールディングス]: PRODUCT（3635ページ目） - Gizmodo
  - New company event detected for コーエーテクモホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [三越伊勢丹ホールディングス]: 日本橋三越本店で「大中央区展」を開催！中央区の食と技がつながるコラボに出会える1週間。10月21日(水)から - PR TIMES
  - New company event detected for 三越伊勢丹ホールディングス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: ノーベル賞受賞貢献は3度目「当たり前のようにやってきたことが大きなことになり非常に誇り」 研究支えた浜松ホトニクスの技術＝静岡 - TBS NEWS DIG
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
