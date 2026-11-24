"""A Monte Carlo estimate of the volume lands within 4 standard errors of 20/3."""
import sympy as sp
import numpy as np
rng = np.random.default_rng(28)
N = 200000
xs = rng.random(N) * 4.0
ys = rng.random(N) * 2.0
zs = rng.random(N) * 2.0
hits = float(np.mean((xs <= 4 - ys**2) & (zs <= 2 - ys)))
V_mc = hits * 16.0
x, z, y = sp.symbols("x z y")
V_exact = float(sp.integrate(sp.integrate(sp.integrate(1, (x, 0, 4 - y**2)), (z, 0, 2 - y)), (y, 0, 2)))
se = 16.0 * np.sqrt(hits * (1 - hits) / N)
print(f"N={N} hit_ratio={hits:.4f} V_mc={V_mc:.4f} se={se:.5f} exact={V_exact}")
assert abs(V_mc - V_exact) < 4 * se
print("PASS 1.3")
