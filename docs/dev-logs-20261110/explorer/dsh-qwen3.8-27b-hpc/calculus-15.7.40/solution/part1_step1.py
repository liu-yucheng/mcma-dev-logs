"""Part 1, Step 1 - mass and center of mass, exercise 15.7.40.

E bounded by the parabolic cylinder z = 1 - y^2 and the planes
x + z = 1, x = 0, z = 0.  rho = 4 (constant).

Region description:
  0 <= z <= 1,
  0 <= x <= 1 - z          (from x = 0 and x + z = 1, z <= 1),
  -sqrt(1 - z) <= y <= sqrt(1 - z)   (from z <= 1 - y^2).
"""
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = 4
sqrty = sp.sqrt(1 - z)

M   = sp.integrate(sp.integrate(sp.integrate(rho, (y, -sqrty, sqrty)),
                                (x, 0, 1 - z)), (z, 0, 1))
Myz = sp.integrate(sp.integrate(sp.integrate(x * rho, (y, -sqrty, sqrty)),
                                (x, 0, 1 - z)), (z, 0, 1))
Mxz = sp.integrate(sp.integrate(sp.integrate(y * rho, (y, -sqrty, sqrty)),
                                (x, 0, 1 - z)), (z, 0, 1))
Mxy = sp.integrate(sp.integrate(sp.integrate(z * rho, (y, -sqrty, sqrty)),
                                (x, 0, 1 - z)), (z, 0, 1))
print("M   =", M)
print("Myz =", Myz)
print("Mxz =", Mxz, " (expected 0 by symmetry)")
print("Mxy =", Mxy)
print("xbar =", sp.simplify(Myz / M))
print("ybar =", sp.simplify(Mxz / M))
print("zbar =", sp.simplify(Mxy / M))

# Monte Carlo
import numpy as np
rng = np.random.default_rng(11)
N = 800_000
xs = rng.uniform(0, 1, N)
ys = rng.uniform(-1, 1, N)
zs = rng.uniform(0, 1, N)
inside = (xs + zs <= 1) & (zs >= 0) & (zs <= 1 - ys**2) & (xs >= 0)
V = inside.sum() / N * 4.0  # box 1 * 2 * 1 = 2... wait
# box: x in [0,1], y in [-1,1], z in [0,1] -> volume 2
V = inside.sum() / N * 2.0
print("MC volume:", round(V, 4), " exact:", float(sp.integrate(sp.integrate(sp.integrate(1, (y, -sqrty, sqrty)), (x, 0, 1 - z)), (z, 0, 1))))
print("MC M:", round(4 * V, 4), " exact:", float(M))
