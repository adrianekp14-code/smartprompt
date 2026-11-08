# $50 every two weeks for 24 months — educational model

Total contributed: **$2,600** (52 contributions). Not investment advice; no brokerage access.

## A. Constant annual return scenarios (final balance after 24 months)

| Annual return | Final balance | Gain/loss vs. $2,600 |
|---|---|---|
| -40% | $1,645 | -955 |
| -25% | $1,988 | -612 |
| -15% | $2,227 | -373 |
| -5% | $2,474 | -126 |
| +0% | $2,600 | +0 |
| +5% | $2,729 | +129 |
| +7% | $2,781 | +181 |
| +10% | $2,859 | +259 |
| +15% | $2,992 | +392 |
| +25% | $3,263 | +663 |

A one-time crash matters less early (little invested) and more late: a −30% drop in month 23 on a ~$2,500 balance costs ≈ $750.

## B. Monte Carlo (10,000 paths, fat-tailed shocks, seeded)

Assumptions (annual, after costs): Broad-market index (e.g., total-market ETF, 0.03% fee): mean 6.5%, vol 16%; Quality-growth stock selection (10-20 stocks): mean 6.0%, vol 21%; Higher-risk small-company research (5-10 stocks): mean 5.0%, vol 34%. Correlations: index–quality 0.85, index–small 0.65, quality–small 0.65. Stock-selection sleeves are given **no** assumed edge (the backtest found none).

| Approach | 5th pct | 25th | Median | 75th | 95th | P(final < $2,600) | P(underperform index) |
|---|---|---|---|---|---|---|---|
| Broad-market index (e.g., total-market ETF, 0.03% fee) | $2,236 | $2,519 | $2,746 | $2,990 | $3,412 | 33% | — |
| Quality-growth stock selection (10-20 stocks) | $2,070 | $2,425 | $2,712 | $3,038 | $3,599 | 40% | 56% |
| Higher-risk small-company research (5-10 stocks) | $1,708 | $2,192 | $2,613 | $3,146 | $4,173 | 49% | 59% |
| Diversified combination (70% index / 20% quality-growth / 10% small-co) | $2,183 | $2,490 | $2,733 | $3,004 | $3,460 | 36% | 56% |

**Reading this:** over 24 months the contribution total ($2,600) dominates; return assumptions move the median by only ~$100–200,
but the spread (5th–95th percentile) is much wider for concentrated small-company portfolios. Concentration raises the odds of both large gains
and of trailing the index; without a demonstrated edge, the extra volatility is a cost, not a benefit. The paper portfolio is how an edge would have to be shown.
