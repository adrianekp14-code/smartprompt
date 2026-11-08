"""Pre-declared robustness checks on bt_rows.json (no new factors): (1) small caps $100M-$2B only, (2) un-winsorized returns, (3) median instead of mean."""
import json, statistics, os
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
rows = json.load(open(f"{D}/bt_rows.json"))
COMP = ["g1", "accel", "gm_chg", "fcf_chg", "roic_chg", "fcf_yield"]
def pr(vals):
    o = sorted(range(len(vals)), key=lambda i: vals[i]); r = [0] * len(vals)
    for p, i in enumerate(o): r[i] = p / max(len(vals) - 1, 1)
    return r
def run(label, filt, agg=statistics.mean, cap=True):
    out = []
    for Y in sorted({r["year"] for r in rows}):
        U = [r for r in rows if r["year"] == Y and r["fwd"] is not None and filt(r)]
        rk = {}
        for c in COMP:
            s = [r for r in U if r[c] is not None]
            for r, v in zip(s, pr([r[c] for r in s])): rk.setdefault(id(r), []).append(v)
        s = [r for r in U if len(rk.get(id(r), [])) >= 4]
        if len(s) < 50: continue
        o = sorted(s, key=lambda r: statistics.mean(rk[id(r)])); q = len(o) // 5
        f = (lambda x: max(-0.95, min(x, 3))) if cap else (lambda x: x)
        top = agg([f(r["fwd"]) for r in o[-q:]]); ew = agg([f(r["fwd"]) for r in s]); bot = agg([f(r["fwd"]) for r in o[:q]])
        out.append((Y, len(s), top - ew, top - bot))
    d = [x[2] for x in out]
    print(f"{label:38} years={len(out)} mean(top-EW)={statistics.mean(d):+.3f} median={statistics.median(d):+.3f} beats={sum(x>0 for x in d)}/{len(d)} mean(top-bottom)={statistics.mean(x[3] for x in out):+.3f}")
    return out
run("composite, all caps (baseline)", lambda r: True)
run("composite, small caps $100M-$2B", lambda r: r["mcap"] <= 2e9)
run("composite, mid caps $2B-$20B", lambda r: r["mcap"] > 2e9)
run("composite, un-winsorized", lambda r: True, cap=False)
run("composite, median returns", lambda r: True, agg=statistics.median)
run("composite + cheapest half EV/S", lambda r: r["ev_s"] is not None and r["ev_s"] < 3)
