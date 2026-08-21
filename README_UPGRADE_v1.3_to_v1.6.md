# investment-quant v1.3 → v1.6 差分アップグレード

このパッケージは、現在稼働中の **v1.3 Daily Quant Screen** を壊さずに、
**Market Regime Engine v1.5 + Company Intelligence v1.6** を追加するための差分です。

## v1.3で保持するもの

現在のv1.3で既に稼働している以下は変更しません。

- `Daily Quant Screen`
- `max_tickers=0` による全銘柄処理
- `data/screening_latest.csv`
- `data/screening_full.csv.gz`
- `data/quality_report.json`
- `data/daily_report.md`
- 日本/米国 上位50+50
- 金融・海運の過度な集中を抑える上限
- AGNC等のモーゲージREITを監視扱いにする除外
- 上位20のセクター集中表示
- rank差分
- 注文前チェック
- 推測した決算日を使わない安全ルール
- 平日16:17 JSTの既存スケジュール

既存の `src/` のv1.3ファイル、既存workflow、`requirements.txt` は上書きしません。

## v1.6で追加するもの

### Market Regime Engine v1.5

- 日経225 / TOPIX ETF proxy / S&P500 / NASDAQ
- VIX
- USDJPY
- 米10年金利
- 金 / WTI / 銅
- TLT / HYG / LQD
- FRED: HY OAS / IG OAS / NFCI / Fed Funds
- v1.3全銘柄結果からBreadthを可能な範囲で計算
- JPX投資部門別 / 空売り / 信用の公式ページをbest-effort取得
- CFTC COTをbest-effort取得
- Trend / Stress / Participation / Liquidity / Positioning の5軸
- `RISK_ON / CONSTRUCTIVE / NEUTRAL / DEFENSIVE / RISK_OFF`
- 欠損時は利用可能な軸だけで再ウェイトし、confidenceを明示

### Company Intelligence v1.6

- TDnet: 決算、業績修正、配当、自社株買い、M&A、増資等
- EDINET
- SEC EDGAR
- 会社IRページ変更監視（任意）
- Google News RSSは「発見専用」secondary source
- 公式財務欠損時のみyfinanceをsecondary fallback
- source / event_date / fetched_at / data_status / source_tier を保持
- データ品質不足なら `actionable=false`
- Market Regime + 企業イベント + v1.3 screeningを `ai_context_latest.md` に統合

## 重要なプライバシー設計

v1.3の「公開スクリーニングと非公開ポートフォリオを分離」を維持します。

- v1.6はデフォルトで `config/portfolio.csv` を読みません。
- 保有株数、取得単価、現金残高をGitHubへ置かないでください。
- GitHub側のCompany Intelligenceは、`config/intelligence_watchlist.csv` とv1.3上位候補を監視します。
- 非公開ポートフォリオは従来どおりGoogle Drive側の楽天証券データとChatGPT/Geminiで結合します。
- private repoで明示的に使いたい場合だけ `ALLOW_REPO_PORTFOLIO=1` を設定できます。

## 導入手順

1. 現在のv1.3リポジトリをZIP等でバックアップ。
2. このパッケージの**中身をリポジトリ直下へ追加**。
3. 既存ファイルの削除・置換はしない。
4. `Actions → Investment Intelligence v1.6 → Run workflow` を1回実行。
5. 以下が生成されれば成功。

```text
data/regime/market_regime_latest.json
data/regime/market_source_health_latest.csv
data/intelligence/company_events_latest.csv
data/intelligence/data_quality_latest.json
data/intelligence/ai_context_latest.md
data/intelligence/system_health_latest.json
```

## スケジュール

既存v1.3:
- 16:17 JST: Daily Quant Screen

追加v1.6:
- 07:15 JST: 朝のRegime + Company Intelligence
- 16:30 JST: v1.3スクリーニング後のRegime + Company Intelligence

16:30側は、Market Regime → Company Intelligenceの順に**同じworkflow内で連続実行**するため、別workflow間のrace conditionを避けます。

## 新しい必須有料サービス

ありません。

使うものは無料公開データとGitHub Actionsです。EDINET/SEC用の既存secretが無ければ、そのソースだけ `missing` になります。取得不能を推測で埋めません。

## 新規ファイルだけを追加する理由

v1.3は既に9,000銘柄超の全市場スクリーニングを安定して処理しているため、コアを作り替えるメリットより障害リスクの方が大きいからです。

v1.6は **スクリーナーを置換する版ではなく、事実確認と市場環境認識を追加する版** です。
