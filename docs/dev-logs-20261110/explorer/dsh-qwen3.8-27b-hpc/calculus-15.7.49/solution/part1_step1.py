"""Exact mass of E for problem 15.7.49.

E: first octant, bounded by the cylinder x^2 + y^2 = 1 and the planes
y = z, x = 0, z = 0. In polar coordinates in the xy-plane
(x = r cos t, y = r sin t, 0 <= t <= pi/2, 0 <= r <= 1) the solid is
0 <= z <= y = r sin t. Density rho = 1 + x + y + z.
"""
import sympy as sp

r, t, z = sp.symbols("r t z", nonnegative=True)
rho = 1 + r * sp.cos(t) + r * sp.sin(t) + z
J = r  # polar Jacobian in the xy-plane

M = sp.integrate(sp.integrate(sp.integrate(rho * J, (z, 0, r * sp.sin(t))),
                              (r, 0, 1)), (t, 0, sp.pi / 2))
M = sp.simplify(M)
print("mass M (polar)  =", M)
print("mass numeric    =", sp.N(M, 15))

# Independent Cartesian check: 0 <= x <= 1, 0 <= y <= sqrt(1 - x^2), 0 <= z <= y
x, y = sp.symbols("x y", nonnegative=True)
rho_c = 1 + x + y + z
M2 = sp.integrate(sp.integrate(sp.integrate(rho_c, (z, 0, y)),
                               (y, 0, sp.sqrt(1 - x**2))), (x, 0, 1))
M2 = sp.simplify(M2)
print("mass M (cart.)  =", M2)
assert sp.simplify(M - M2) == 0, "mass mismatch between orders"
print("OK: both orders agree")
