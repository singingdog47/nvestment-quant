# 決算・開示レビューゲート（最小構成）

## 目的
決算・業績修正・配当変更の確認漏れを、確認済みと偽らず人間に提示する。自動売買は行わない。

## 最小運用
1. 保有銘柄コードのCSVと、確認できた一次資料（発行体IR・JPX）の記録を**非公開**で管理する。
2. `python -m src.decision_event_review_bridge --symbols PRIVATE.csv --manifest PRIVATE_MANIFEST.json --as-of-utc 2026-11-09T00:15:00Z --output PRIVATE_REVIEW.json` を実行する。未確認の銘柄はmanifestに入れなくてよい。
3. `AWAITING_USER_CONFIRMATION` なら未確認銘柄を明示し、「今回だけ暫定分析を続けるか」を本人に確認する。
4. 承認時も未検証フラグを残し、自動注文は禁止する。承認はレビュー単位のfingerprintに紐付け、再利用しない。
5. `src.private_runtime_readiness.assess_sources` が非公開の正規化済み楽天保有CSVから日本株4桁コードを抽出し、同一の決算ゲートを実行する。結果は `.private/readiness/event_review_latest.json` に権限600で保存する。一次資料記録は `.private/readiness/event_disclosures_verified.json` に任意で設置し、なければ全件未確認とする。承認は `.private/readiness/event_review_consent.json` にレビュー固有のfingerprintで保存する。\n6. この結果はprivate readinessの報告に含むが、既存の売買提案を自動的に許可・変更するものではない。売買判断を生成する下流処理のゲート連動は別途検証が必要。

## 意図的に実装しないもの
- 有料TDnet API
- 不安定な非公式Atom/RSS自動取得
- 全銘柄の決算発表の網羅性保証
- 公開Actionsへの私有PFアップロード
- 実売買の自動実行

## 統合条件
CI成功、合成楽天保有データによるprivate readiness接続テスト、非公開データ保護、未確認時の本人確認の受け渡しを確認する。実Google Drive保有データを使った実行と、下流の売買判断へのゲート強制は別途確認する。
