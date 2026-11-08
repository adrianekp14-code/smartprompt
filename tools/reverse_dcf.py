"""Market-implied growth ("what does the market expect?").
Solves for the 10-year revenue CAGR that makes PV(FCF) = EV, given a steady-state FCF margin.
Assumptions (explicit, editable): discount 10%, terminal growth 3%, FCF margin ramps linearly from current to target over 5y.
python3 tools/reverse_dcf.py EV_musd TTM_REV_musd current_fcf_margin target_fcf_margin"""
import sys
def pv(ev_rev, g, m0, m1, r=0.10, tg=0.03, years=10):
    rev, tot = 1.0, 0.0
    for y in range(1, years + 1):
        rev *= 1 + g; m = m0 + (m1 - m0) * min(y, 5) / 5
        tot += rev * m / (1 + r) ** y
    tv = rev * (1 + tg) * m1 / (r - tg) / (1 + r) ** years
    return tot + tv
def implied_growth(ev, rev, m0, m1, **kw):
    target = ev / rev; lo, hi = -0.3, 1.0
    if pv(None, hi, m0, m1, **kw) < target: return None   # needs >100%/yr
    for _ in range(80):
        mid = (lo + hi) / 2
        if pv(None, mid, m0, m1, **kw) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
if __name__ == "__main__":
    ev, rev, m0, m1 = map(float, sys.argv[1:5])
    g = implied_growth(ev, rev, m0, m1)
    print(f"EV/Sales {ev/rev:.2f}; FCF margin {m0:.0%}->{m1:.0%}: market-implied 10y revenue CAGR = {g:.1%}" if g is not None else "Implied growth >100%/yr")
