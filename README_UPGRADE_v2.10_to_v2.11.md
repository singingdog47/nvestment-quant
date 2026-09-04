# v2.10 → v2.11

## PayPayポイント運用・数か月スイング監視を追加

### 目的
PayPayポイント運用を短期回転ではなく数か月単位で比較し、手数料負けを避けながら「金 / テクノロジー / スタンダード / BTC / WAIT」を検討するための補助レイヤーを追加しました。

### 追加内容
- `config/paypay_swing_v1.json`
  - Momentum 35% / Macro 25% / Trend 20% / Risk 10% / Cost 10%
  - BTCは往復スプレッド負担を考慮し、通常コースより高い確認閾値を設定
- `src/paypay_swing.py`
  - GLD / QQQ / SPY / BTC-USD と米10年金利・DXY・VIXを用いた相対スコア
  - 日次監視と週次レビュー用の出力
  - WAITを常に有効な選択肢として維持
  - 自動発注は行わない
- `src/run_paypay_swing.py`
  - 日次パイプラインから実行
  - モバイルブリーフと統合レポートへ簡潔なPayPay Swing欄を挿入
- `tests/test_paypay_swing.py`
  - 通常コース1%と暗号資産コース約4.5%×往復のコスト計算を検証

### 出力
- `data/paypay_swing/paypay_swing_latest.json`
- `data/paypay_swing/paypay_swing_daily_latest.md`
- `data/paypay_swing/paypay_swing_weekly_latest.md`
- `data/paypay_swing/history.csv`

### データ上の注意
- PayPayポイント運用のコース価格は参照ETF・暗号資産価格と完全一致しません。
- yfinanceは二次データです。実際の切り替え前にはPayPay画面の提示条件と一次情報を確認します。
- 暗号資産コースのスプレッド相当は市況で変動するため、4.5%は固定値ではなく通常時の概算です。

### 運用思想
日次ではノイズを拾いすぎないよう監視に限定し、数か月スイングの正式な再評価は週次を中心に行います。スコア首位でも閾値や優位差が不足する場合はWAITとします。
