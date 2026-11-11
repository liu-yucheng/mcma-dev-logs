"""Part 1, Step 1 - mass and center of mass, exercise 15.7.39.

E: under plane z = 1 + x + y, above D = {(x,y): 0 <= x <= 1, 0 <= y <= sqrt(x)}.
rho = 2 (constant).
"""
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = 2

# Mass
M = sp.integrate(sp.integrate(sp.integrate(rho, (z, 0, 1 + x + y)),
                              (y, 0, sp.sqrt(x))), (x, 0, 1))
print("M  =", M)

Myz = sp.integrate(sp.integrate(sp.integrate(x * rho, (z, 0, 1 + x + y)),
                                (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxz = sp.integrate(sp.integrate(sp.integrate(y * rho, (z, 0, 1 + x + y)),
                                (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxy = sp.integrate(sp.integrate(sp.integrate(z * rho, (z, 0, 1 + x + y)),
                                (y, 0, sp.sqrt(x))), (x, 0, 1))
print("Myz =", Myz, "   Mxz =", Mxz, "   Mxy =", Mxy)

xb, yb, zb = Myz / M, Mxz / M, Mxy / M
print("xbar =", sp.simplify(xb), "=", float(xb))
print("ybar =", sp.simplify(yb), "=", float(yb))
print("zbar =", sp.simplify(zb), "=", float(zb))

# Monte Carlo sanity check
# --- Mxy inner antiderivative check -------------------------------
# int_0^{sqrt(x)} (1+x+y)^2 dy = [(1+x+sqrt(x))^3 - (1+x)^3]/3
t = sp.symbols("t")
inner = ((1 + x + sp.sqrt(x))**3 - (1 + x)**3) / 3
inner_exp = sp.expand(inner.rewrite(sp.Pow))
check_Mxy = sp.integrate(inner, (x, 0, 1))
print("inner antiderivative check, outer integral =", sp.simplify(check_Mxy),
      " (must equal 571/210)")
assert sp.simplify(check_Mxy - sp.Rational(571, 210)) == 0

import numpy as np
rng = np.random.default_rng(7)
N = 600_000
xs = rng.uniform(0, 1, N)
ys = rng.uniform(0, 1, N)
sel = ys <= np.sqrt(xs)
zs = rng.uniform(0, 3, N)  # 1+x+y <= 3; box x,y in [0,1], z in [0,3]
inside = sel & (zs <= 1 + xs + ys)
boxvol = 3.0
V = inside.sum() / N * boxvol
print("MC volume:", round(V, 4), " exact:", float(sp.integrate(sp.integrate(1 + x + y, (y, 0, sp.sqrt(x))), (x, 0, 1))))
print("MC M:", round(2 * V, 4), " exact:", float(M))
