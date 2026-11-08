"""High-growth screen (strategy HG). Uses data_cache/fundamentals.json (from screen.py) + cached frames.
Stage A (fundamental, no price): growth >= 15% (3y CAGR or latest y/y), gross margin >= 35% or rising, no extreme dilution.
Stage B: price enrichment (enrich.py) then factor scoring + reverse DCF.
Outputs data_cache/hg_stageA.json, research/high_growth/hg_screen_YYYY-MM-DD.csv"""
import json, os, sys, csv, subprocess, datetime
sys.path.insert(0, os.path.dirname(__file__))
from fetch_frames import frame
from reverse_dcf import implied_growth
D = os.path.join(os.path.dirname(__file__), "..", "data_cache"); OUT = os.path.join(os.path.dirname(__file__), "..", "research", "high_growth")
os.makedirs(OUT, exist_ok=True)
fund = json.load(open(f"{D}/fundamentals.json"))
gp24 = frame("us-gaap", "GrossProfit", "USD", "CY2024"); cor24 = frame("us-gaap", "CostOfRevenue", "USD", "CY2024")
cogs24 = frame("us-gaap", "CostOfGoodsAndServicesSold", "USD", "CY2024")
def stageA(d):
    r = d["rev"]; g1 = d["yoy25"]; g3 = d["cagr3"]; q = d.get("q_yoy")
    g0 = r["CY2024"] / r["CY2023"] - 1 if r.get("CY2024") and r.get("CY2023") else None
    d["yoy24"] = g0
    g = max(x for x in [g1, g3, q, -9] if x is not None)
    if g < 0.15: return False
    if (g3 or 0) > 1.5 and (g1 or 0) > 1.0: return False  # acquisition/licensing spikes
    k = d["cik"]; r24 = r.get("CY2024")
    gp_24 = gp24.get(k) if k in gp24 else (r24 - (cor24.get(k) or cogs24.get(k)) if r24 and (cor24.get(k) or cogs24.get(k)) else None)
    d["gm24"] = gp_24 / r24 if gp_24 is not None and r24 else None
    gm = d["gm"]
    if gm is not None and gm < 0.35 and not (d["gm24"] and gm > d["gm24"] + 0.02): return False
    if d["dilution3"] is not None and d["dilution3"] > 0.45: return False
    return bool(d["shares"])
A = [d for d in fund if stageA(d)]
json.dump(A, open(f"{D}/hg_stageA.json", "w")); print("stage A:", len(A))
if "--no-price" in sys.argv: sys.exit()
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "enrich.py"), f"{D}/hg_stageA.json"], check=True)
S = json.load(open(f"{D}/hg_stageA_enriched.json"))
cl = lambda x, a, b: 0 if x is None else max(0.0, min(1.0, (x - a) / (b - a)))
rows = []
for d in S:
    p = d.get("px"); co = d.get("co") or {}
    if not p or p.get("cur") not in ("USD", None): continue
    sic = int(co.get("sic") or 0)
    if 6000 <= sic <= 6799: continue
    mc = p["price"] * d["shares"]
    if mc < 1e8: continue
    ev = mc + d["debt"] - d["cash"]; rev = d["ttm_rev"]
    fcfm = d["fcf"] / d["rev"]["CY2025"] if d["fcf"] is not None else None
    # factors (each 0..1), explicit and documented in STRATEGY.md
    growth = max(x for x in [d["cagr3"], d["q_yoy"], d["yoy25"], -1] if x is not None)
    accel = None
    if d.get("q_yoy") is not None and d["yoy25"] is not None: accel = d["q_yoy"] - d["yoy25"]
    elif d["yoy25"] is not None and d.get("yoy24") is not None: accel = d["yoy25"] - d["yoy24"]
    gm_trend = (d.get("q_gm") or d["gm"] or 0) - (d["gm24"] or d["gm"] or 0) if d["gm"] is not None else None
    opl = (d["opm"] - d["opm24"]) if d["opm"] is not None and d["opm24"] is not None else None
    fcf_trend = (d["fcf"] - d["fcf24"]) / d["rev"]["CY2025"] if d["fcf"] is not None and d["fcf24"] is not None else None
    netcash = d["cash"] - d["debt"]
    strength = 1.0 if netcash >= 0 else cl(-(-netcash) / max((d["oi"] or 0) + (d["da"] or 0), 1), -4, 0)
    # market-implied growth with target FCF margin = max(current FCF margin, 60% of gross margin * 0.35) capped 35%
    m0 = max(min(fcfm if fcfm is not None else 0, 0.4), -0.2)
    m1 = min(max(m0, 0.35 * (d["gm"] or 0.4) + 0.02, 0.08), 0.35)
    ig = implied_growth(ev, rev, m0, m1) if ev > 0 else -0.3
    gap = (growth - ig) if ig is not None else -1  # recent growth minus market-implied
    F = dict(growth=cl(growth, 0.10, 0.50), accel=cl(accel, -0.10, 0.15), gm_trend=cl(gm_trend, -0.03, 0.05),
             op_leverage=cl(opl, -0.05, 0.10), fcf_trend=cl(fcf_trend, -0.05, 0.10), strength=strength,
             dilution=1 - cl(d["dilution3"], 0.0, 0.30), expectations_gap=cl(gap, -0.10, 0.25))
    W = dict(growth=0.20, accel=0.10, gm_trend=0.10, op_leverage=0.10, fcf_trend=0.10, strength=0.10, dilution=0.10, expectations_gap=0.20)
    score = 100 * sum(F[k] * W[k] for k in W)
    rows.append(dict(ticker=d["ticker"], name=d["name"], sic=co.get("sicDesc"), mcap_musd=round(mc / 1e6), price=p["price"],
        price_ts=datetime.datetime.fromtimestamp(p["ts"], datetime.UTC).isoformat(timespec="minutes"),
        ttm_rev_musd=round(rev / 1e6, 1), growth=round(growth, 3), accel=None if accel is None else round(accel, 3),
        gm=None if d["gm"] is None else round(d["gm"], 3), gm_trend=None if gm_trend is None else round(gm_trend, 3),
        opm=None if d["opm"] is None else round(d["opm"], 3), op_lev=None if opl is None else round(opl, 3),
        fcf_m=None if fcfm is None else round(fcfm, 3), ev_sales=round(ev / rev, 2), implied_10y_cagr=None if ig is None else round(ig, 3),
        target_fcf_m=round(m1, 3), dil3=d["dilution3"] and round(d["dilution3"], 3), net_cash_musd=round(netcash / 1e6),
        hg_score=round(score, 1), **{"f_" + k: round(v, 2) for k, v in F.items()}))
rows.sort(key=lambda r: -r["hg_score"])
fn = f"{OUT}/hg_screen_{datetime.date.today()}.csv"
with open(fn, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("ranked:", len(rows), "->", fn)
