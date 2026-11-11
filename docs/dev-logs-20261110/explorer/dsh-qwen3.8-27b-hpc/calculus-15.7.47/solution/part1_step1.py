"""Parts 1-3, Step 1 - SET UP (do NOT evaluate) the integrals, exercise 15.7.47.

Solid enclosed by the cylinder y = x^2 and the planes z = 0 and y + z = 1;
rho(x, y, z) = sqrt(x^2 + y^2).

Region description (order dz dy dx):
  -1 <= x <= 1,   x^2 <= y <= 1,   0 <= z <= 1 - y
  (the cylinder meets the plane y + z = 1 at z = 0 in the line y = 1,
   i.e. at x = +/- 1)

Verification (values stay private; the published answer is the setup only):
  1. Geometry checks (symbolic, sympy).
  2. Region membership tests.
  3. Monte-Carlo sanity check of the mass integrand over the region.
"""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = sp.sqrt(x**2 + y**2)

# --- 1. Geometry -----------------------------------------------------------
# intersection of y = x^2 with y + z = 1: substitute -> z = 1 - x^2.
# At z = 0: 1 - x^2 = 0 -> x = +/- 1, y = 1.  Vertex of cylinder: (0,0).
z_on = 1 - x**2
xs = sp.solve(sp.Eq(z_on, 0), x)
print("z=0 intersection x-values:", xs, " (expect [-1, 1])")
# max z on the solid: at y = 0 (x = 0) -> z = 1
print("z at (x,y)=(0,0):", z_on.subs(x, 0), " (expect 1)")

# --- 2. Region membership --------------------------------------------------
def in_region(px, py, pz):
    return (-1 <= px <= 1) and (px**2 <= py <= 1) and (0 <= pz <= 1 - py)

eps = 1e-9
def in_region_t(px, py, pz):
    return (-1 - eps <= px <= 1 + eps) and (px**2 - eps <= py <= 1 + eps) \
        and (-eps <= pz <= 1 - py + eps)

tests = [
    ((0, 0.5, 0.4), True),    # inside
    ((0.5, 0.4, 0.5), True),  # inside (0.4 >= 0.25, 0.5 <= 1-0.4)
    ((0.5, 0.1, 0.5), False), # y < x^2 = 0.25 -> outside
    ((0, 0.5, 0.6), False),   # z > 1 - y = 0.5 -> outside
    ((1.2, 1, 0), False),     # x > 1 -> outside
    ((-0.8, 0.64, 0), True),  # on the cylinder wall y = x^2, z = 0
]
ok = True
for (pt, expect) in tests:
    got = in_region_t(*pt)
    ok &= (got == expect)
    print("point", pt, "inside:", got, "expected:", expect,
          "OK" if got == expect else "MISMATCH")
print("membership tests all OK:", ok)

# --- 3. Monte-Carlo sanity checks (private) --------------------------------
rng = np.random.default_rng(5)
N = 1_500_000
xs_ = rng.uniform(-1, 1, N)
ys_ = rng.uniform(0, 1, N)
zs_ = rng.uniform(0, 1, N)
inside = (xs_**2 <= ys_) & (ys_ <= 1) & (zs_ <= 1 - ys_)
box = 2.0  # x in [-1,1] (2) * y in [0,1] (1) * z in [0,1] (1)
V = inside.sum() / N * box
rho_i = np.sqrt(xs_**2 + ys_**2)[inside]
M_mc = rho_i.sum() / N * box
Mxz_mc = (np.abs(xs_)[inside] * rho_i).sum() / N * box * 2 - (xs_[inside] * rho_i).sum() / N * box
# Mxz = integral of x*rho: odd in x -> 0
Mxz_mc = (xs_[inside] * rho_i).sum() / N * box
Myz_mc = (ys_[inside] * rho_i).sum() / N * box
Mxy_mc = (zs_[inside] * rho_i).sum() / N * box
Iz_mc = (rho_i**2).sum() / N * box  # (x^2+y^2)*rho = (sqrt(x^2+y^2))^2 * rho = rho^3... 
# careful: integrand for Iz is (x^2+y^2)*rho = rho^2 * rho = rho^3
Iz_mc = (rho_i**3).sum() / N * box
print("MC volume:", round(V, 4))
print("MC M  :", round(M_mc, 4))
print("MC Mxz (expect ~0):", round(Mxz_mc, 5))
print("MC Myz:", round(Myz_mc, 4))
print("MC Mxy:", round(Mxy_mc, 4))
print("MC Iz :", round(Iz_mc, 4))

# exact volume cross-check (symbolic)
V_ex = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, 1 - y)), (y, x**2, 1)), (x, -1, 1))
print("exact volume:", V_ex, "=", float(V_ex))
