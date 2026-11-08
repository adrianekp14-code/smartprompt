"""Add price (Yahoo chart API) and SIC/industry (SEC submissions) to stage-1 names."""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
        except Exception: time.sleep(1 + i)
def price(t):
    d = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t.replace('.', '-')}?range=1y&interval=1d")
    try:
        m = d["chart"]["result"][0]; meta = m["meta"]; closes = [c for c in m["indicators"]["quote"][0]["close"] if c]
        return {"price": meta["regularMarketPrice"], "ts": meta["regularMarketTime"], "hi52": max(closes), "lo52": min(closes), "p1y": closes[0], "cur": meta.get("currency")}
    except Exception: return None
def sic(cik):
    d = get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"); time.sleep(0.12)
    if not d: return None
    return {"sic": d.get("sic"), "sicDesc": d.get("sicDescription"), "state": (d.get("addresses", {}).get("business") or {}).get("stateOrCountry"), "fy_end": d.get("fiscalYearEnd")}
if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else f"{D}/stage1.json"
    s = json.load(open(fn))
    with ThreadPoolExecutor(6) as ex: P = list(ex.map(lambda d: price(d["ticker"]), s))
    for d, p in zip(s, P): d["px"] = p
    for d in s: d["co"] = sic(d["cik"])
    json.dump(s, open(fn.replace(".json", "_enriched.json"), "w"))
    print(sum(1 for d in s if d["px"]), "prices;", sum(1 for d in s if d["co"]), "sic")
