"""Exact moment of inertia about the z-axis for problem 15.7.50.

Iz = int_E (x^2 + y^2) rho dV with the same region and density.
"""
import sympy as sp

r, t, x = sp.symbols("r t x", nonnegative=True)
y = r * sp.cos(t)
z = r * sp.sin(t)
rho = x**2 + y**2
J = r

Iz = sp.integrate(sp.integrate(sp.integrate((x**2 + y**2) * rho * J, (x, 0, y / 3)),
                               (r, 0, 3)), (t, 0, sp.pi / 2))
Iz = sp.simplify(Iz)
print("Iz (exact)  =", Iz)
print("Iz numeric  =", sp.N(Iz, 15))
print("Iz to 3 dp  =", round(float(sp.N(Iz, 20)), 3))

# Independent Cartesian check.
xc, yc, zc = sp.symbols("x y z", nonnegative=True)
rho_c = xc**2 + yc**2
Iz2 = sp.integrate(sp.integrate(sp.integrate((xc**2 + yc**2) * rho_c,
                                            (xc, 0, yc / 3)),
                                (yc, 0, sp.sqrt(9 - zc**2))), (zc, 0, 3))
Iz2 = sp.simplify(Iz2)
print("Iz (cart.)  =", Iz2)
print("Iz cart 3dp =", round(float(sp.N(Iz2, 20)), 3))
assert sp.simplify(Iz - Iz2) == 0, "Iz mismatch between orders"
print("OK: both orders agree")
