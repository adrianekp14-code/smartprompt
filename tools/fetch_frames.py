"""Pull SEC XBRL 'frames' (one fact per company per period) for screening.
Free public SEC API; obeys SEC fair-access (<10 req/s, descriptive UA)."""
import json, os, sys, time, urllib.request
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
CACHE = os.path.join(os.path.dirname(__file__), "..", "data_cache", "frames")
os.makedirs(CACHE, exist_ok=True)

def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2 ** i)
        except Exception:
            time.sleep(2 ** i)
    return None

def frame(tax, concept, unit, period):
    fn = os.path.join(CACHE, f"{tax}_{concept}_{unit}_{period}.json")
    if os.path.exists(fn):
        return json.load(open(fn))
    d = get(f"https://data.sec.gov/api/xbrl/frames/{tax}/{concept}/{unit}/{period}.json")
    out = {str(x["cik"]): x["val"] for x in (d or {}).get("data", [])}
    json.dump(out, open(fn, "w")); time.sleep(0.15)
    return out

REV = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
       "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]
DUR = ["GrossProfit", "CostOfRevenue", "CostOfGoodsAndServicesSold", "OperatingIncomeLoss", "NetIncomeLoss",
       "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment",
       "ShareBasedCompensation", "DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
       "WeightedAverageNumberOfDilutedSharesOutstanding", "IncomeTaxExpenseBenefit", "InterestExpense"]
INST = ["CashAndCashEquivalentsAtCarryingValue", "ShortTermInvestments", "MarketableSecuritiesCurrent",
        "LongTermDebtNoncurrent", "LongTermDebt", "LongTermDebtCurrent", "OperatingLeaseLiabilityNoncurrent",
        "StockholdersEquity", "Assets", "Goodwill"]
if __name__ == "__main__":
    jobs = []
    for y in ["CY2021", "CY2022", "CY2023", "CY2024", "CY2025"]:
        for c in REV: jobs.append(("us-gaap", c, "USD", y))
    for q in ["CY2025Q1", "CY2025Q2", "CY2025Q3", "CY2026Q1", "CY2026Q2", "CY2026Q3"]:
        for c in REV + ["OperatingIncomeLoss", "GrossProfit", "NetIncomeLoss"]: jobs.append(("us-gaap", c, "USD", q))
    for y in ["CY2024", "CY2025"]:
        for c in DUR:
            jobs.append(("us-gaap", c, "shares" if "Shares" in c else "USD", y))
    jobs.append(("us-gaap", "WeightedAverageNumberOfDilutedSharesOutstanding", "shares", "CY2022"))
    for p in ["CY2025Q4I", "CY2026Q2I", "CY2026Q3I"]:
        for c in INST: jobs.append(("us-gaap", c, "USD", p))
        jobs.append(("dei", "EntityCommonStockSharesOutstanding", "shares", p))
    for p in ["CY2025Q3I", "CY2026Q1I"]:
        jobs.append(("dei", "EntityCommonStockSharesOutstanding", "shares", p))
    for i, j in enumerate(jobs):
        d = frame(*j)
        print(i, len(jobs), j, len(d), flush=True)
