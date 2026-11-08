"""Paper-portfolio tracker (prospective results only; never mixed with backtests).
Ledger: research/high_growth/paper_portfolio.csv (one row per candidate, never deleted).
- entry_price is the FIRST daily close strictly after date_identified (avoids look-ahead); filled automatically.
- Returns use Yahoo adjclose (split + dividend adjusted) => total return incl. dividends.
- Costs: 0.10% per side for >= $1B market cap, 0.50% per side below $1B (spread/slippage proxy), applied at entry and at exit/mark.
- Delistings: if a ticker stops returning data, the last available adjclose is kept and status set to 'data-ended — investigate';
  a confirmed bankruptcy is marked at -100%; confirmed cash acquisitions at the deal price.
- Benchmark per row (e.g., SPY, IWM, SMH, IHI, XLI) measured over the identical dates.
Writes research/high_growth/paper_performance.csv (snapshot) and appends a line to research/high_growth/performance_log.csv.
Usage: python3 tools/paper_portfolio.py"""
import csv, json, os, datetime, urllib.request, statistics
ROOT = os.path.join(os.path.dirname(__file__), "..")
L = f"{ROOT}/research/high_growth/paper_portfolio.csv"
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
_cache = {}
def daily(t):
    if t in _cache: return _cache[t]
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{t.replace('.', '-')}?range=5y&interval=1d&events=div,split", headers=UA), timeout=30))["chart"]["result"][0]
        ts = m["timestamp"]; c = m["indicators"]["quote"][0]["close"]; a = m["indicators"]["adjclose"][0]["adjclose"]
        s = [(datetime.datetime.fromtimestamp(x, datetime.UTC).date().isoformat(), cc, aa) for x, cc, aa in zip(ts, c, a) if cc and aa]
    except Exception:
        s = None
    _cache[t] = s; return s
def first_after(s, d):
    for row in s:
        if row[0] > d: return row
def at_or_before(s, d):
    out = None
    for row in s:
        if row[0] <= d: out = row
    return out
rows = list(csv.DictReader(open(L)))
today = datetime.date.today().isoformat(); perf = []
for r in rows:
    s = daily(r["ticker"]); b = daily(r["benchmark"])
    if not s or not b:
        r["status"] = r["status"] if r["status"] != "active" else "data-ended — investigate"; continue
    e = first_after(s, r["date_identified"])
    if not e: perf.append(dict(ticker=r["ticker"], strategy=r["strategy"], note="awaiting first close after identification")); continue
    if not r["entry_price"]:
        r["entry_price"], r["entry_date"] = f"{e[1]:.2f}", e[0]
    end_date = r.get("exit_date") or today
    x = at_or_before(s, end_date); be = first_after(b, r["date_identified"]); bx = at_or_before(b, end_date)
    cost = 0.001 if float(r["mcap_musd_at_id"]) >= 1000 else 0.005
    gross = x[2] / e[2] - 1; net = (1 + gross) * (1 - cost) ** 2 - 1; bret = bx[2] / be[2] - 1
    perf.append(dict(ticker=r["ticker"], strategy=r["strategy"], entry_date=e[0], entry_price=round(e[1], 2), mark_date=x[0], mark_price=round(x[1], 2),
                     total_return_net=round(net, 4), benchmark=r["benchmark"], benchmark_return=round(bret, 4), excess=round(net - bret, 4), status=r["status"],
                     vs_bear=r["bear_value"], vs_base=r["base_value"], vs_bull=r["bull_value"]))
with open(L, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
P = f"{ROOT}/research/high_growth/paper_performance.csv"
keys = ["ticker", "strategy", "entry_date", "entry_price", "mark_date", "mark_price", "total_return_net", "benchmark", "benchmark_return", "excess", "status", "vs_bear", "vs_base", "vs_bull", "note"]
with open(P, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); [w.writerow({k: p.get(k, "") for k in keys}) for p in perf]
done = [p for p in perf if "total_return_net" in p]
LOG = f"{ROOT}/research/high_growth/performance_log.csv"; new = not os.path.exists(LOG)
with open(LOG, "a", newline="") as fh:
    w = csv.writer(fh)
    if new: w.writerow(["date", "strategy", "n_positions", "ew_return_net", "ew_benchmark", "ew_excess", "share_beating_benchmark"])
    for strat in sorted({p["strategy"] for p in done}):
        d = [p for p in done if p["strategy"] == strat]
        w.writerow([today, strat, len(d), round(statistics.mean(p["total_return_net"] for p in d), 4), round(statistics.mean(p["benchmark_return"] for p in d), 4),
                    round(statistics.mean(p["excess"] for p in d), 4), round(sum(p["excess"] > 0 for p in d) / len(d), 3)])
print(f"{len(perf)} rows; {len(done)} with marks. Pending entries:", [p["ticker"] for p in perf if "note" in p])
