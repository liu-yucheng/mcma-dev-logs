"""Step 1.1: with f = 1 the x-first order gives volume 18*4**(1/3)/7 for E."""

import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
inner = sp.integrate((4 - y) / 2, (y, x ** 3, 4))
volume = sp.simplify(sp.integrate(inner, (x, 0, 4 ** sp.Rational(1, 3))))
print("exact volume:", volume, "=", float(volume))

rng = np.random.default_rng(7)
n = 200000
sx = rng.uniform(0, 4 ** (1 / 3), n)
sy = rng.uniform(0, 4, n)
sz = rng.uniform(0, 2, n)
inside = (sy >= sx ** 3) & (sz <= (4 - sy) / 2)
box = float(4 ** (1 / 3)) * 4.0 * 2.0
print("mc volume:", round(box * inside.mean(), 4))
assert abs(box * inside.mean() - float(volume)) < 0.05
print("PASS 1.1")
