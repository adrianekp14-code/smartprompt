"""Historical data for the point-in-time backtest.
1) SEC XBRL frames CY2015..CY2025 (annual) + year-end instants.
2) Yahoo monthly price history (10y, split events, adjclose incl. dividends) for every ticker in fundamentals + benchmarks."""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from fetch_frames import frame, REV
D = os.path.join(os.path.dirname(__file__), "..", "data_cache")
UA = {"User-Agent": "EquityResearchAgent/1.0 research-bot"}
ANN = ["GrossProfit", "CostOfRevenue", "CostOfGoodsAndServicesSold", "OperatingIncomeLoss", "NetIncomeLoss",
       "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment"]
INST = ["CashAndCashEquivalentsAtCarryingValue", "LongTermDebtNoncurrent", "LongTermDebt", "StockholdersEquity"]
def frames():
    for y in range(2015, 2026):
        for c in REV + ANN: frame("us-gaap", c, "USD", f"CY{y}")
        for c in INST: frame("us-gaap", c, "USD", f"CY{y}Q4I")
        frame("dei", "EntityCommonStockSharesOutstanding", "shares", f"CY{y}Q4I")
        frame("dei", "EntityCommonStockSharesOutstanding", "shares", f"CY{y+1}Q1I")
        print("frames", y, flush=True)
def px(t):
    fn = f"{D}/px/{t}.json"
    if os.path.exists(fn): return
    for i in range(3):
        try:
            u = f"https://query1.finance.yahoo.com/v8/finance/chart/{t.replace('.', '-')}?range=10y&interval=1mo&events=div,split"
            d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
            json.dump(d["chart"]["result"][0], open(fn, "w")); return
        except Exception as e:
            time.sleep(1 + i)
    json.dump(None, open(fn, "w"))
if __name__ == "__main__":
    os.makedirs(f"{D}/px", exist_ok=True)
    if "frames" in sys.argv: frames()
    if "prices" in sys.argv:
        tick = json.load(open(f"{D}/tickers.json"))
        fund = {d["cik"] for d in json.load(open(f"{D}/fundamentals.json"))}
        ts = sorted({r[2] for r in tick["data"] if str(r[0]) in fund}) + ["SPY", "IWM", "RSP", "IJR", "QQQ"]
        with ThreadPoolExecutor(6) as ex: list(ex.map(px, ts))
        print("prices done", len(ts))
