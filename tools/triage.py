"""Write discovered/rejected CSVs from ranked screens + manual decisions (research/decisions.json)."""
import json, csv, os, datetime
D = "data_cache"; R = "research"; today = "2026-11-08"
main = json.load(open(f"{D}/ranked_main.json")); look = json.load(open(f"{D}/ranked_lookup.json"))
allr = {d["ticker"]: d for d in main + look}
manual = json.load(open(f"{R}/decisions.json"))
PHARMA = {2833, 2834, 2835, 2836, 8731, 8000, 8090}
COMMOD = {1311, 1381, 1382, 1389, 1040, 1000, 1090, 2911, 4412, 4400, 4424, 4923, 4922, 1221, 3330, 3310, 2860}
def triage(d):
    t = d["ticker"]
    if t in manual: return manual[t]["status"], manual[t]["reason"]
    sic = int(d["co"]["sic"] or 0); mc = d["mcap"]
    if sic in PHARMA: return "rejected", "Pharma/biotech: revenue tied to few drugs/licensing; needs clinical/patent analysis outside current screen; one-off license revenue distorts growth"
    if sic in COMMOD: return "rejected", "Commodity/shipping/energy-price driven earnings; growth reflects cycle not durable niche"
    if mc > 2.0e10: return "rejected", f"Large/mega-cap (${mc/1e9:.0f}B), widely followed; outside small/mid-cap mandate"
    if d["dilution3"] is not None and d["dilution3"] > 0.40: return "rejected", f"Share count +{d['dilution3']*100:.0f}% over 3y (or data artifact); dilution risk"
    if (d["ev_ebit"] or 0) > 45 or d["ev_s"] > 12: return "rejected", f"Valuation already discounts strong growth (EV/S {d['ev_s']:.1f}, EV/EBIT {d['ev_ebit'] or 0:.0f})"
    if d["cagr3"] is not None and d["cagr3"] > 1.0: return "rejected", "Revenue jump from acquisition/merger/one-off; organic growth unverifiable from screen"
    return "screened-pass", "Passed quantitative screen; not yet prioritized for qualitative research"
fields = ["ticker", "name", "exchange", "sic_desc", "market_cap_musd", "price", "price_date", "rev_cagr_3y", "last_q_rev_yoy", "gross_margin", "op_margin", "fcf_margin", "ev_sales", "ev_ebit", "fcf_yield", "share_change_3y", "net_debt_musd", "pre_score", "status", "reason", "first_seen", "last_reviewed"]
rows = []
for t, d in allr.items():
    st, why = triage(d)
    f = lambda x, p=1: None if x is None else round(x * (100 if p else 1), 1)
    rows.append(dict(ticker=t, name=d["name"], exchange=d["exchange"], sic_desc=d["co"]["sicDesc"], market_cap_musd=round(d["mcap"] / 1e6),
        price=d["px"]["price"], price_date=datetime.datetime.fromtimestamp(d["px"]["ts"], datetime.UTC).strftime("%Y-%m-%d"),
        rev_cagr_3y=f(d["cagr3"]), last_q_rev_yoy=f(d["q_yoy"]), gross_margin=f(d["gm"]), op_margin=f(d["opm"]), fcf_margin=f(d["fcf_m"]),
        ev_sales=f(d["ev_s"], 0), ev_ebit=f(d["ev_ebit"], 0), fcf_yield=f(d["fcf_yield"]), share_change_3y=f(d["dilution3"]),
        net_debt_musd=round((d["debt"] - d["cash"]) / 1e6), pre_score=round(d["pre"], 1), status=st, reason=why, first_seen=today, last_reviewed=today))
rows.sort(key=lambda r: -r["pre_score"])
with open(f"{R}/discovered_companies.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(rows)
with open(f"{R}/rejected_companies.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["ticker", "name", "market_cap_musd", "reason", "date", "revisit_trigger"]); w.writeheader()
    for r in rows:
        if r["status"] == "rejected":
            w.writerow(dict(ticker=r["ticker"], name=r["name"], market_cap_musd=r["market_cap_musd"], reason=r["reason"], date=today,
                            revisit_trigger=manual.get(r["ticker"], {}).get("revisit", "Material change in fundamentals or >30% price move")))
from collections import Counter
print(Counter(r["status"] for r in rows), len(rows))
