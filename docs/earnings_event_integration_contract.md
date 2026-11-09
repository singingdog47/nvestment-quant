# 決算・開示チェックの本番接続契約（統合前）

## 目的
株価変動の理由を断定する前に決算・業績修正・配当変更を確認する。無料情報は候補であり、網羅性・正確性を保証しない。

## 処理順
1. 非公開の銘柄コードCSVをローカル/非公開ランナーで読み込む。公開GitHubやActionsログへ保有一覧・残高・注文を出さない。
2. `python -m src.run_free_disclosure_preflight --symbols PRIVATE.csv --output PRIVATE_CANDIDATES.json` で候補収集。失敗は UNKNOWN。
3. 重要な候補は公式の企業IR等で確認し、検証済みmanifestを非公開で作成する。候補が0件でも「開示なし」と断定しない。
4. `python -m src.decision_event_review_bridge --symbols PRIVATE.csv --manifest PRIVATE_MANIFEST.json --as-of-utc 2026-11-09T00:15:00Z --output PRIVATE_REVIEW.json`。
5. `analysis_mode=AWAITING_USER_CONFIRMATION` の場合、未確認銘柄とリスクを表示し、本人に今回だけ続行するか尋ねる。本人の回答がない限り暫定売買推奨を確定しない。
6. 許可後も `may_execute_orders=false`。本人が証券会社で判断・注文する。

## 接続上の制約
- このPRは既存の本番ポートフォリオ処理へフックしていない。CLIとJSON契約のみ。
- ChatGPTの対話確認は外部プログラムから直接発火しない。ホスト側で `user_confirmation.question_ja` を表示し、明示的回答を当該レビューに戻す必要がある。
- 実API疎通・実保有データのE2E・開示ソースの利用規約確認は未完了。
- GitHub Actionsのモックテスト成功は実通信や情報網羅性の証明ではない。
- 有料J-Quantsアダプターは任意であり、無料運用では利用しない。

## 統合判定
専用CIとPR CIが成功、無料候補取得の実通信が成功、私有データを漏洩させないE2E、明示的同意のUI接続、実際の決算発表の照合が揃うまではマージしない。

## 2026-11-09 実通信監査
GitHub Actions run 42542230275 の実通信プローブは `FREE_FEED_UNAVAILABLE RuntimeError Unexpected feed format; fail closed` を記録。HTTP応答をAtomとして解釈できなかった。実通信成功とは認めない。従来の `continue-on-error: true` によりCIが緑になったことは誤解を招くため撤去した。無料候補フィードの代替を検証し、一次ソース照合を実装するまで本番統合不可。
