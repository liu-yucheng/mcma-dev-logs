"""Step 1.3: a Monte Carlo pass over the box confirms 16*pi/3 and volume 2*pi."""

import numpy as np

rng = np.random.default_rng(7)
n = 400_000
xs = rng.uniform(0, 4, n)
ys = rng.uniform(-1, 1, n)
zs = rng.uniform(-1, 1, n)
hit = 4.0 * ys**2 + 4.0 * zs**2 <= xs
estimate = 16.0 * xs[hit].sum() / n
volume = 16.0 * hit.sum() / n
print("monte carlo integral:", round(float(estimate), 4))
print("monte carlo volume:", round(float(volume), 4), "target", round(2 * float(np.pi), 4))
assert abs(estimate - 16.0 * np.pi / 3.0) < 0.2
assert abs(volume - 2.0 * np.pi) < 0.05
print("PASS 1.3")
