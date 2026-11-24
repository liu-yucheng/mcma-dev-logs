"""Step 1.3: the section at height z is x^3 <= y <= 4 - 2z, shrinking to (0, 0, 2)."""

import numpy as np
import sympy as sp

x, y = sp.symbols("x y", nonnegative=True)
for hgt in [0, 1, 2]:
    xmax = (4 - 2 * hgt) ** sp.Rational(1, 3)
    print("z =", hgt, ": x in [0, {}] ~ {:.4f}, y in [x^3, {}]".format(sp.simplify(xmax), float(xmax), 4 - 2 * hgt))

corners = [(0, 0, 0), (0, 4, 0), (4 ** sp.Rational(1, 3), 4, 0)]
for c in corners:
    on = sp.simplify(c[1] + 2 * c[2] - 4)
    print("corner", c, "plane value y + 2z - 4 =", on)

g = np.mgrid[0.01:1.59:0.02, 0.01:4.001:0.02]
ztop = (4 - g[1]) / 2
inside = g[1] >= g[0] ** 3
print("grid max z:", round(float(ztop[inside].max()), 4), "exact max z: 2")
assert abs(float(ztop[inside].max()) - 2.0) < 0.02
print("PASS 1.3")
