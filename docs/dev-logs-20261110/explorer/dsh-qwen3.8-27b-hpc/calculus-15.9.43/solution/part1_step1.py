"""Problem 15.9.43: verify the silo geometry.

Silo = cylinder of radius R = 3 and height H = 10, surmounted by a
hemisphere of radius 3 (the dome closes the top circular rim of the
cylinder, so it has the same radius R = 3).
"""

import sympy as sp

x, y = sp.symbols("x y", real=True)
R, H = 3, 10

# Rim circle at height z = H: x^2 + y^2 = R^2  (radius 3).
print("rim: x^2 + y^2 - 9 factors as", sp.factor(x**2 + y**2 - R**2).subs(y, 0))

# Dome:  z = H + sqrt(R^2 - x^2 - y^2);  top point at x = y = 0.
dome_top = H + sp.sqrt(R**2)
print("dome top height =", dome_top, "= H + R =", H + R)

# Context for the figure: total volume V = pi R^2 H + (2/3) pi R^3.
V_cyl = sp.pi * R**2 * H
V_dome = sp.Rational(2, 3) * sp.pi * R**3
V = sp.simplify(V_cyl + V_dome)
print("V_cylinder =", V_cyl, "  V_hemisphere =", V_dome)
print("V_total exact =", V, "  numeric =", sp.N(V, 10))
assert V == 108 * sp.pi, "expected 108*pi"
print("OK: total silo volume = 108*pi")
