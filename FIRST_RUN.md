# First Run — 最短手順

1. v1.3リポジトリをバックアップ。
2. ZIP内のファイルをリポジトリ直下に追加してcommit/push。
3. GitHub → Actions → `Investment Intelligence v1.6` → `Run workflow`。
4. 成功後に以下を確認。
   - `data/regime/market_regime_latest.json`
   - `data/intelligence/ai_context_latest.md`
   - `data/intelligence/source_health_latest.csv`
5. `EDINET_API_KEY` が未登録なら、EDINETだけ `missing` になります。システム全体は停止しません。
6. `SEC_USER_AGENT` が未登録なら、SECだけ `missing` になります。
7. 翌営業日に既存v1.3 `Daily Quant Screen` が16:17 JST、その後v1.6が16:30 JSTに動くことを確認。

## 成功条件

- v1.3の既存成果物が消えていない
- v1.3 workflowが従来どおり成功
- Market Regimeの `confidence` が表示される
- 取得失敗ソースが `missing/error` として明示される
- `ai_context_latest.md` に「推測で埋めない」ルールが入る

## 重要

この環境では外部Webへの実通信テストができないため、TDnet/JPX/FRED/CFTC等のライブ疎通は最初のGitHub Actions手動実行で確認してください。構文・互換アダプター・スコアリングのローカルテストはパッケージ作成時に実施済みです。
