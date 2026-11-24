"""Step 1.1: the silo volume is the cylinder volume plus the hemisphere volume."""

import numpy as np
import sympy as sp

radius, height = sp.Integer(3), sp.Integer(10)
exact = sp.pi * radius**2 * height + sp.Rational(2, 3) * sp.pi * radius**3

rng = np.random.default_rng(7)
N = 200000
x = rng.uniform(-3.0, 3.0, N)
y = rng.uniform(-3.0, 3.0, N)
z = rng.uniform(0.0, 13.0, N)
in_cyl = (x**2 + y**2 <= 9) & (z <= 10)
in_hemi = (x**2 + y**2 + (z - 10)**2 <= 9) & (z >= 10)
box = 6.0 * 6.0 * 13.0
frac = float((in_cyl | in_hemi).mean())
mc = frac * box
se = float(np.sqrt(frac * (1.0 - frac) / N)) * box
print("exact volume:", sp.simplify(exact), "=", round(float(exact), 4))
print("monte carlo volume:", round(mc, 4), "standard error:", round(se, 4))
assert abs(mc - float(exact)) < 5.0 * se
print("PASS 1.1")
