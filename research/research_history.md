# Research History

Log of every research run: what was done, what changed, and what was learned. Newest first.

---

## 2026-11-08 — High-Growth strategy added (run #2)
- Added: `tools/hg_screen.py` (755 stage-A → 566 ranked), `tools/reverse_dcf.py`, `tools/backtest.py` (+robustness), `tools/paper_portfolio.py`, `tools/dca_model.py`;
  docs in `research/high_growth/` (STRATEGY, BACKTEST, hg_theses, contribution_model, paper_portfolio.csv).
- Backtest 2018–2025 (8 cohorts, 975–1,629 names): no factor significant (|t|<2); growth/quality-change ≈ 0; valuation +2–3%/yr (n.s.); small caps no edge. Survivorship bias documented.
- HG deep dives (each with independent skeptic): AEIS, CAMT, TMDX, KLIC — all "survive with major caveats". Ranking: AEIS > IESC > CAMT > TMDX > KLIC.
- Screen error caught by skeptic: reverse DCF used CY2025 FCF (TMDX 22%) instead of TTM (~6%) — fix: feed TTM FCF.
- Paper portfolio: 9 rows (4 HG + 5 CORE), entry = first close after 2026-11-08.
- Scheduled task created: weekdays 22:41 UTC, fresh cloud session, push notification on completion (delivery not confirmed back to the session).
- Notifications this run: none (threshold not met).

---

## 2026-11-08 — Initial discovery scan (run #1)

### Data sources actually used
| Source | Access | Used for |
|---|---|---|
| SEC EDGAR XBRL `frames` API (data.sec.gov) | Free, no key | Cross-sectional fundamentals for every US-GAAP filer (124 datasets: revenue CY2021–25, quarterly CY2025–26, margins, cash flow, SBC, diluted shares, balance sheet) |
| SEC `companyfacts` / `submissions` APIs | Free, no key | Per-company multi-year history, SIC codes, filing lists, Form 4 counts |
| SEC EDGAR filing documents (www.sec.gov/Archives) | Free | 10-K/10-Q/8-K text: backlog, customer concentration, litigation, MD&A |
| Yahoo Finance chart API (query1.finance.yahoo.com) | Free, unofficial | Last price (timestamped), 52-week range, splits |
| Web search | Built-in | News, negative developments, sector context |

Not available: paid data (FactSet/Bloomberg/S&P), consensus estimates, short interest, transcripts behind paywalls, IFRS-only foreign filers in the XBRL screen (20-F IFRS filers are invisible to the us-gaap frames).

### Funnel
1. **Universe:** 10,000+ SEC tickers → 3,073 US-listed companies with ≥$25M CY2025 revenue in XBRL.
2. **Stage-1 fundamental screen:** growth ≥10% 3y CAGR (or latest-quarter y/y ≥20%), gross margin ≥25% (when reported), operating profit positive (annual or latest quarter) → **595**.
3. **Enrichment:** price + SIC for all 595; financials excluded; market cap ≥$80M → **509 ranked**.
4. **Supplementary list:** 73 niche industrial/tech/semicap/aerospace/water names that stage-1 dropped (cyclical dip, low-GM contractors) → **59 ranked**.
5. **Triage:** 561 companies recorded in `discovered_companies.csv`; ~142 reviewed by hand with a written reason (`decisions.json`); 377 rejected by rule or by hand.
6. **Shortlist:** 20 companies. **Deep research:** 5 (POWL, IESC, BKTI, MPTI, PSIX), each challenged by an independent skeptic review.

### Market context found
- AI/data-center construction & electrical names peaked May–June 2026 and fell 50–75% (STRL −75%, AGX −65%, IESC −60%, POWL −59%, AAON −61%). Accelerant: Nov 4–5, 2026 post-midterm selloff on fears of data-center restrictions after Democrats won Congress (Motley Fool, Nov 4 2026). Reported backlogs largely held up (e.g., FIX backlog $17.8B vs $9.4B a year ago).
- Implication: quality electrical-infrastructure suppliers became materially cheaper; but customer concentration in a handful of hyperscaler projects is now a first-order risk.

### Data-quality lessons (fix before trusting screen numbers)
- `dei:EntityCommonStockSharesOutstanding` can be **pre-split**: IESC (2:1 on 2026-08-24) was understated 50% in the screen. Always check Yahoo split events after the share-count date.
- Screen `debt` misses convertible notes for some filers (CAMT) — verify on the balance sheet.
- Revenue tag changes (e.g., BKTI moved to `RevenueFromContractWithCustomerIncludingAssessedTax`) — take max across tags.
- Annualizing a single strong quarter misleads (PSIX: 5x "annualized" vs ~9x trailing EBIT). Use trailing figures unless backlog supports a run-rate.
- ADR share counts and acquisitions create absurd dilution/CAGR figures (INOD, BMI, ONC) — treat >100% values as artifacts until checked.

### Deep research outcomes (each challenged by an independent skeptic agent)
| Ticker | Skeptic verdict | Key corrections the skeptic forced | Decision |
|---|---|---|---|
| IESC | survives w/ major caveats | Jun-26 qtr flattered by short jobs + $26M securities gain; DBM debt-funded; drawdown began post-DBM; insiders sold May–Jun | Notification prepared, HELD for FY26 10-K |
| POWL | survives w/ major caveats | "Net cash" is ~55% customer advances (excess ≈ $280M) → ~20x EBIT; margins 2.5x prior peak; ~$800M of 9M bookings data center | Watchlist; base case < price |
| MPTI | survives w/ major caveats | Cash from ~49% dilution, not operations; M&A-linked pay; top-2 customers 51%; CEO is Cameron Pforr (not Ferrantino); NYSE American | Watchlist |
| BKTI | survives w/ major caveats | Oct-8-2026 roof collapse at only plant; backlog $3.2M; 2025 EBIT helped by capitalized R&D; diluted shares 4.05M | Watchlist (event) |
| PSIX | survives w/ major caveats | "5x EBIT" was annualized best quarter → ~9x trailing; tariff refund; DC products lower margin; Weichai control | Watchlist |

Lesson: my first-pass theses overstated cash (customer advances, raised capital), annualized peak quarters, and misattributed drawdowns to a single macro event. Future theses must compute excess cash net of contract liabilities and use trailing EBIT.

### Prior assumptions to test next run
- (See `investment_theses.md` — each thesis lists measurable checkpoints with dates.)
