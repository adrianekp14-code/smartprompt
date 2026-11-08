"""Metrics for an arbitrary ticker list: python3 tools/lookup.py TICK1 TICK2 ..."""
import json, os, sys, subprocess
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
want = set(t.upper() for t in sys.argv[1:])
fund = json.load(open(f"{D}/fundamentals.json"))
sub = [d for d in fund if d["ticker"] in want]
missing = want - {d["ticker"] for d in sub}
json.dump(sub, open(f"{D}/lookup.json", "w"))
here = os.path.dirname(__file__)
subprocess.run([sys.executable, f"{here}/enrich.py", f"{D}/lookup.json"], check=True)
os.replace(f"{D}/ranked.json", f"{D}/ranked_main.json") if os.path.exists(f"{D}/ranked.json") and not os.path.exists(f"{D}/ranked_main.json") else None
subprocess.run([sys.executable, f"{here}/rank.py", f"{D}/lookup_enriched.json", "500"], check=True)
os.replace(f"{D}/ranked.json", f"{D}/ranked_lookup.json")
print("not in SEC us-gaap revenue universe (IFRS filer / tiny / tag mismatch):", sorted(missing))
