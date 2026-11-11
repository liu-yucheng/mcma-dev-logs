"""Exact mass of E for problem 15.7.50, then three-decimal rounding.

E: first octant, bounded by the cylinder y^2 + z^2 = 9 and the planes
x = 0, y = 3x, z = 0. In polar coordinates in the yz-plane
(y = r cos t, z = r sin t, 0 <= t <= pi/2, 0 <= r <= 3) the solid is
0 <= x <= y/3 = r cos t / 3. Density rho = x^2 + y^2.
"""
import sympy as sp

r, t, x = sp.symbols("r t x", nonnegative=True)
y = r * sp.cos(t)
z = r * sp.sin(t)
rho = x**2 + y**2
J = r

M = sp.integrate(sp.integrate(sp.integrate(rho * J, (x, 0, y / 3)),
                              (r, 0, 3)), (t, 0, sp.pi / 2))
M = sp.simplify(M)
print("mass M (exact) =", M)
print("mass M numeric =", sp.N(M, 15))
print("mass to 3 dp   =", round(float(sp.N(M, 20)), 3))
