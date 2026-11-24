"""Step 1.3: Monte Carlo over the box [-2,2]x[0,8]x[-2,2] confirms 16*pi."""

import numpy as np

rng = np.random.default_rng(23)
n = 400_000
xs = rng.uniform(-2, 2, n)
ys = rng.uniform(0, 8, n)
zs = rng.uniform(-2, 2, n)
hit = (xs**2 + zs**2 <= ys) & (ys <= 8.0 - xs**2 - zs**2)
estimate = 128.0 * hit.mean()
print("monte carlo volume:", round(float(estimate), 4))
print("target 16*pi:", round(16.0 * float(np.pi), 4))
assert abs(float(estimate) - 16.0 * np.pi) < 0.6
print("PASS 1.3")
