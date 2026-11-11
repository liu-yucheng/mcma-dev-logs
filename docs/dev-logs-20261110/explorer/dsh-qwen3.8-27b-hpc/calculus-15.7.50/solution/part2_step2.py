"""Exact center of mass of E for problem 15.7.50, then three-decimal rounding.

Region and density as in part1_step1.py.
COM = (M_yz/M, M_xz/M, M_xy/M).
"""
import sympy as sp

r, t, x = sp.symbols("r t x", nonnegative=True)
y = r * sp.cos(t)
z = r * sp.sin(t)
rho = x**2 + y**2
J = r

M   = sp.integrate(sp.integrate(sp.integrate(rho * J, (x, 0, y / 3)), (r, 0, 3)), (t, 0, sp.pi / 2))
Myz = sp.integrate(sp.integrate(sp.integrate(x * rho * J, (x, 0, y / 3)), (r, 0, 3)), (t, 0, sp.pi / 2))
Mxz = sp.integrate(sp.integrate(sp.integrate(y * rho * J, (x, 0, y / 3)), (r, 0, 3)), (t, 0, sp.pi / 2))
Mxy = sp.integrate(sp.integrate(sp.integrate(z * rho * J, (x, 0, y / 3)), (r, 0, 3)), (t, 0, sp.pi / 2))

M, Myz, Mxz, Mxy = [sp.simplify(q) for q in (M, Myz, Mxz, Mxy)]
print("M   =", M)
print("Myz =", Myz)
print("Mxz =", Mxz)
print("Mxy =", Mxy)

xbar = sp.simplify(Myz / M)
ybar = sp.simplify(Mxz / M)
zbar = sp.simplify(Mxy / M)
for name, val in (("xbar", xbar), ("ybar", ybar), ("zbar", zbar)):
    print(f"{name} (exact)  = {val}")
    print(f"{name} numeric  = {sp.N(val, 15)}")
    print(f"{name} to 3 dp  = {round(float(sp.N(val, 20)), 3)}")

# Sanity: COM inside solid: 0 <= x <= y/3, 0 <= y, 0 <= z, y^2+z^2 <= 9
xn = float(sp.N(xbar, 20)); yn = float(sp.N(ybar, 20)); zn = float(sp.N(zbar, 20))
assert 0 <= xn <= yn / 3, "xbar <= ybar/3 required"
assert yn >= 0 and zn >= 0
assert yn**2 + zn**2 <= 9 + 1e-12
print("OK: COM inside the solid")
