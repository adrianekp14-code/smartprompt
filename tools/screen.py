"""Stage-1 fundamental screen from cached SEC XBRL frames -> data_cache/fundamentals.json"""
import json, os, glob
from fetch_frames import frame, REV
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
tick = json.load(open(f"{D}/tickers.json"))
F = tick["fields"]; rows = [dict(zip(F, r)) for r in tick["data"]]
bycik = {}
for r in rows:
    if r["exchange"] in ("Nasdaq", "NYSE", "CBOE", "NYSE American") or r["exchange"] is None:
        bycik.setdefault(str(r["cik"]), []).append(r)

def rev(period):
    out = {}
    for c in REV:
        for k, v in frame("us-gaap", c, "USD", period).items():
            out[k] = max(out.get(k, 0), v)
    return out
def f(c, p, unit="USD", tax="us-gaap"): return frame(tax, c, unit, p)
def latest(c, unit="USD", tax="us-gaap"):
    a, b, cc = f(c, "CY2026Q3I", unit, tax), f(c, "CY2026Q2I", unit, tax), f(c, "CY2025Q4I", unit, tax)
    return lambda k: a.get(k, b.get(k, cc.get(k)))

R = {y: rev(y) for y in ["CY2021", "CY2022", "CY2023", "CY2024", "CY2025"]}
Q = {q: rev(q) for q in ["CY2025Q1", "CY2025Q2", "CY2025Q3", "CY2026Q1", "CY2026Q2", "CY2026Q3"]}
OIq = {q: f("OperatingIncomeLoss", q) for q in Q}
GPq = {q: f("GrossProfit", q) for q in Q}
gp, cor, cogs = f("GrossProfit", "CY2025"), f("CostOfRevenue", "CY2025"), f("CostOfGoodsAndServicesSold", "CY2025")
oi, ni, cfo, capex = (f(c, "CY2025") for c in ["OperatingIncomeLoss", "NetIncomeLoss", "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment"])
oi24 = f("OperatingIncomeLoss", "CY2024"); cfo24 = f("NetCashProvidedByUsedInOperatingActivities", "CY2024"); capex24 = f("PaymentsToAcquirePropertyPlantAndEquipment", "CY2024")
sbc = f("ShareBasedCompensation", "CY2025")
da1, da2 = f("DepreciationDepletionAndAmortization", "CY2025"), f("DepreciationAndAmortization", "CY2025")
dil22, dil25 = f("WeightedAverageNumberOfDilutedSharesOutstanding", "CY2022", "shares"), f("WeightedAverageNumberOfDilutedSharesOutstanding", "CY2025", "shares")
cash, sti, msc = latest("CashAndCashEquivalentsAtCarryingValue"), latest("ShortTermInvestments"), latest("MarketableSecuritiesCurrent")
ltdn, ltd, ltdc = latest("LongTermDebtNoncurrent"), latest("LongTermDebt"), latest("LongTermDebtCurrent")
eq, assets, gw = latest("StockholdersEquity"), latest("Assets"), latest("Goodwill")
sh = latest("EntityCommonStockSharesOutstanding", "shares", "dei")

out = []
for k, tl in bycik.items():
    r25 = R["CY2025"].get(k)
    if not r25 or r25 < 25e6: continue
    d = {"cik": k, "ticker": tl[0]["ticker"], "name": tl[0]["name"], "exchange": tl[0]["exchange"], "rev": {y: R[y].get(k) for y in R}}
    base = R["CY2022"].get(k) or R["CY2021"].get(k) and None
    yrs = 3 if R["CY2022"].get(k) else (2 if R["CY2023"].get(k) else None)
    b = R["CY2022"].get(k) or R["CY2023"].get(k)
    d["cagr3"] = (r25 / b) ** (1 / yrs) - 1 if b and b > 0 and yrs else None
    d["yoy25"] = r25 / R["CY2024"][k] - 1 if R["CY2024"].get(k) else None
    # TTM using reported quarters
    qs = [q for q in ["Q1", "Q2", "Q3"] if Q["CY2026" + q].get(k) and Q["CY2025" + q].get(k)]
    if qs:
        d["ttm_rev"] = r25 + sum(Q["CY2026" + q][k] - Q["CY2025" + q][k] for q in qs)
        lq = qs[-1]; d["last_q"] = "CY2026" + lq
        d["q_yoy"] = Q["CY2026" + lq][k] / Q["CY2025" + lq][k] - 1
        o1, o0 = OIq["CY2026" + lq].get(k), OIq["CY2025" + lq].get(k)
        d["q_opm"] = o1 / Q["CY2026" + lq][k] if o1 is not None else None
        d["q_opm_prev"] = o0 / Q["CY2025" + lq][k] if o0 is not None else None
        g1 = GPq["CY2026" + lq].get(k); d["q_gm"] = g1 / Q["CY2026" + lq][k] if g1 is not None else None
    else:
        d["ttm_rev"] = r25; d["q_yoy"] = None
    g = gp.get(k)
    if g is None and (cor.get(k) or cogs.get(k)): g = r25 - (cor.get(k) or cogs.get(k))
    d["gm"] = g / r25 if g is not None else None
    d["opm"] = oi[k] / r25 if k in oi else None
    d["opm24"] = oi24[k] / R["CY2024"][k] if k in oi24 and R["CY2024"].get(k) else None
    d["ni"] = ni.get(k); d["oi"] = oi.get(k)
    d["fcf"] = cfo[k] - capex.get(k, 0) if k in cfo else None
    d["fcf24"] = cfo24[k] - capex24.get(k, 0) if k in cfo24 else None
    d["sbc_pct"] = sbc[k] / r25 if k in sbc else None
    d["da"] = da1.get(k, da2.get(k))
    d["dilution3"] = dil25[k] / dil22[k] - 1 if k in dil25 and dil22.get(k) else None
    d["cash"] = (cash(k) or 0) + (sti(k) or 0) + (msc(k) or 0)
    d["debt"] = (ltdn(k) or ltd(k) or 0) + (ltdc(k) or 0)
    d["equity"], d["assets"], d["goodwill"], d["shares"] = eq(k), assets(k), gw(k), sh(k)
    out.append(d)
json.dump(out, open(f"{D}/fundamentals.json", "w"))
print("universe with rev>=25M:", len(out))
# stage-1 filter
def ok(d):
    g = d["cagr3"] if d["cagr3"] is not None else d["yoy25"]
    if g is None: return False
    growth = g >= 0.10 or (d["q_yoy"] or 0) >= 0.20
    if not growth: return False
    if d["gm"] is not None and d["gm"] < 0.25: return False
    prof = (d["opm"] or -1) > 0 or (d.get("q_opm") or -1) > 0
    return prof and d["shares"]
s1 = [d for d in out if ok(d)]
json.dump(s1, open(f"{D}/stage1.json", "w"))
print("stage1 pass:", len(s1))
