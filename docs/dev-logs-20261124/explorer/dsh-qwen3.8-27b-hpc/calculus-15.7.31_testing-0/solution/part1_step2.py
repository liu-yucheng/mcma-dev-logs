"""Step 1.2: all six iterated orders of f = 1 give the exact volume 18*4**(1/3)/7."""

import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", positive=True)
r3 = 4 ** sp.Rational(1, 3)
cbrt = lambda t: t ** sp.Rational(1, 3)
orders = [
    sp.integrate(sp.integrate(sp.integrate(1, (z, 0, (4 - y) / 2)), (y, x ** 3, 4)), (x, 0, r3)),
    sp.integrate(sp.integrate(sp.integrate(1, (y, x ** 3, 4 - 2 * z)), (z, 0, (4 - x ** 3) / 2)), (x, 0, r3)),
    sp.integrate(sp.integrate(sp.integrate(1, (z, 0, (4 - y) / 2)), (x, 0, cbrt(y))), (y, 0, 4)),
    sp.integrate(sp.integrate(sp.integrate(1, (x, 0, cbrt(y))), (z, 0, (4 - y) / 2)), (y, 0, 4)),
    sp.integrate(sp.integrate(sp.integrate(1, (x, 0, cbrt(y))), (y, 0, 4 - 2 * z)), (z, 0, 2)),
    sp.integrate(sp.integrate(sp.integrate(1, (y, x ** 3, 4 - 2 * z)), (x, 0, cbrt(4 - 2 * z))), (z, 0, 2)),
]
vals = [float(sp.simplify(v)) for v in orders]
target = float(sp.Rational(18, 7) * r3)
print("six values:", [round(v, 6) for v in vals])

h = 0.05
xs = np.arange(h, float(4 ** (1 / 3)) + h, h)
ys = np.arange(0.0, 4.0 + h, h)
zs = np.arange(0.0, 2.0, h)
grid = np.array([[a, b, c] for a in xs for b in ys for c in zs])
inside = (grid[:, 1] >= grid[:, 0] ** 3) & (grid[:, 2] <= (4 - grid[:, 1]) / 2)
gvol = float(inside.sum()) * h ** 3
print("grid volume:", round(gvol, 4))
assert max(abs(v - vals[0]) for v in vals) < 1e-9 and abs(vals[0] - target) < 1e-9 and abs(gvol - target) < 0.1
print("PASS 1.2")
