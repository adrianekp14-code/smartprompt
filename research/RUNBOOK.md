# Equity Discovery Agent — Runbook

Every scheduled run follows this file. Research memory lives in `research/`; helper scripts in `tools/`.
Raw caches in `data_cache/` are regenerable and git-ignored.

## Ground rules
- Do research only. No apps, no dashboards, no trading, no brokerage access, no paid APIs/subscriptions.
- Never fabricate data. If a figure cannot be verified from a primary source, say "not verified".
- No return probabilities, no price targets presented as forecasts, no urgency language.
- Bear / base / bull values are scenario arithmetic with stated assumptions, not predictions.
- Never write that a notification was delivered unless the delivery channel confirmed it.

## Tools (all free; SEC requires a descriptive User-Agent and <10 req/s)
| Script | Purpose |
|---|---|
| `python3 tools/fetch_frames.py` | Cache SEC XBRL frames (edit period lists each quarter: add the newest CYyyyyQn / CYyyyy) |
| `cd tools && python3 screen.py` | Stage-1 fundamental screen → `data_cache/stage1.json` |
| `python3 tools/enrich.py` | Add Yahoo price + SEC SIC to stage-1 names |
| `python3 tools/rank.py data_cache/stage1_enriched.json N` | Valuation metrics + quantitative pre-score (triage only) |
| `python3 tools/lookup.py T1 T2 …` | Same metrics for an arbitrary ticker list |
| `python3 tools/company.py TICKER` | EDGAR snapshot: fiscal-year history, last quarters, balance sheet, recent filings, Form 4 counts |
| `python3 tools/filing_text.py URL kw1 kw2 …` | Pull text around keywords from a filing (backlog, customer, litigation …) |
| `python3 tools/triage.py` | Regenerate `discovered_companies.csv` / `rejected_companies.csv` from screens + `decisions.json` |

Known data pitfalls: pre-split share counts in `dei` (check Yahoo split events), convertible debt missing from screen debt,
revenue-tag changes, ADR ratios, acquisition-driven CAGR. Verify every number that goes into a notification against the filing.

## Cadence
**Daily (every run):**
1. For each ticker in `active_watchlist.csv`: check EDGAR `submissions` for new 8-K / 10-Q / 10-K / Form 4 / S-3 / 424B since `last_checked`.
   Read anything material (earnings, guidance, financing, executive changes, litigation, M&A). Web-search for news on each.
2. Update `active_watchlist.csv` (`last_checked`, `last_event`, `next_catalyst`) and append findings to `research_history.md`.
3. If an event changes a thesis checkpoint, update `investment_theses.md` (keep the old assumption, record the outcome).

**Weekly (Mondays):** run the full screen (fetch_frames → screen → enrich → rank), add new names to `discovered_companies.csv`,
review ≥20 not-yet-reviewed names by hand, promote/reject with reasons in `decisions.json`, deepen research on 1–2 shortlist names.

**Monthly (first Monday):** re-evaluate every watchlist thesis vs. latest fundamentals; explore one new industry/niche not yet covered;
compare scenario assumptions to actual results in `investment_theses.md` (“assumption tracking” table).

**Quarterly (first Monday of Feb/May/Aug/Nov):** after earnings season, refresh `fetch_frames.py` periods, rerun the whole screen,
update every deep-research thesis and its bear/base/bull arithmetic, score past assessments for accuracy.

## Notification threshold (all must hold)
1. Credible path to substantial long-term expansion (niche with growing demand, room to expand TAM).
2. Financial evidence supports it (growth + margins/FCF, or a verified path to them).
3. Interesting competitive position (switching costs, certification, IP, scale in a niche).
4. Valuation deserves investigation (base case ≥ current price on conservative multiples; bear case loss understood).
5. Risks identified and disclosed; a separate skeptical review (independent agent) did not reject the thesis.
6. Primary-source verification done (latest 10-K/10-Q/8-K read; numbers in the note match filings).

Incomplete-but-interesting → `active_watchlist.csv` + `investment_theses.md`, not a notification.
Re-notify a company only when its research status materially changes; log every notification in `notifications_sent.md`
with the delivery channel and whether delivery was confirmed.

## Notification format
Write to `research/notifications/YYYY-MM-DD-TICKER.md` using the sections: COMPANY, WHY IT IS INTERESTING, FINANCIALS,
VALUATION (bear/base/bull + assumptions), RISKS (top 5, strongest counter-argument, invalidation triggers), SOURCES (direct SEC links),
FINAL ASSESSMENT. Then deliver via the configured channel(s) and record the result in `notifications_sent.md`.

## Scores (1–5, separate, never combined into a return probability)
Business quality · Growth potential · Financial strength · Competitive advantage · Management quality · Valuation attractiveness ·
Downside risk (5 = low risk) · Evidence quality.

## High-Growth (HG) strategy add-on — see `research/high_growth/STRATEGY.md`
| Script | Purpose |
|---|---|
| `python3 tools/hg_screen.py` | HG screen + reverse DCF → `research/high_growth/hg_screen_DATE.csv` (needs `screen.py` run first) |
| `python3 tools/reverse_dcf.py EV REV m0 m1` | Market-implied 10-year revenue CAGR for one company |
| `python3 tools/paper_portfolio.py` | Fill entry prices (first close after identification), mark all paper positions, log performance |
| `python3 tools/fetch_history.py frames prices` + `python3 tools/backtest.py` + `python3 tools/backtest_robust.py` | Re-run historical backtest (annually, after June) |
| `python3 tools/dca_model.py` | Educational $50/2-week contribution model |

- **Daily:** run `paper_portfolio.py`. Check HG candidates' new filings the same way as the core watchlist.
- **Weekly:** run `hg_screen.py`. Review ≥ 10 new names by hand. Any name that reaches "serious candidate" gets:
  - the six mispricing questions answered;
  - an independent skeptic agent review;
  - its scores recorded in `research/high_growth/hg_theses.md`;
  - a row in `paper_portfolio.csv` the same day. Rows are never deleted. A closed thesis gets `status=closed` and an `exit_date`.
- **Quarterly:**
  - re-score every HG candidate;
  - record scenario calibration (price vs bear/base/bull);
  - update `performance_log.csv` analysis in `hg_theses.md` ("Strategy scorecard").
- **Annually (July):** extend and re-run the backtest with the new cohort. Never tune factors to improve history.
