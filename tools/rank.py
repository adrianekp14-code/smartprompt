"""Compute valuation metrics + quantitative pre-score. Pre-score only prioritises human-style research; it is not a return forecast."""
import json, os, sys, csv
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
s = json.load(open(sys.argv[1] if len(sys.argv) > 1 else f"{D}/stage1_enriched.json"))
EXCL = lambda sic: sic and (6000 <= int(sic) <= 6799)  # banks, insurers, REITs, holding cos
res = []
for d in s:
    if not d.get("px") or not d.get("co") or not d.get("shares") or d["px"].get("cur") not in ("USD", None): continue
    if EXCL(d["co"]["sic"]): continue
    mc = d["px"]["price"] * d["shares"]; d["mcap"] = mc
    if mc < 8e7: continue
    ev = mc + d["debt"] - d["cash"]; d["ev"] = ev
    rv = d["ttm_rev"]; d["ev_s"] = ev / rv
    ebit = d["oi"]; d["ev_ebit"] = ev / ebit if ebit and ebit > 0 else None
    ebitda = (ebit or 0) + (d["da"] or 0); d["ev_ebitda"] = ev / ebitda if ebitda > 0 else None
    d["fcf_yield"] = d["fcf"] / mc if d["fcf"] is not None else None
    d["pe"] = mc / d["ni"] if d["ni"] and d["ni"] > 0 else None
    d["fcf_m"] = d["fcf"] / d["rev"]["CY2025"] if d["fcf"] is not None else None
    d["ret1y"] = d["px"]["price"] / d["px"]["p1y"] - 1 if d["px"]["p1y"] else None
    g = d["cagr3"] if d["cagr3"] is not None else d["yoy25"]
    cl = lambda x, a, b: max(0, min(1, (x - a) / (b - a)))
    growth = 0.6 * cl(g, 0.05, 0.40) + 0.4 * cl(d["q_yoy"] if d["q_yoy"] is not None else g, 0.0, 0.40)
    quality = 0.4 * cl(d["gm"] if d["gm"] is not None else 0.35, 0.25, 0.70) + 0.3 * cl(d["opm"] or 0, 0.0, 0.30) + 0.3 * cl(d["fcf_m"] if d["fcf_m"] is not None else 0, 0, 0.25)
    netdebt = d["debt"] - d["cash"]
    strength = 1.0 if netdebt <= 0 else max(0, 1 - netdebt / max(ebitda, 1) / 4)
    dil = 1 - cl(d["dilution3"] if d["dilution3"] is not None else 0.05, 0.0, 0.25)
    sbcp = 1 - cl(d["sbc_pct"] or 0, 0.03, 0.15)
    # valuation: growth-adjusted EV/S and FCF yield
    gadj = d["ev_s"] / max(g * 100, 5) / max(d["opm"] or 0.05, 0.05) if d["ev_s"] > 0 else 0
    val = 0.5 * (1 - cl(gadj, 0.2, 3.0)) + 0.5 * cl(d["fcf_yield"] if d["fcf_yield"] is not None else 0, 0.0, 0.07)
    size = 1.0 if 1e8 <= mc <= 1e10 else (0.6 if mc <= 2e10 else 0.2)
    d["scores"] = dict(growth=growth, quality=quality, strength=strength, dilution=dil, sbc=sbcp, valuation=val, size=size)
    d["pre"] = 100 * (0.25 * growth + 0.2 * quality + 0.15 * strength + 0.08 * dil + 0.05 * sbcp + 0.2 * val + 0.07 * size)
    res.append(d)
res.sort(key=lambda d: -d["pre"])
json.dump(res, open(f"{D}/ranked.json", "w"))
print(len(res), "ranked (ex-financials, mcap>=80M)")
pct = lambda x: f"{x*100:5.0f}%" if x is not None else "   n/a"
num = lambda x: f"{x:6.1f}" if x is not None else "   n/a"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 160
for i, d in enumerate(res[:N]):
    print(f"{i+1:3} {d['ticker']:6} {d['name'][:26]:26} {d['co']['sicDesc'][:24] if d['co']['sicDesc'] else '':24} mc{d['mcap']/1e9:6.2f}B cagr{pct(d['cagr3'])} q{pct(d['q_yoy'])} gm{pct(d['gm'])} opm{pct(d['opm'])} fcfm{pct(d['fcf_m'])} EV/S{num(d['ev_s'])} EV/EBIT{num(d['ev_ebit'])} fcfY{pct(d['fcf_yield'])} dil{pct(d['dilution3'])} 1y{pct(d['ret1y'])} pre{d['pre']:5.1f}")
