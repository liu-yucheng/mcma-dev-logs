"""Step 1.3: Monte Carlo over the box [0,1]x[0,3]x[0,3] confirms 27/8."""

import numpy as np
import sympy as sp

rng = np.random.default_rng(11)
n = 300_000
xs = rng.uniform(0, 1, n)
ys = rng.uniform(0, 3, n)
zs = rng.uniform(0, 3, n)
hit = (ys**2 + zs**2 <= 9.0) & (xs <= ys / 3.0)
estimate = 9.0 * (zs * hit).sum() / n
target = sp.Rational(27, 8)
print("monte carlo value:", round(float(estimate), 4))
print("exact value:", float(target))
assert abs(float(estimate) - float(target)) < 0.1
print("PASS 1.3")
