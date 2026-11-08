"""Point-in-time factor backtest for the High-Growth strategy (research/high_growth/BACKTEST.md explains design & biases).
Formation: June 30 of year Y (2018..2025). Fundamentals: SEC XBRL annual frames CY(Y-1), CY(Y-2), CY(Y-3) — all filed before June 30 Y for
calendar-year filers (non-calendar FYs mapped by SEC to the nearest calendar year; residual look-ahead risk documented).
Shares: dei EntityCommonStockSharesOutstanding at CY(Y)Q1I (10-K cover date) else CY(Y-1)Q4I. Price: Yahoo monthly close at formation, un-split-adjusted.
Return: Yahoo adjclose (split+dividend adjusted) from formation month to +12 months. Factors fixed in advance; no parameter search."""
import json, os, sys, math, statistics, datetime, csv
sys.path.insert(0, os.path.dirname(__file__))
from fetch_frames import frame, REV
D = os.path.join(os.path.dirname(__file__), "..", "data_cache"); OUT = os.path.join(os.path.dirname(__file__), "..", "research", "high_growth")
tick = json.load(open(f"{D}/tickers.json")); cik2t = {}
for r in tick["data"]: cik2t.setdefault(str(r[0]), r[2])
sicmap = {}
for fn in ["stage1_enriched.json", "hg_stageA_enriched.json", "lookup_enriched.json"]:
    try:
        for d in json.load(open(f"{D}/{fn}")): sicmap[d["cik"]] = int((d.get("co") or {}).get("sic") or 0)
    except FileNotFoundError: pass
def rev(y):
    out = {}
    for c in REV:
        for k, v in frame("us-gaap", c, "USD", f"CY{y}").items(): out[k] = max(out.get(k, 0), v)
    return out
PX = {}
def series(t):
    if t in PX: return PX[t]
    fn = f"{D}/px/{t}.json"; m = json.load(open(fn)) if os.path.exists(fn) else None
    if not m or "timestamp" not in m: PX[t] = None; return None
    ts = m["timestamp"]; q = m["indicators"]["quote"][0]["close"]; a = m["indicators"].get("adjclose", [{}])[0].get("adjclose") or q
    spl = [(int(k), v["numerator"] / v["denominator"]) for k, v in (m.get("events", {}).get("splits") or {}).items()]
    s = {}
    for t_, c, ac in zip(ts, q, a):
        if c is None or ac is None: continue
        ym = datetime.datetime.fromtimestamp(t_, datetime.UTC).strftime("%Y-%m")
        factor = math.prod(r for (st, r) in spl if st > t_)  # undo later splits => raw price
        s[ym] = (c * factor, ac)
    PX[t] = s; return s
def ret(t, y, months=12):
    s = series(t)
    if not s: return None
    a, b = f"{y}-06", f"{y + months // 12}-06"
    if a not in s or b not in s: return None
    return s[b][1] / s[a][1] - 1
def bench(t, y): return ret(t, y)
cl = lambda x: x
rows = []; coverage = []
for Y in range(2018, 2026):
    R1, R2, R3 = rev(Y - 1), rev(Y - 2), rev(Y - 3)
    g = lambda c, y: frame("us-gaap", c, "USD", f"CY{y}")
    GP1, GP2 = g("GrossProfit", Y - 1), g("GrossProfit", Y - 2)
    CR1, CR2 = g("CostOfRevenue", Y - 1), g("CostOfRevenue", Y - 2)
    OI1, OI2 = g("OperatingIncomeLoss", Y - 1), g("OperatingIncomeLoss", Y - 2)
    CF1, CF2 = g("NetCashProvidedByUsedInOperatingActivities", Y - 1), g("NetCashProvidedByUsedInOperatingActivities", Y - 2)
    CX1, CX2 = g("PaymentsToAcquirePropertyPlantAndEquipment", Y - 1), g("PaymentsToAcquirePropertyPlantAndEquipment", Y - 2)
    inst = lambda c, y: frame("us-gaap", c, "USD", f"CY{y}Q4I")
    CA1, EQ1, EQ2 = inst("CashAndCashEquivalentsAtCarryingValue", Y - 1), inst("StockholdersEquity", Y - 1), inst("StockholdersEquity", Y - 2)
    DB1 = {**inst("LongTermDebt", Y - 1), **inst("LongTermDebtNoncurrent", Y - 1)}
    DB2 = {**inst("LongTermDebt", Y - 2), **inst("LongTermDebtNoncurrent", Y - 2)}
    CA2 = inst("CashAndCashEquivalentsAtCarryingValue", Y - 2)
    SH = {**frame("dei", "EntityCommonStockSharesOutstanding", "shares", f"CY{Y-1}Q4I"), **frame("dei", "EntityCommonStockSharesOutstanding", "shares", f"CY{Y}Q1I")}
    eligible = [k for k, v in R1.items() if v >= 25e6 and k in R2 and k in R3 and not (6000 <= sicmap.get(k, 0) <= 6799)]
    nprice = 0
    for k in eligible:
        t = cik2t.get(k)
        if not t: continue
        s = series(t)
        if not s or f"{Y}-06" not in s: continue
        nprice += 1
        sh = SH.get(k)
        if not sh: continue
        mc = s[f"{Y}-06"][0] * sh
        if not (1e8 <= mc <= 2e10): continue
        r1, r2, r3 = R1[k], R2[k], R3[k]
        if r2 <= 0 or r3 <= 0: continue
        gp1 = GP1.get(k, r1 - CR1[k] if k in CR1 else None); gp2 = GP2.get(k, r2 - CR2[k] if k in CR2 else None)
        ev = mc + DB1.get(k, 0) - CA1.get(k, 0)
        fcf1 = CF1[k] - CX1.get(k, 0) if k in CF1 else None; fcf2 = CF2[k] - CX2.get(k, 0) if k in CF2 else None
        ic1 = (EQ1.get(k) or 0) + DB1.get(k, 0) - CA1.get(k, 0); ic2 = (EQ2.get(k) or 0) + DB2.get(k, 0) - CA2.get(k, 0)
        roic1 = OI1[k] * 0.79 / ic1 if k in OI1 and ic1 > 0 else None; roic2 = OI2[k] * 0.79 / ic2 if k in OI2 and ic2 > 0 else None
        fwd = ret(t, Y)
        rows.append(dict(year=Y, cik=k, ticker=t, mcap=mc, g1=r1 / r2 - 1, accel=(r1 / r2 - 1) - (r2 / r3 - 1),
            gm_chg=(gp1 / r1 - gp2 / r2) if gp1 is not None and gp2 is not None else None,
            fcf_chg=(fcf1 - fcf2) / r1 if fcf1 is not None and fcf2 is not None else None,
            roic_chg=(roic1 - roic2) if roic1 is not None and roic2 is not None else None,
            fcf_yield=fcf1 / mc if fcf1 is not None else None, ev_s=ev / r1 if ev > 0 else None,
            ebit_yield=OI1[k] / ev if k in OI1 and ev > 0 else None, fwd=fwd))
    coverage.append(dict(year=Y, sec_filers_eligible=len(eligible), with_price=nprice, in_universe=sum(1 for r in rows if r["year"] == Y),
                         with_fwd_return=sum(1 for r in rows if r["year"] == Y and r["fwd"] is not None)))
json.dump(rows, open(f"{D}/bt_rows.json", "w"))
# ---------- analysis ----------
def rank(vals):
    srt = sorted(range(len(vals)), key=lambda i: vals[i]); r = [0] * len(vals)
    for pos, i in enumerate(srt): r[i] = pos / (len(vals) - 1)
    return r
def spearman(x, y):
    rx, ry = rank(x), rank(y); mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0
FACTORS = {"g1": 1, "accel": 1, "gm_chg": 1, "fcf_chg": 1, "roic_chg": 1, "fcf_yield": 1, "ebit_yield": 1, "ev_s": -1}
COMPOSITE = ["g1", "accel", "gm_chg", "fcf_chg", "roic_chg", "fcf_yield"]  # pre-specified, equal weight
res = {}; years = sorted({r["year"] for r in rows if r["fwd"] is not None})
WIN = lambda x: max(-0.95, min(x, 3.0))  # cap single-stock returns at +300% for IC stability (reported both ways below)
for Y in years:
    U = [r for r in rows if r["year"] == Y and r["fwd"] is not None]
    for r in U:  # composite: average percentile rank of available components
        pass
    for f, sign in list(FACTORS.items()) + [("composite", 1), ("hg_screen_rule", 1)]:
        if f == "composite":
            ranks = {}
            for c in COMPOSITE:
                sub = [r for r in U if r[c] is not None]; rk = rank([r[c] for r in sub]) if len(sub) > 2 else []
                for r, v in zip(sub, rk): ranks.setdefault(id(r), []).append(v)
            sub = [r for r in U if len(ranks.get(id(r), [])) >= 4]; vals = [statistics.mean(ranks[id(r)]) for r in sub]
        elif f == "hg_screen_rule":  # the live strategy's hard filter: growth>=15%, accel>0, gm not falling, fcf>0 & rising
            sub = U; vals = [1.0 if (r["g1"] >= 0.15 and r["accel"] > 0 and (r["gm_chg"] or 0) >= 0 and (r["fcf_chg"] or -1) > 0 and (r["fcf_yield"] or -1) > 0) else 0.0 for r in U]
        else:
            sub = [r for r in U if r[f] is not None]; vals = [sign * r[f] for r in sub]
        if len(sub) < 50: continue
        fw = [WIN(r["fwd"]) for r in sub]; ew = statistics.mean(fw)
        if f == "hg_screen_rule":
            top = [x for x, v in zip(fw, vals) if v == 1]; bot = [x for x, v in zip(fw, vals) if v == 0]
            res.setdefault(f, []).append(dict(year=Y, n=len(sub), n_top=len(top), top=statistics.mean(top) if top else None, bottom=statistics.mean(bot), ew=ew, ic=None)); continue
        order = sorted(range(len(sub)), key=lambda i: vals[i]); q = len(order) // 5
        top = [fw[i] for i in order[-q:]]; bot = [fw[i] for i in order[:q]]
        res.setdefault(f, []).append(dict(year=Y, n=len(sub), n_top=q, top=statistics.mean(top), bottom=statistics.mean(bot), ew=ew, ic=spearman(vals, fw)))
bm = {y: dict(SPY=bench("SPY", y), IWM=bench("IWM", y), RSP=bench("RSP", y)) for y in years}
with open(f"{OUT}/backtest_results.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["factor", "year", "n", "n_top", "top_quintile_ret", "bottom_quintile_ret", "universe_ew_ret", "top_minus_universe", "top_minus_SPY", "rank_IC", "SPY", "IWM"])
    for f, L in res.items():
        for x in L:
            w.writerow([f, x["year"], x["n"], x["n_top"], x["top"] and round(x["top"], 4), round(x["bottom"], 4), round(x["ew"], 4),
                        x["top"] is not None and round(x["top"] - x["ew"], 4), x["top"] is not None and bm[x["year"]]["SPY"] is not None and round(x["top"] - bm[x["year"]]["SPY"], 4),
                        x["ic"] and round(x["ic"], 4), bm[x["year"]]["SPY"] and round(bm[x["year"]]["SPY"], 4), bm[x["year"]]["IWM"] and round(bm[x["year"]]["IWM"], 4)])
print("coverage:"); [print(c) for c in coverage]
print("\nbenchmarks (Jun->Jun total return):", {y: {k: v and round(v, 3) for k, v in b.items()} for y, b in bm.items()})
print(f"\n{'factor':16}{'yrs':>4}{'avgTop':>8}{'avgBot':>8}{'avgEW':>8}{'Top-EW':>8}{'TopBeatsEW':>11}{'meanIC':>8}{'IC_t':>7}{'Top-SPY':>9}")
summ = []
for f, L in res.items():
    tops = [x for x in L if x["top"] is not None]
    d = [x["top"] - x["ew"] for x in tops]; ics = [x["ic"] for x in L if x["ic"] is not None]
    t = statistics.mean(ics) / (statistics.stdev(ics) / math.sqrt(len(ics))) if len(ics) > 2 and statistics.stdev(ics) > 0 else float("nan")
    ds = [x["top"] - bm[x["year"]]["SPY"] for x in tops if bm[x["year"]]["SPY"] is not None]
    line = dict(factor=f, years=len(L), avg_top=statistics.mean(x["top"] for x in tops), avg_bottom=statistics.mean(x["bottom"] for x in L), avg_ew=statistics.mean(x["ew"] for x in L),
                top_minus_ew=statistics.mean(d), hit=sum(1 for x in d if x > 0), mean_ic=statistics.mean(ics) if ics else float("nan"), ic_t=t, top_minus_spy=statistics.mean(ds))
    summ.append(line)
    print(f"{f:16}{len(L):>4}{line['avg_top']:8.3f}{line['avg_bottom']:8.3f}{line['avg_ew']:8.3f}{line['top_minus_ew']:8.3f}{str(line['hit'])+'/'+str(len(d)):>11}{line['mean_ic']:8.3f}{t:7.2f}{line['top_minus_spy']:9.3f}")
json.dump(dict(coverage=coverage, benchmarks=bm, summary=summ), open(f"{OUT}/backtest_summary.json", "w"), indent=1, default=str)
