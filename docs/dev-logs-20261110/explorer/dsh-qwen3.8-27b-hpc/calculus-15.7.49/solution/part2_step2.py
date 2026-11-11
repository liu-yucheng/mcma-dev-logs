"""Exact center of mass of E for problem 15.7.49.

Region and density as in part1_step1.py:
x = r cos t, y = r sin t, 0 <= t <= pi/2, 0 <= r <= 1, 0 <= z <= r sin t.
rho = 1 + x + y + z.
COM = (M_yz / M, M_xz / M, M_xy / M) with M_yz = int_E x rho dV etc.
"""
import sympy as sp

r, t, z = sp.symbols("r t z", nonnegative=True)
x = r * sp.cos(t)
y = r * sp.sin(t)
rho = 1 + x + y + z
J = r

def tri(func, *args):
    return sp.simplify(sp.integrate(sp.integrate(sp.integrate(func * J, *args), *args), *args))

M   = sp.integrate(sp.integrate(sp.integrate(rho * J, (z, 0, y)), (r, 0, 1)), (t, 0, sp.pi / 2))
Myz = sp.integrate(sp.integrate(sp.integrate(x * rho * J, (z, 0, y)), (r, 0, 1)), (t, 0, sp.pi / 2))
Mxz = sp.integrate(sp.integrate(sp.integrate(y * rho * J, (z, 0, y)), (r, 0, 1)), (t, 0, sp.pi / 2))
Mxy = sp.integrate(sp.integrate(sp.integrate(z * rho * J, (z, 0, y)), (r, 0, 1)), (t, 0, sp.pi / 2))

M, Myz, Mxz, Mxy = [sp.simplify(q) for q in (M, Myz, Mxz, Mxy)]
print("M   =", M)
print("Myz =", Myz)
print("Mxz =", Mxz)
print("Mxy =", Mxy)

xbar = sp.simplify(Myz / M)
ybar = sp.simplify(Mxz / M)
zbar = sp.simplify(Mxy / M)
print("xbar =", xbar, "=", sp.N(xbar, 15))
print("ybar =", ybar, "=", sp.N(ybar, 15))
print("zbar =", zbar, "=", sp.N(zbar, 15))

# Sanity: COM must lie inside the solid.
assert 0 <= float(sp.N(xbar)) <= 1
assert 0 <= float(sp.N(ybar)) <= 1
assert 0 <= float(sp.N(zbar)) and float(sp.N(zbar)) <= float(sp.N(ybar)), "zbar <= ybar required"
print("OK: COM inside the solid")
