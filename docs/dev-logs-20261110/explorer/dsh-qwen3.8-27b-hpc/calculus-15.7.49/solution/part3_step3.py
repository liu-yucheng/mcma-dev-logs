"""Exact moment of inertia about the z-axis for problem 15.7.49.

Iz = int_E (x^2 + y^2) rho dV with the same region and density.
"""
import sympy as sp

r, t, z = sp.symbols("r t z", nonnegative=True)
x = r * sp.cos(t)
y = r * sp.sin(t)
rho = 1 + x + y + z
J = r

Iz = sp.integrate(sp.integrate(sp.integrate(r**2 * rho * J, (z, 0, y)),
                               (r, 0, 1)), (t, 0, sp.pi / 2))
Iz = sp.simplify(Iz)
print("Iz (exact)  =", Iz)
print("Iz numeric  =", sp.N(Iz, 15))

# Cross-check with Cartesian order.
xc, yc = sp.symbols("x y", nonnegative=True)
rho_c = 1 + xc + yc + z
Iz2 = sp.integrate(sp.integrate(sp.integrate((xc**2 + yc**2) * rho_c, (z, 0, yc)),
                                (yc, 0, sp.sqrt(1 - xc**2))), (xc, 0, 1))
Iz2 = sp.simplify(Iz2)
print("Iz (cart.)  =", Iz2)
assert sp.simplify(Iz - Iz2) == 0, "Iz mismatch between orders"
print("OK: both orders agree")
