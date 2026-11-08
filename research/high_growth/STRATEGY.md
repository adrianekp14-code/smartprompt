# High-Growth (HG) Research Strategy

This is an add-on to the core discovery system (see `research/RUNBOOK.md`). It has the same ground rules: research only, no trading,
no fabricated data, no return probabilities, and no buy instructions.

## Goal
Find companies that could plausibly appreciate a lot over 5–10+ years, where there is a **defensible, evidence-based reason** to think the
market's implied expectations are too low. Being in a popular industry is not that reason.

## Pipeline
1. **Screen.** `python3 tools/hg_screen.py` produces `hg_screen_YYYY-MM-DD.csv`.
   - Stage A filters, using fundamentals only:
     - growth ≥ 15% (3-year CAGR, last fiscal year, or latest quarter year on year);
     - gross margin ≥ 35%, or rising;
     - 3-year share count increase ≤ 45%;
     - one-off revenue spikes excluded.
   - Stage B adds price, eight factors and a **reverse DCF**. The reverse DCF solves for the 10-year revenue CAGR implied by today's EV,
     using a 10% discount rate, 3% terminal growth, and an FCF margin that ramps over 5 years from current to target.
2. **Judgment triage.**
   - Remove growth bought through acquisitions, commodity and energy cycles, single-drug pharma, and screen artifacts.
   - Prefer essential infrastructure and component suppliers.
3. **Mispricing analysis.** Every serious candidate gets these six questions answered in its thesis:
   1. What does the market currently expect? Cover the reverse-DCF implied growth, guidance, and why the price moved.
   2. What could the company realistically achieve in 5–10 years?
   3. What evidence suggests expectations are too pessimistic?
   4. What could make earnings or cash flow grow faster than expected?
   5. What would prevent that growth? Keep "large TAM" separate from "will capture the TAM".
   6. Is the optimistic case already in the price?
4. **Independent skeptic review.** A separate agent tries to break the thesis. Its verdict and corrections are recorded verbatim in the thesis.
5. **Scoring** (below). Business quality and stock attractiveness are scored separately.
6. **Paper portfolio.** Every serious candidate is entered on the day it is identified. Candidates are never removed.
7. **Notification** only when the core notification threshold is met **and** the mispricing case survives the skeptic review.

## Scoring framework
Each dimension is scored 1–5 with a written reason. The scores are **not** combined into a probability and are **not** a forecast.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Business quality | Commodity product, low or erratic margins | Decent niche, average margins | Essential product, high and stable margins, recurring demand |
| Growth potential | Shrinking or ex-growth | ~10% durable growth | Credible 20%+ durable growth in a growing market |
| Competitive advantage | None visible | Some switching costs or certification | Hard-to-replicate technology, logistics, scale or regulatory position, with evidence of share gains |
| Financial strength | Funding need, high leverage | Manageable debt | Net cash (excluding customer advances), self-funding |
| Management quality | Governance or control red flags, poor allocation | Adequate | Record of beating guidance, disciplined allocation, aligned ownership |
| Valuation | Optimistic case priced in | Base case ≈ price | Base case well above price on conservative multiples |
| Downside risk (5 = low) | Large plausible permanent loss | Moderate | Bear case close to the current price |
| Evidence quality | Thin, unverified | Mostly verified, some gaps | Primary-source verified; skeptic review found no material errors |
| Uncertainty / data quality | Key numbers unverifiable or contested | Some unknowns | Clear data, few unknowns |

**Two separate verdicts per candidate:**
- **Business verdict:** high-quality, average, or low-quality business.
- **Stock verdict at today's price:** attractive, fair, or expensive. This is based on where the price sits against the bear, base and bull values.

A great business can be an unattractive stock, and the reverse.

## Lessons hard-coded from the first runs
- Compute excess cash **net of customer advances** (contract liabilities) and of raised capital earmarked for M&A.
- Use **trailing** EBIT and FCF. Annualize a single quarter only when backlog supports it, and label it if so.
  The 2026-11-08 screen used CY2025 annual FCF in the reverse DCF. That overstated TMDX's cash margin (22% vs ~6% TTM).
  Feed TTM FCF in when you rerun.
- Check stock splits against share-count dates, convertible debt, VIE consolidation, and acquisition-driven ("inorganic") growth.

## How success is measured (and how it could fail)
- **Prospective only.** Measured by `paper_portfolio.csv` and `paper_performance.csv`:
  - total return net of costs, including dividends;
  - compared with the benchmark on identical dates;
  - delistings handled as described in `tools/paper_portfolio.py`.
- **Primary metric.** Equal-weight excess return of every HG candidate ever entered, against SPY and against each candidate's assigned
  benchmark. Measured at 1, 3 and 5 years. Includes losers.
- **Secondary metrics.**
  - Hit rate (share beating the benchmark).
  - Scenario calibration: how often the price at 3 years lands below bear, between bear and bull, or above bull. If about 1/3 lands
    outside each tail, the scenarios are too narrow.
  - Notification precision: excess return of notified versus non-notified candidates.
- **Minimum evidence before claiming an edge:** at least 30 candidates and 3 years, with an excess return t-stat above 2.
  Until then, results are reported as "insufficient evidence", whatever their sign.
- **Kept separate:** historical backtests (`BACKTEST.md`) are never merged with paper results.
