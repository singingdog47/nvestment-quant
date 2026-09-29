# Exception Alerts v1.9.1

Generated: 2026-09-29T14:07:21+00:00
Highest severity: **WARNING**

## Counts
- CRITICAL: 0
- WARNING: 4
- WATCH: 12
- INFO: 0

## Alerts
- **WARNING** COMPANY_EVENT/EVENT_FILING [Hercules Capital, Inc. Common Stock]: SEC 8-K filing
  - New company event detected for Hercules Capital, Inc. Common Stock.
- **WARNING** COMPANY_EVENT/EVENT_FILING [NEC]: 変更報告書
  - New company event detected for NEC.
- **WARNING** LIQUIDITY/THIN_LIQUIDITY: Thin liquidity flag active
  - Market Regime Engine reports thin_liquidity_flag=true.
- **WARNING** VOLATILITY/TREASURY_VOLATILITY_SHOCK: Treasury yield volatility is unusually high
  - The official-Treasury realized-yield-volatility proxy is at or above its 90th percentile. It is not ICE MOVE.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: 楽天モバイル、携帯「独り立ち」へ正念場 ＫＤＤＩの回線貸し出し縮小―基地局整備、ライバルに遅れ - 時事ドットコム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: AI時代の企業ネットワーク基盤となる「AccelWaves」構想を始動 - KDDI ニュースルーム
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDIが提供する「SASEゲートウェイ」： SP Interconnect がクローズドネットワークのゼロトラスト化をシンプルに実現 - Palo Alto Networks
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: ダイヤモンド・オンラインで、KDDIの広告運用インハウス化7年の取り組みに関する記事が掲載されました - supership.jp
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [KDDI]: KDDI、米パロアルトと提携 セキュリティー新サービス提供 - 日本経済新聞
  - New company event detected for KDDI.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: ＣＥＨＤについて、ＮＥＣは保有割合が増加したと報告 [変更報告書No.2] - 株探
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NECと川崎市の共催による『かわさきSDGsパートナーまつり2026』を開催 - PR TIMES
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [NEC]: NEC川崎の10/30ホームゲームにお笑い芸人ミカボの出演が決定！ - バレーボールキング
  - New company event detected for NEC.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス、先端半導体の動作解析向け顕微鏡 AIチップに対応 - 日本経済新聞
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 浜松ホトニクス、先進半導体の故障解析向け「ｉＰＨＥＭＯＳ－ＤＤＸ」開発、７手法を１台に統合 - kabu-ir.com
  - New company event detected for 浜松ホトニクス.
- **WATCH** COMPANY_EVENT/EVENT_DISCLOSURE [浜松ホトニクス]: 先進半導体パッケージの故障解析に対応した倒立型エミッション顕微鏡「iPHEMOS®-DDX」を発売 - PR TIMES
  - New company event detected for 浜松ホトニクス.
- **WATCH** LIQUIDITY/LIQUIDITY_SOFT: Market liquidity is soft
  - Liquidity component fell below 40/100.

## Governance
- Alerts are deterministic exception flags, not buy/sell signals.
- Missing values are never inferred.
- Only public-safe market/company data may be persisted by this module.
