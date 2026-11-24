"""Step 3: a Monte Carlo volume estimate from the region's inequalities agrees with the exact value 2/3."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
Vexact = sp.integrate(sp.integrate(sp.integrate(sp.Integer(1), (y, 0, 2 - 2 * z)), (z, 0, 1 - x)), (x, 0, 1))
print("exact V =", Vexact)
N = 400000
print("N =", N)
rng = np.random.default_rng(20261124)
P = rng.random((N, 3))
X, Y, Z = P[:, 0], 2 * P[:, 1], P[:, 2]
mask = (X >= 0) & (X <= 1) & (Z >= 0) & (Z <= 1 - X) & (Y >= 0) & (Y <= 2 - 2 * Z)
Vmc = float(mask.mean()) * 2.0
se = 2.0 * float(np.sqrt(mask.mean() * (1 - mask.mean()) / N))
print("MC V =", Vmc, " SE =", se)
assert abs(Vmc - float(Vexact)) < 6 * se + 0.002
print("PASS 1.3")
