from __future__ import annotations
from pathlib import Path
import json
from .integration import read_v1_3_daily_report


def build_brief(targets, events, health, quality, snapshot, market_regime=None, policy=None, system_health=None):
    lines=["# AI Decision Context — Investment Quant v1.6","",f"Generated quality score: **{quality['quality_score']:.3f}** / actionable={quality['actionable']}",""]
    lines += ["## Market Regime v1.5", json.dumps(market_regime or {"status":"not_found"},ensure_ascii=False,indent=2),""]
    lines += ["## Policy guardrails",json.dumps(policy or {},ensure_ascii=False,indent=2),"","## Integration health",json.dumps(system_health or {},ensure_ascii=False,indent=2),"","## Source health"]
    for h in health:
        lines.append(f"- {h.source}: {h.status} / records={h.records} / tier={h.source_tier}"+(f" / {h.error[:160]}" if h.error else ""))
    report=read_v1_3_daily_report()
    if report:
        lines += ["","## v1.3 Daily Quant Screen report (existing output; preserved)",report]
    lines += ["","## Critical / high company events"]
    important=[e for e in events if e.priority in ("critical","high")]
    if not important: lines.append("- none detected (this does NOT prove that no event exists)")
    for e in important[:50]:
        lines.append(f"- [{e.priority.upper()}] {e.code} {e.name} | {e.event_date} | {e.event_type} | {e.title} | {e.source} ({e.source_tier}) | status={e.data_status} | {e.source_url}")
        if e.raw_excerpt: lines.append(f"  excerpt: {e.raw_excerpt[:700]}")
    lines += ["","## Mandatory AI rules",
      "- Primary source > secondary news > model inference.",
      "- A secondary RSS item is a detection signal, never sufficient evidence for a trade.",
      "- If a material fact is missing/stale, write 判断不能 or データ未取得.",
      "- Distinguish price date, event date, filing date, and fetched_at.",
      "- Market Regime is context, not an automatic buy/sell signal.",
      "- v1.3 screening score is candidate ranking, not a trade recommendation.",
      "- Evaluate portfolio impact and alternatives including 何もしない before buy/sell.",
      "- Do not infer the user's private positions from the public GitHub repository. Private portfolio data must be joined from the user's Drive/account data separately."
    ]
    return "\n".join(lines)


def load_market_regime():
    for p in ["data/regime/market_regime_latest.json"]:
        if Path(p).exists():
            try: return json.loads(Path(p).read_text(encoding="utf-8"))
            except Exception: pass
    return {"status":"not_found"}
