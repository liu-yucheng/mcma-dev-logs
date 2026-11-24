"""Step 1.1: rho stays in [4/5, 6/5], so the surface is a star shape about the origin."""

import numpy as np
import sympy as sp

m, n = 6, 5
th, ph = sp.symbols("theta phi", positive=True)
a = sp.Rational(1, 5)
tvals = [sp.sin(m * v) for v in sp.solveset(sp.cos(m * th), th, sp.Interval(0, 2 * sp.pi))]
pvals = [sp.sin(n * v) for v in sp.solveset(sp.cos(n * ph), ph, sp.Interval(0, sp.pi))]
tmin, tmax = min(tvals), max(tvals)
pmin, pmax = min(pvals), max(pvals)
lo, hi = 1 + a * tmin * pmax, 1 + a * tmax * pmax
print("sine bounds: theta sine in [%s, %s], phi sine in [%s, %s]" % (tmin, tmax, pmin, pmax))
print("rho min (exact):", lo, "=", float(lo))
print("rho max (exact):", hi, "=", float(hi))

rng = np.random.default_rng(3)
N = 200000
t = rng.uniform(0.0, 2.0 * np.pi, N)
p = rng.uniform(0.0, np.pi, N)
rv = 1.0 + 0.2 * np.sin(6.0 * t) * np.sin(5.0 * p)
print("sample min rho:", round(float(rv.min()), 6), "sample max rho:", round(float(rv.max()), 6))
assert abs(float(rv.max()) - float(hi)) < 0.02 and abs(float(rv.min()) - float(lo)) < 0.02
print("PASS 1.1")
