"""Educational model: $50 every two weeks for 24 months (52 contributions = $2,600). Not advice; assumptions are deliberately modest.
Part A: deterministic constant-annual-return scenarios. Part B: Monte Carlo (seeded) with stated means/vols/correlations, Student-t shocks (fat tails).
No strategy is assumed to beat the index on average: the backtest found no reliable edge, so stock-selection sleeves get the SAME or lower
expected return with higher volatility and costs."""
import random, math, statistics, json, os, sys
N, C = 52, 50.0
def deterministic(annual):
    r = (1 + annual) ** (1 / 26) - 1; bal = 0.0
    for _ in range(N): bal = bal * (1 + r) + C
    return bal
SLEEVES = {  # annual expected return (after fees/costs), annual volatility
    "Broad-market index (e.g., total-market ETF, 0.03% fee)": (0.065, 0.16),
    "Quality-growth stock selection (10-20 stocks)": (0.060, 0.21),
    "Higher-risk small-company research (5-10 stocks)": (0.050, 0.34),
}
CORR = [[1.0, 0.85, 0.65], [0.85, 1.0, 0.65], [0.65, 0.65, 1.0]]
MIX = {"Diversified combination (70% index / 20% quality-growth / 10% small-co)": (0.70, 0.20, 0.10)}
def chol(A):
    n = len(A); Lm = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(Lm[i][k] * Lm[j][k] for k in range(j))
            Lm[i][j] = math.sqrt(A[i][i] - s) if i == j else (A[i][j] - s) / Lm[j][j]
    return Lm
def tshock(rng, dfree=4):
    z = rng.gauss(0, 1); chi = sum(rng.gauss(0, 1) ** 2 for _ in range(dfree))
    return z / math.sqrt(chi / dfree) * math.sqrt((dfree - 2) / dfree)
def mc(paths=10000, seed=42):
    rng = random.Random(seed); Lm = chol(CORR); names = list(SLEEVES); mus = [SLEEVES[n][0] for n in names]; vols = [SLEEVES[n][1] for n in names]
    finals = {n: [] for n in names + list(MIX)}; under = {n: 0 for n in names[1:] + list(MIX)}
    for _ in range(paths):
        bal = [0.0] * 3; mixbal = {m: 0.0 for m in MIX}
        for _ in range(N):
            e = [tshock(rng) for _ in range(3)]; z = [sum(Lm[i][k] * e[k] for k in range(3)) for i in range(3)]
            r = [math.exp((mus[i] - vols[i] ** 2 / 2) / 26 + vols[i] / math.sqrt(26) * z[i]) - 1 for i in range(3)]
            bal = [b * (1 + ri) + C for b, ri in zip(bal, r)]
            for m, wts in MIX.items(): mixbal[m] = mixbal[m] * (1 + sum(w * ri for w, ri in zip(wts, r))) + C
        for n, b in zip(names, bal): finals[n].append(b)
        for m in MIX: finals[m].append(mixbal[m])
        for n, b in zip(names[1:], bal[1:]): under[n] += b < bal[0]
        for m in MIX: under[m] += mixbal[m] < bal[0]
    return finals, {k: v / paths for k, v in under.items()}
if __name__ == "__main__":
    out = ["# $50 every two weeks for 24 months — educational model\n", f"Total contributed: **${N*C:,.0f}** (52 contributions). Not investment advice; no brokerage access.\n",
           "## A. Constant annual return scenarios (final balance after 24 months)\n", "| Annual return | Final balance | Gain/loss vs. $2,600 |", "|---|---|---|"]
    for a in [-0.40, -0.25, -0.15, -0.05, 0.0, 0.05, 0.07, 0.10, 0.15, 0.25]:
        b = deterministic(a); out.append(f"| {a:+.0%} | ${b:,.0f} | {b-N*C:+,.0f} |")
    out += ["\nA one-time crash matters less early (little invested) and more late: a −30% drop in month 23 on a ~$2,500 balance costs ≈ $750.\n",
            "## B. Monte Carlo (10,000 paths, fat-tailed shocks, seeded)\n", "Assumptions (annual, after costs): " + "; ".join(f"{k}: mean {v[0]:.1%}, vol {v[1]:.0%}" for k, v in SLEEVES.items()) +
            ". Correlations: index–quality 0.85, index–small 0.65, quality–small 0.65. Stock-selection sleeves are given **no** assumed edge (the backtest found none).\n",
            "| Approach | 5th pct | 25th | Median | 75th | 95th | P(final < $2,600) | P(underperform index) |", "|---|---|---|---|---|---|---|---|"]
    finals, under = mc()
    for n, f in finals.items():
        f = sorted(f); q = lambda p: f[int(p * (len(f) - 1))]
        out.append(f"| {n} | ${q(.05):,.0f} | ${q(.25):,.0f} | ${q(.5):,.0f} | ${q(.75):,.0f} | ${q(.95):,.0f} | {sum(x < N*C for x in f)/len(f):.0%} | {('—' if n.startswith('Broad') else f'{under[n]:.0%}')} |")
    out += ["\n**Reading this:** over 24 months the contribution total ($2,600) dominates; return assumptions move the median by only ~$100–200,",
            "but the spread (5th–95th percentile) is much wider for concentrated small-company portfolios. Concentration raises the odds of both large gains",
            "and of trailing the index; without a demonstrated edge, the extra volatility is a cost, not a benefit. The paper portfolio is how an edge would have to be shown.\n"]
    p = os.path.join(os.path.dirname(__file__), "..", "research", "high_growth", "contribution_model.md"); open(p, "w").write("\n".join(out)); print("\n".join(out))
