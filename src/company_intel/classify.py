from __future__ import annotations

def classify_event(title: str) -> tuple[str,str]:
    t=(title or "").lower()
    rules=[
      (("決算短信","earnings","決算発表"), "earnings", "critical"),
      (("業績予想","forecast","上方修正","下方修正"), "guidance", "critical"),
      (("配当予想","配当","dividend"), "dividend", "high"),
      (("自己株式","自社株買","share repurchase","buyback"), "buyback", "high"),
      (("公開買付","tob","買収","合併","m&a","merger","acquisition"), "mna", "critical"),
      (("増資","新株","転換社債","cb","financing","offering"), "financing", "critical"),
      (("行政","訴訟","regulat","investigation","security incident","情報漏えい","漏洩"), "regulatory", "high"),
      (("人事","代表取締役","ceo"), "management", "normal"),
    ]
    for keys,typ,sev in rules:
        if any(k in t for k in keys): return typ,sev
    return "disclosure","normal"
