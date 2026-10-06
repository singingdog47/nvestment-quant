from __future__ import annotations
import json, math, os
from datetime import date, datetime
from pathlib import Path
from typing import Any
import pandas as pd

VERSION="2.0.0"; ROOT=Path("data"); OUT=ROOT/"shadow_swing_v2"; CONFIG=Path("config/shadow_swing_v2.json")

def read_json(p:Path,d:Any)->Any:
    try:return json.loads(p.read_text(encoding="utf-8"))
    except Exception:return d

def num(v,d=None):
    try:
        x=float(v);return x if math.isfinite(x) else d
    except (TypeError,ValueError):return d

def c01(v,d=.5): return max(0.,min(1.,float(num(v,d))))

def today_jst():
    o=os.getenv("SHADOW_V2_AS_OF_DATE")
    return date.fromisoformat(o) if o else datetime.utcnow().date()

def score_row(r:pd.Series):
    v=c01(num(r.get("value_score"),50)/100);q=c01(num(r.get("quality_score"),50)/100)
    g=c01(num(r.get("growth_score"),50)/100);m=c01(num(r.get("momentum_score"),50)/100)
    risk=c01(num(r.get("risk_score"),50)/100);r1=num(r.get("return_1m"),0) or 0;r3=num(r.get("return_3m"),0) or 0
    chase=c01(max(0,r1-15)/30,0);weak=c01(max(0,-r1)/20,0);medium=c01(max(0,r3)/40,0)
    out=[
      {"model":"expectation_gap","score":.28*g+.24*q+.22*v+.16*weak+.10*risk-.20*chase,"thesis":"fundamentals_vs_price_expectation"},
      {"model":"contrarian_quality","score":.40*q+.25*v+.20*weak+.15*risk,"thesis":"quality_value_after_weakness"},
      {"model":"fundamental_confirmed_momentum","score":.30*m+.25*g+.20*q+.15*medium+.10*risk-.25*chase,"thesis":"momentum_requires_fundamental_confirmation"}]
    rev=num(r.get("earnings_revision_score"))
    if rev is not None:out.append({"model":"earnings_revision","score":.55*c01(rev)+.25*g+.20*q,"thesis":"earnings_revision_confirmation"})
    ev=num(r.get("event_rerating_score"))
    if ev is not None:out.append({"model":"event_rerating","score":.60*c01(ev)+.20*q+.20*v,"thesis":"event_driven_rerating"})
    return out

def eligible_jp(s,cfg):
    if s.empty:return s
    x=s[s.market.astype(str).str.upper().isin(["JP","JAPAN","TSE","TOKYO"])].copy()
    if "eligible" in x:x=x[x.eligible.astype(str).str.lower().isin(["true","1"])]
    x=x[pd.to_numeric(x.liquidity_score,errors="coerce").fillna(0)>=float(cfg["research"]["min_liquidity_score"])]
    return x[pd.to_numeric(x.avg_turnover_30d,errors="coerce").fillna(0)>=float(cfg["research"]["min_avg_turnover_jpy"])]

def generate_signals(screen,cfg,as_of):
    rows=[]
    for _,r in eligible_jp(screen,cfg).iterrows():
        sym=str(r.get("ticker") or "");code=str(r.get("code") or "").strip()
        if not sym.endswith(".T"):sym=f"{code}.T" if code else ""
        price=num(r.get("price"))
        if not sym or not price or price<=0:continue
        for h in score_row(r):
            rows.append({"signal_date":as_of.isoformat(),"symbol":sym,"code":code,"name":str(r.get("name") or sym),
             "theme":str(r.get("theme") or "Other"),"model":h["model"],"score":round(h["score"]*100,4),
             "signal_price":price,"thesis":h["thesis"],"total_score_v1":num(r.get("total_score")),
             "momentum_score_v1":num(r.get("momentum_score")),"value_score_v1":num(r.get("value_score")),
             "quality_score_v1":num(r.get("quality_score")),"growth_score_v1":num(r.get("growth_score")),
             "return_1m":num(r.get("return_1m")),"return_3m":num(r.get("return_3m"))})
    if not rows:return pd.DataFrame()
    d=pd.DataFrame(rows);n=int(cfg["research"]["signals_per_day"]);k=max(1,n//d.model.nunique())
    out=pd.concat([g.nlargest(k,"score") for _,g in d.groupby("model")],ignore_index=True)
    return out.sort_values("score",ascending=False).drop_duplicates(["symbol","model"]).head(n).reset_index(drop=True)

def upsert(path,df,keys):
    if df.empty:return
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        old=pd.read_csv(path);df=pd.concat([old,df],ignore_index=True).drop_duplicates(keys,keep="last")
    df.to_csv(path,index=False)

def update_outcomes(as_of,screen,cfg):
    sigp=OUT/"signals.csv"
    if not sigp.exists():return pd.DataFrame()
    sig=pd.read_csv(sigp);prices={}
    for _,r in eligible_jp(screen,cfg).iterrows():
        sym=str(r.get("ticker") or "");code=str(r.get("code") or "").strip()
        if not sym.endswith(".T"):sym=f"{code}.T" if code else ""
        p=num(r.get("price"))
        if sym and p:prices[sym]=p
    today=pd.DataFrame([{"date":as_of.isoformat(),"symbol":s,"price":p} for s,p in prices.items()])
    obs=OUT/"daily_prices.csv";upsert(obs,today,["date","symbol"]);hist=pd.read_csv(obs).sort_values(["symbol","date"])
    result=[]
    for _,s in sig.iterrows():
        h=hist[(hist.symbol==s.symbol)&(hist.date.astype(str)>=str(s.signal_date))].drop_duplicates("date").sort_values("date")
        row=dict(s);base=num(s.signal_price)
        for n in cfg["research"]["horizons_sessions"]:
            if base and len(h)>int(n):row[f"return_{int(n)}s_pct"]=round((float(h.iloc[int(n)].price)/base-1)*100,4)
        result.append(row)
    out=pd.DataFrame(result);out.to_csv(OUT/"signal_outcomes.csv",index=False);return out

def latest(signals,outcomes,cfg,as_of):
    matured={}
    if not outcomes.empty:
        for n in cfg["research"]["horizons_sessions"]:
            col=f"return_{int(n)}s_pct"
            if col in outcomes:
                x=pd.to_numeric(outcomes[col],errors="coerce").dropna()
                matured[str(n)]={"n":int(len(x)),"mean_pct":round(float(x.mean()),4) if len(x) else None,
                                 "win_rate":round(float((x>0).mean()),4) if len(x) else None}
    return {"version":VERSION,"as_of_date":as_of.isoformat(),"mode":"SHADOW_ONLY","research_only":True,
      "initial_capital_jpy":cfg["initial_cash_jpy"],"max_positions":cfg["portfolio"]["max_positions"],
      "signals_today":signals.to_dict("records") if not signals.empty else [],
      "model_counts_today":signals.model.value_counts().to_dict() if not signals.empty else {},
      "matured_outcomes":matured,"note":"v1 control remains untouched; v2 measures hypothesis-level forward returns."}

def run(as_of=None):
    as_of=as_of or today_jst();cfg=read_json(CONFIG,{})
    if not cfg:raise FileNotFoundError(CONFIG)
    p=ROOT/"screening_latest.csv"
    if not p.exists():raise FileNotFoundError(p)
    screen=pd.read_csv(p);OUT.mkdir(parents=True,exist_ok=True)
    signals=generate_signals(screen,cfg,as_of);upsert(OUT/"signals.csv",signals,["signal_date","symbol","model"])
    outcomes=update_outcomes(as_of,screen,cfg);obj=latest(signals,outcomes,cfg,as_of)
    (OUT/"latest.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(obj,ensure_ascii=False,indent=2));return obj

if __name__=="__main__":run()
