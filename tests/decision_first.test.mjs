import { test } from "node:test";
import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {decide} from "../scripts/decision_first.mjs";
const p=JSON.parse(readFileSync(new URL("../config/decision_first_v1.json",import.meta.url),"utf8"));
const now="2026-11-06T00:05:00Z";
test("Critical overnight future triggers cancel+precommitted exit without orders being executed",()=>{
const r=decide({now,market:{nikkei_future_pct:{value:-5.8,as_of:"2026-11-05T22:00:00Z"}},orders:[{ticker:"SAMPLE-BUY",side:"BUY",status:"OPEN",quantity:10,limit_price:1234,as_of:"2026-11-05T23:50:00Z"}],positions:[{ticker:"SAMPLE-SELL",shares:10,exit_on_critical:true}]},p);
assert.equal(r.market_level,"CRITICAL");assert.deepEqual(r.decisions.map(x=>x.action),["CANCEL_BUY","SELL"]);assert.equal(r.decisions[1].state,"PROPOSAL_ONLY");
});
test("Stale quote does not fabricate hard-stop execution recommendation",()=>{const r=decide({now,market:{vix:{value:21,as_of:now}},positions:[{ticker:"X",shares:10,hard_stop:100,latest_price:90,quote_as_of:"2026-11-05T17:00:00Z"}]},p);assert.notEqual(r.decisions[0].action,"SELL");});
test("Stale market data never means normal",()=>{const r=decide({now,market:{nikkei_future_pct:{value:-8,as_of:"2026-11-03T12:00:00Z"}}},p);assert.equal(r.market_level,"UNVERIFIED");assert.equal(r.notify,true);});
test("Executed orders cannot be cancelled again",()=>{const r=decide({now,market:{nikkei_future_pct:{value:-6,as_of:now}},orders:[{ticker:"SAMPLE-BUY",side:"BUY",status:"EXECUTED",quantity:10,as_of:now}]},p);assert.equal(r.decisions.length,0);});
test("A verified hard-stop can recommend a sell even without macro crisis",()=>{const r=decide({now,market:{vix:{value:20,as_of:now}},positions:[{ticker:"SAMPLE-SELL",shares:10,hard_stop:1200,latest_price:1100,quote_as_of:now}]},p);assert.equal(r.decisions[0].action,"SELL");});

test("Sell recommendation notifies even without macro risk",()=>{const r=decide({now,market:{vix:{value:20,as_of:now}},positions:[{ticker:"SAMPLE-SELL",shares:10,hard_stop:1200,latest_price:1100,quote_as_of:now}]},p);assert.equal(r.notify,true);});
