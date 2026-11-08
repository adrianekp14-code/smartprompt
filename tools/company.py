"""Primary-source snapshot from SEC EDGAR for one ticker: python3 tools/company.py TICKER
Prints fiscal-year history of key XBRL facts, latest quarter, recent filings, and Form 4 activity."""
import json, os, sys, time, urllib.request, collections
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
t = sys.argv[1].upper()
tk = json.load(open(f"{D}/tickers.json")); cik = next(r[0] for r in tk["data"] if r[2] == t)
cf = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
sub = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
print(f"{sub['name']} | CIK {cik} | SIC {sub.get('sic')} {sub.get('sicDescription')} | FY end {sub.get('fiscalYearEnd')} | {sub.get('exchanges')}")
G = cf["facts"].get("us-gaap", {})
CONCEPTS = [("Revenue", ["SalesRevenueNet", "Revenues", "RevenueFromContractWithCustomerIncludingAssessedTax", "RevenueFromContractWithCustomerExcludingAssessedTax"]),
 ("GrossProfit", ["GrossProfit"]), ("OpIncome", ["OperatingIncomeLoss"]), ("NetIncome", ["NetIncomeLoss"]),
 ("CFO", ["NetCashProvidedByUsedInOperatingActivities"]), ("Capex", ["PaymentsToAcquirePropertyPlantAndEquipment"]),
 ("SBC", ["ShareBasedCompensation", "AllocatedShareBasedCompensationExpense"]), ("R&D", ["ResearchAndDevelopmentExpense"]),
 ("DilShares", ["WeightedAverageNumberOfDilutedSharesOutstanding"]), ("EPSdil", ["EarningsPerShareDiluted"]),
 ("Buyback", ["PaymentsForRepurchaseOfCommonStock"]), ("Dividends", ["PaymentsOfDividends", "PaymentsOfDividendsCommonStock"]),
 ("Acquisitions", ["PaymentsToAcquireBusinessesNetOfCashAcquired"]), ("StockIssued", ["ProceedsFromIssuanceOfCommonStock"])]
def annual(names):
    out = {}
    for n in names:
        for u, facts in G.get(n, {}).get("units", {}).items():
            for f in facts:
                if f.get("form") in ("10-K", "20-F", "40-F", "10-K/A") and f.get("fp") == "FY" and "start" in f:
                    days = (time.mktime(time.strptime(f["end"], "%Y-%m-%d")) - time.mktime(time.strptime(f["start"], "%Y-%m-%d"))) / 86400
                    if 340 < days < 390: out[f["end"][:7]] = max(out.get(f["end"][:7], f["val"]), f["val"])
    return out
def quarters(names):
    out = {}
    for n in names:
        for u, facts in G.get(n, {}).get("units", {}).items():
            for f in facts:
                if "start" in f and f.get("form", "").startswith("10-Q"):
                    days = (time.mktime(time.strptime(f["end"], "%Y-%m-%d")) - time.mktime(time.strptime(f["start"], "%Y-%m-%d"))) / 86400
                    if 80 < days < 100: out[f["end"]] = max(out.get(f["end"], f["val"]), f["val"])
    return out
rows = {k: annual(v) for k, v in CONCEPTS}
yrs = sorted({y for r in rows.values() for y in r})[-7:]
fmt = lambda v, k: ("" if v is None else (f"{v:.2f}" if k == "EPSdil" else f"{v/1e6:.1f}"))
print("FY end    " + "".join(f"{y:>10}" for y in yrs))
for k, _ in CONCEPTS:
    if rows[k]: print(f"{k:12}" + "".join(f"{fmt(rows[k].get(y), k):>10}" for y in yrs))
print("-- last 6 quarters (3-month) revenue / op income / net income ($M)")
qr, qo, qn = quarters(CONCEPTS[0][1]), quarters(["OperatingIncomeLoss"]), quarters(["NetIncomeLoss"])
for q in sorted(qr)[-6:]: print(f"  {q}  rev {qr[q]/1e6:8.1f}  op {qo.get(q, 0)/1e6:7.1f}  ni {qn.get(q, 0)/1e6:7.1f}")
def inst(names):
    for n in names:
        for u, facts in G.get(n, {}).get("units", {}).items():
            fs = [f for f in facts if "start" not in f]
            if fs: f = max(fs, key=lambda f: f["end"]); return f["end"], f["val"]
    return None, None
for lab, names in [("Cash", ["CashAndCashEquivalentsAtCarryingValue"]), ("ST invest", ["ShortTermInvestments", "MarketableSecuritiesCurrent"]),
                   ("LT debt", ["LongTermDebtNoncurrent", "LongTermDebt"]), ("Equity", ["StockholdersEquity"]), ("Goodwill", ["Goodwill"]),
                   ("Contract liab", ["ContractWithCustomerLiabilityCurrent"]), ("RPO", ["RevenueRemainingPerformanceObligation"])]:
    e, v = inst(names); print(f"  {lab:14} {e}  {v/1e6 if v else v}")
dei = cf["facts"].get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])
if dei: f = max(dei, key=lambda f: f["end"]); print(f"  Shares out (dei) as of {f['end']}: {f['val']/1e6:.2f}M (filed {f['filed']})")
r = sub["filings"]["recent"]
print("-- recent filings")
n4 = collections.Counter()
for i in range(len(r["form"])):
    fm = r["form"][i]
    if fm == "4": n4[r["filingDate"][i][:4]] += 1; continue
    if fm in ("10-K", "10-Q", "8-K", "DEF 14A", "S-3", "S-3ASR", "424B5", "424B4", "S-1", "20-F", "6-K", "SC 13D", "SC 13D/A", "10-K/A", "NT 10-K", "NT 10-Q", "8-K/A") and i < 60:
        print(f"  {r['filingDate'][i]} {fm:8} {r.get('items', [''] * 999)[i]:12} https://www.sec.gov/Archives/edgar/data/{cik}/{r['accessionNumber'][i].replace('-', '')}/{r['primaryDocument'][i]}")
print("-- Form 4 filings by year:", dict(sorted(n4.items())[-4:]))
