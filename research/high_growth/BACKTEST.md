# Historical Factor Backtest (kept separate from paper results)

**Run date:** 2026-11-08. **Scripts:** `tools/fetch_history.py`, `tools/backtest.py`, `tools/backtest_robust.py`.
**Raw outputs:** `backtest_results.csv`, `backtest_summary.json`, `backtest_robustness.txt`.

## Question
Do the characteristics this strategy looks for actually predict next-year outperformance among US small and mid caps?
The characteristics tested:
- revenue growth;
- revenue acceleration;
- gross-margin improvement;
- FCF improvement;
- ROIC improvement;
- valuation.

## Design (fixed before seeing results; nothing was tuned)
- **Formation dates:** June 30 of each year, 2018–2025 (8 cohorts). The 12-month forward window runs June to June, so the last window ends June 2026.
- **Fundamentals:** SEC XBRL annual frames for CY(Y-1), CY(Y-2) and CY(Y-3).
  - Calendar-year filers have filed their 10-Ks by June 30, so the data was public at formation.
  - The SEC maps non-calendar fiscal years to the nearest calendar year. That leaves a small look-ahead risk for fiscal years ending
    January–March of year Y. Using a June formation date, rather than April, reduces it.
- **Universe:**
  - CY(Y-1) revenue ≥ $25M, with three years of revenue;
  - market cap $100M–$20B at formation;
  - financials (SIC 6000–6799) excluded.
  - Cohort sizes: 975 to 1,629 companies.
- **Market cap:** shares as reported at the time (10-K cover date) × the raw price at formation. The raw price undoes later splits.
- **Return:** total return including dividends (Yahoo adjusted close) over 12 months, equal-weighted. Single-stock returns are capped at
  +300% / −95% in the headline numbers; the un-capped figures are reported too.
- **Factors:**
  - g1 (revenue growth), accel (change in growth), gm_chg, fcf_chg (scaled by revenue), roic_chg, fcf_yield, ebit_yield, ev_s (lower is better).
  - **Composite:** equal-weight average percentile of six factors, specified in advance: g1, accel, gm_chg, fcf_chg, roic_chg, fcf_yield.
  - **hg_screen_rule:** the strategy's own hard filter — growth ≥ 15%, acceleration > 0, gross margin not falling, FCF positive and rising.
- **Tests:**
  - top-quintile return minus universe return;
  - top quintile minus bottom quintile;
  - rank information coefficient (IC) with its t-statistic across years;
  - comparison with SPY, IWM and RSP over the same June-to-June windows.

## Results (8 annual cohorts)
| Factor | Avg top-quintile − universe | Years top beat universe | Mean rank IC | IC t-stat | Avg top − SPY |
|---|---|---|---|---|---|
| Revenue growth (g1) | +0.5% | 5/8 | 0.004 | 0.15 | −1.3% |
| Revenue acceleration | +0.8% | 5/8 | 0.017 | 0.57 | −0.9% |
| Gross-margin change | +0.2% | 4/8 | −0.016 | −0.84 | −0.7% |
| FCF change | −0.1% | 5/8 | 0.020 | 0.97 | −1.9% |
| ROIC change | +0.9% | 5/8 | 0.007 | 0.26 | −0.4% |
| FCF yield | +2.0% | 5/8 | 0.033 | 0.63 | +0.2% |
| EBIT yield | +2.1% | 5/8 | 0.055 | 1.34 | +0.5% |
| Low EV/Sales | +3.0% | 5/8 | 0.015 | 0.25 | +1.2% |
| **Composite (pre-specified)** | **+0.8%** | **4/8** | 0.023 | 0.91 | **−1.0%** |
| **HG screen rule** | +1.7% | 4/8 | — | — | 0.0% |

Benchmarks, June-to-June total return:

| Benchmark | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|
| SPY | +10.1% | +7.3% | +40.9% | −10.6% | +19.4% | +24.5% | +14.9% | +22.2% |
| IWM | −3.5% | −6.6% | +61.9% | −25.4% | +12.4% | +9.8% | +7.6% | +40.7% |

Robustness checks, declared in advance:

| Check | Composite top − universe | Years it beat the universe |
|---|---|---|
| Small caps only ($100M–$2B) | −0.3% | 3/8 |
| Mid caps only ($2B–$20B) | +2.5% | 6/8 (subgroup found after the fact, so not evidence) |
| Un-capped returns | −0.3% | 4/8 (top minus bottom −7.9%; the bottom quintile holds the extreme winners) |
| Median returns | −0.5% | 4/8 |

## Conclusion
- **No statistically reliable edge.** No factor reaches |t| ≥ 2. The growth and quality-improvement factors are indistinguishable from zero.
- **Valuation is the only consistently positive group**, at about +2–3% a year, and it is still not significant over 8 cohorts.
- **Small caps showed no edge**, even though they are the strategy's priority segment.
- **Implication:** screening on "great recent numbers" alone does not beat the market, because public growth metrics are already priced.
  Any edge must come from what the screen cannot see:
  - verified qualitative judgment on durability and competitive position;
  - correctly identifying where market-implied expectations are wrong;
  - avoiding the errors the skeptic reviews keep catching.
  That cannot be backtested honestly, because there are no point-in-time human or AI judgments for the past. It has to be proven
  prospectively in the paper portfolio.
- **How the strategy changes:** valuation and expectations-gap discipline get more weight in judgment. Growth alone is treated as a
  necessary condition, not a signal.

## Known biases (they all push results in a stated direction)
1. **Survivorship bias.** Price history exists only for tickers listed today. Only 52–82% of eligible SEC filers per year have a price
   series (1,459/2,780 in 2018 up to 2,661/3,264 in 2025). Delisted companies — bankruptcies, but also acquisitions at a premium — are missing.
   - This inflates absolute returns for every group.
   - It likely flatters low-quality and distressed names most, so the true quality and value spreads may be somewhat larger.
   - It cannot be corrected without a paid delisting database such as CRSP.
2. **Ticker reuse and mapping.** CIK-to-ticker mapping uses today's ticker list. Renamed or reused tickers can mis-map a small number of rows.
3. **Short sample.** 8 annual cohorts, including the 2020–2021 boom-and-bust, give low statistical power. A real but small edge of about
   2% a year would not be detectable.
4. **No transaction costs** in the backtest. Equal weighting of small caps overstates achievable returns by perhaps 0.5–1% a year.
5. **Untestable items.** Customer adoption is not available as XBRL data, so it was not tested.
