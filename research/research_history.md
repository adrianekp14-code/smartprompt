# Research History

Log of every research run: what was done, what changed, and what was learned. Newest first.

---

## 2026-11-23 (Monday) — Daily run + weekly screen
- Filings since 11-21: none on any watchlist/paper ticker.
- Owned (closes 11-23): VOO $663.91 (+4.5%), IESC $170.92 (+9.5%), AEIS $214.07 (+12.6%) — broad rebound after the 11-20 selloff.
- Weekly screen: refreshed CY2026Q3 frames; stage-1 598; HG screen → research/high_growth/hg_screen_2026-11-23.csv. Hand-reviewed 23 previously unreviewed names (decisions.json): 20 rejected (commodity, acquisition-driven, consumer, mega/well-followed, dilution); **NPKI** and **MKSI** → watch. NPKI (composite matting for utility/grid sites) queued for deep research next run — screen figures are NOT yet verified.
- Paper portfolio: rate limits left 5 of 9 unmarked today (statuses unchanged).
- Notifications: none — threshold not met.

---

## 2026-11-20 — Daily run
- **IESC FY26 10-K + Q4 8-K filed (FACT, see investment_theses.md IESC update 2026-11-20):** Q4 revenue +55%, op income +108%, C&I margin 27.0%, RPO $3.48B, CFO $364.5M; 350k shares bought back at $248 after year-end; +$350M authorization. DBM economics deferred to Q1 FY27 10-Q → held notification stays held (3 of 4 criteria met). 8-K Item 5.02 = executive bonuses/incentive plans (no departures).
- **Market:** chip stocks fell sharply (SMH −10.6%, KLIC −11.2%, CAMT −8.8%; AEIS ≈ −10% to $190.18); VOO −3.4%; IESC −6.5% to $156.06. Cause of the selloff: MISSING (one search found no Nov-20 coverage). No AEIS company filings.
- LMAT Form 4 (not read in detail; insider transaction).
- Paper portfolio (marks 11-20; TMDX, PSIX unmarked due to rate limits): HG EW −16.5% vs −17.9% benchmarks; CORE EW −6.7% vs −8.3%.
- Notifications: none sent (IESC held).

---

## 2026-11-19 (scheduled, 4:41 PM CT) — Daily run
- Filings since last run: KLIC FY26 10-K (results already covered via 8-K; not re-read in full); PSIX 8-K 5.02 (FACT): CFO Xun (Ken) Li resigning effective 2026-11-27 (first disclosed in 8-K of 2026-11-06, missed by the 11-08/11-13 runs); Robert Losier (Anchor Resource Management consultant) interim CFO from 11-28. Second senior change in 2026 after the CEO change → governance score stays 1; watchlist unchanged.
- Owned: VOO $658.01 (−2.0% day), IESC $166.90 (+0.5%), AEIS $212.24 (−1.5%) — closes 2026-11-19. No IESC/AEIS filings. IESC 10-K still pending.
- Tool fix: Yahoo rate limits had again marked 8 positions "data-ended"; changes discarded, tools/paper_portfolio.py now retries with backoff and never changes status on a fetch failure. 3 positions (MPTI, BKTI, PSIX) unmarked today; performance_log rows for 11-19 with n<5/9 are partial.
- Notifications: none — threshold not met.

---

## 2026-11-19 — Daily run (first in-session run; covers filings since 2026-11-17)
- Paper portfolio (entry 2026-11-09 close, marks 2026-11-18 close, net of costs): HG EW −2.2% vs benchmarks −5.0% (3 of 4 ahead); CORE EW −3.7% vs −3.6% (2 of 5 ahead). Seven trading days: no meaning yet.
- KLIC 8-K (Q4 FY26, FACT): revenue $410.3M (> $355M invalidation level → not triggered); GM 47.8%; NI $73.2M; CFO only $25.4M, adj. FCF $14.6M (cash conversion weak); Q1 FY27 guide $410M ±$20M (flat q/q); cash+ST inv $517.0M. Stance unchanged (expensive on mid-cycle).
- AEIS Form 4 (FACT): Lanesha Minnix sold 2,000 sh at $208.73 (~$0.42M); 10b5-1 status not stated in filing text parsed. Small; no thesis change.
- PPIH 8-K 1.01 (FACT): closed 51% of Welspun Special Coating (India) JV via Qatar subsidiary. Immaterial to thesis.
- RDCM, ESP: Form 4/144 only. POWL 10-K already covered. IESC: still no 10-K.
- Notifications: none — threshold not met.

---

## 2026-11-19 — Daily runs moved into the owner's chat session
Owner approved. New schedule "Daily equity research run (in owner's chat)" (weekdays 4:41 PM America/Chicago) fires into the original analyst session, which can push. Old routine "Equity discovery agent — daily research run" disabled (kept for history).

---

## 2026-11-18 — Scheduled-run push failures; NVDA review; POWL recovered
- Daily routine runs on 11-13, 11-17, 11-18 (manual test) and 11-18 (scheduled) all completed research but were refused by GitHub (403: repo not in the routine's authorized sources). Owner edited the routine; manual test and scheduled run still failed. Findings recovered here from run transcripts (11-13 earlier; POWL 11-17 now).
- NVDA post-earnings review: see research/reviews/2026-11-18-NVDA.md — does not pass (CEO resignation, board investigation, delayed 10-Q).
- POWL FY26: both checkpoints met; still watchlist (base < price).

---

## 2026-11-13 — Daily run (Friday)
Note: no runs are recorded for 2026-11-09…11-12 (only two ad-hoc commits: AEIS correction, NVDA prediction). This run covers filings since 2026-11-08.

**Paper portfolio** (marks = Yahoo close 2026-11-13T21:00Z; entry = first close after 2026-11-08, i.e. 2026-11-09). All 9 entries now filled.
CORE (5): EW net −2.4% vs benchmarks −1.1% (3 of 5 ahead). HG (4): EW net −1.6% vs −0.3% (2 of 4 ahead). Worst: BKTI −12.3% (guide cut). Four days of data: no meaning.
Tool bug fixed (rate-limit 429 had been recorded as "data-ended").

**Filings reviewed (EDGAR submissions, 23 tickers):**
- MPTI 10-Q/8-K (Q3): both checkpoints met (backlog $84.9M, GM 44.5%). NI growth mostly related-party interest income; op income flat y/y.
- BKTI 10-Q/8-K×2 (Q3): FY26 guide cut ($90M → ~$85M revenue; GAAP EPS >$3.15 → $2.40); backlog $6.3M; buyback auth +$5M. Correction: GAAP TTM FCF $11.8M, not $19M.
- PSIX 8-K 1.01: fixed-price HCE engine supply 2027–28 (~$121.9M purchases, 10% advances). Form 4 (CFO) = option exercise/tax withholding.
- CAMT Q3 6-K (from 11-04, carried over): checkpoints met; $877.1M cash/investments now FACT; convert carrying $489.2M; goodwill +$38M (acquisition terms MISSING).
- TGLS 10-Q + 8-K/A: margin collapse; earnings-release net income corrected −$6.0M; ~14x TTM EBIT, not ~9x → under review.
- LMB 10-Q (carried over), ELMD 10-Q, ESP 10-Q, RDCM 6-K, PPIH 8-K (51% of an Indian coating JV): summarised in watchlist `last_event`; no thesis change.
- Form 4s: USLM CEO sold 42,000 sh (~$5.0M) on 11-10; OSPN director/CFO/GC sales (~37k sh); AEIS EVP 10b5-1 sale (3,238 sh); TMDX director 4,059 sh. Governance note for USLM.
- IESC: no 10-K yet (13F-HR only). FY26 Q4 date unconfirmed (aggregators REPORTED Nov 20 or Dec 9). Held notification stays held.
- No filings: POWL, AGX, LMAT, AZZ, PLAB, UFPT, NSSC, KLIC.

**News (REPORTED):** POWL reports FY26 Q4 after close Mon 2026-11-16 (GlobeNewswire via finviz). TGLS mgmt calls Q3 the margin trough, Q4 GM guide 38–39%, third straight EBITDA guide cut (finviz/stockstory). BKTI Q2 guide confirmed from the primary filing.

**Checkpoints tested:** MPTI backlog/GM → met. BKTI guide ≥ $85M → met at the boundary (EPS guide −24%). CAMT 2027 ≥ $800M, GM ≥ 50% → met. Others not yet due.

**Corrections:** 3 rows (BKTI FCF, TGLS valuation, paper-portfolio tool).

**Notifications:** none. Threshold not met; IESC send criteria await the FY26 10-K. No candidate reached "survives" in a disproof review this run (none run: no new high-conviction candidate).

**Next run:** POWL FY26 Q4 (11-16), IESC 10-K / earnings schedule, KLIC FY26 Q4 (invalidation if Q4 revenue < $355M). Monday 11-16 = weekly screen (not first Monday of the month).

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
