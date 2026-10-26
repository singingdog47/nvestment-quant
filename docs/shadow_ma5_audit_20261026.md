# 2026-10-26 decision audit: shadow swing / five-session average exit rule

**Status: human review required. No trading-rule changes and NO broker orders.**  
**Information cutoff: 2026-10-23 close JST.**

## I. Operating effectiveness is NOT established

| Cohort | Verified book and outcome | Key limitation |
| --- | --- | --- |
| v1 ¥1m, started 2026-09-10 | One entry: 8622.T BUY 100 at 933 on Sep 15; hard-stop SELL signal Oct 6 filled Oct 15 at 812.187, realized -¥12,081.30 (13.0% of position) | Nine-calendar-day execution delay. No verified automatic AI selection cadence. One completed round trip only. |
| v2 ¥5m, started Oct 15 | 7 dated equity snapshots through Oct 23, all fully in cash, 0 trades | Oct 23 audited 50 Japanese candidates, 0 qualified. Veto counts overlap: unconfirmed trend 34, insufficient turnover 33, weak score/momentum 32, missing point-in-time supply 32, missing price/volume evidence 32, insufficient history 28. Cannot distinguish an effective no-trade policy from poor feature coverage without counterfactual tests. |
| Challenger ¥1m, started Oct 22 | Oct 23 one 3932.T BUY 100 at 1,275.911, one 6750.T pending, NAV ¥997,308.9 | First open position only; 0 closed trades, hence no return evidence. |

### Control-system findings

- GitHub Actions success means the program ran, **not** that it made a trade-quality decision.
- v1 reads a versioned GPT decision JSON. The script is an execution ledger; it does NOT independently generate discretionary judgments. Human/AI decision input timing and freshness need auditing separately.
- Do not compare raw cohort returns without aligning dates and cash/benchmark controls.
- Missing or delayed daily OHLC must remain explicit and must not be fabricated or backfilled into imagined fills.
- No live capital until execution correctness, signal cadence, point-in-time availability, out-of-sample superiority versus cash / broad ETF / simple trend or momentum baseline, and operational alerts are demonstrated.

## II. Five-day moving average (MA5) hypothesis, not the recovered historical formula

The exact earlier user/AI sell-price formula and coefficients could **not** be recovered.  
Test only these **newly proposed, unvalidated proxies**:

- MA5 at close t = mean of closes for t-4 through t.
- `SMA-cross exit`: if close(t) < MA5(t), sell at **next** trading session's open (one-time exit, no reentry).
- `Limit-on-exit`: conditional on an exit decision made after close t when close(t) < MA5(t), set next-session SELL LIMIT = `MA5(t) * k`; if next-session high reaches it, fill at max(next open, limit) for a sell limit. Otherwise cancel at end of that session and force an exit at the **following** session open. Benchmark = sell at immediate next-session open. No fees, slippage or taxes; no synthetic use of same-day close or earlier high to fill.
- k values pretested here: 0.97, 0.98, 1.00; these parameters are NOT adopted.

Public daily OHLC checked: [Yahoo Finance Fujikura history](https://finance.yahoo.co.jp/quote/5803.T/history). Two separate 20-session windows: Jul 13–Aug 10 2026 and Sep 25–Oct 23 2026, each with 5-session warm-up; only decisions where both subsequent opens are visible included.

### Example one-time MA5 cross

| Window | First below-MA5 close | Next open for exit | Final sample close | Exit minus final close, 100 shares |
| --- | --- | ---: | ---: | ---: |
| Jul 13–Aug 10 | Jul 17: close 4,472 versus MA5 4,837 | Jul 21: 4,542 | Aug 10: 5,580 | **-¥103,800**: missing the later rebound (not a realized loss) |
| Sep 25–Oct 23 | Oct 8: close 5,512 versus MA5 5,646.2 | Oct 9: 5,471 | Oct 23: 4,037 | **+¥143,400**: avoided later price decline (not guaranteed repeatability) |

Samples are deliberately different market regimes. Endpoint choice makes the comparisons descriptive, not a generalizable backtest.

### Test of waiting for a MA5-multiple SELL LIMIT

*Units below: compared with selling at the immediately following open, yen per **100 shares**. Multiple decision dates in one continuous interval are overlapping counterfactuals and NOT independent trades.*

| Window; decision opportunities | k=0.97 | k=0.98 | k=1.00 |
| --- | --- | --- | --- |
| Summer; 8 below-MA5 decision dates | limit filled 5/8, mean difference **+¥2,011** | 4/8, **+¥5,514** | 3/8, **+¥1,125** |
| October; 9 below-MA5 decision dates | limit filled 2/9, mean difference **-¥8,502** | 1/9, **-¥12,738** | 0/9, **-¥17,811** |

One severe example: Oct 14 close 5,200, MA5 5,379; next Oct 15 open 4,850. The 0.97 limit near 5,218 never traded on Oct 15 (high 4,858); forced Oct 16 open exit 4,541, **¥30,900 worse** per 100 shares than immediate next-session open.

The October k=1 limit was hit **0/9** times under the specified one-session expiry. The approach encourages waiting for a rebound that may not happen; the short MA5 tends to sit above falling prices. Recent 14-session average true range near Oct 23 was ~¥293/share (~7.3% of price), making fixed 2–3% MA5 offsets especially sensitive to noise and gaps.

### Decision

1. **Do NOT use MA5 × 0.97/0.98/1.00 as an automatic sell-limit recommendation**. No robust improvement is demonstrated; October evidence is adverse.
2. MA5 can be one **review alert**, not a self-sufficient recommendation or hard exit. It did identify the October deterioration, but would also have flagged the July pullback before a strong rebound.
3. Exits must separately assess thesis impairment, liquidity/execution gap risk, market regime, current valuation, position risk and alternatives; then choose execution plan. An exit decision must not depend on *recovering to* the moving average.
4. Before any rule promotion: longer point-in-time sample with multiple securities and regimes, walk-forward/out-of-sample cross-validation, implementation costs, gap/whipsaw analysis and reentry rules, *versus plain next-open exit and a simple volatility-adjusted stop*.
5. The user owns final trade decisions; AI produces explicit recommendations and a contrary case. Existing v1/v2/Challenger ledgers and configured risk thresholds remain unchanged pending review.

**Sources (public)**: GitHub virtual ledgers in `data/shadow_swing`, `data/shadow_swing_v2`, `data/shadow_challenger`; repository `src/shadow_swing.py`, `src/shadow_swing_v2.py`, `src/shadow_challenger.py`, and their corresponding config files. Market prices: Yahoo Finance Japan public historical table. Historical price snippets, small sample and transcribed values require independent reproduction before promotion.
