"""Part 1, Step 1 - moment of inertia about the z-axis, exercise 15.7.46.

Cone: sqrt(x^2 + y^2) <= z <= h, constant density k.
In cylindrical coords: 0 <= theta <= 2*pi, 0 <= r <= h, r <= z <= h.
Iz = k * int (x^2 + y^2) dV = k * int r^2 * r dz dr dtheta.
"""
import sympy as sp

r, th, z, h, k = sp.symbols("r theta z h k", positive=True)

Iz = sp.integrate(sp.integrate(sp.integrate(k * r**2 * r, (z, r, h)),
                               (r, 0, h)), (th, 0, 2*sp.pi))
Iz = sp.simplify(Iz)
print("Iz =", Iz)

# mass of the cone (for context) - include the Jacobian r
M = sp.integrate(sp.integrate(sp.integrate(k * r, (z, r, h)), (r, 0, h)), (th, 0, 2*sp.pi))
print("M  =", sp.simplify(M), " (should be pi*k*h^3/3)")
assert sp.simplify(M - sp.pi * k * h**3 / 3) == 0
# standard cone formula cross-check: Iz = (3/10) M R^2 with R = h
Iz_std = sp.Rational(3, 10) * M * h**2
print("Iz via (3/10)MR^2 =", sp.simplify(Iz_std), " matches:", sp.simplify(Iz_std - Iz) == 0)

# also verify by integrating in x,y with z last using the region description
# Iz = k * int_0^h int_0^{2pi} int_0^h r^3 (h - r)... check numerically
import mpmath as mp
hval, kval = 2.0, 3.0
num = mp.quad(lambda H: mp.quad(lambda R: kval * R**3 * (hval - R), [0, hval]), [0, 2*mp.pi])
print("numeric Iz (h=2,k=3):", num, " formula:", (mp.pi*kval*hval**5)/10)

# Monte Carlo in the physical box [0,1]^3 x [-1,1] (h = 1)
import numpy as np
rng = np.random.default_rng(3)
N = 1_200_000
xs = rng.uniform(-1, 1, N); ys = rng.uniform(-1, 1, N); zs = rng.uniform(0, 1, N)
inside = np.sqrt(xs**2 + ys**2) <= zs
V_mc = inside.sum() / N * 4.0  # box 2*2*1
Iz_mc = (xs**2 + ys**2)[inside].sum() / N * 4.0
print("MC cone volume (h=1):", round(V_mc, 4), " exact:", round(float(mp.pi/3), 4))
print("MC Iz (h=1,k=1):", round(Iz_mc, 4), " exact:", round(float(mp.pi/10), 4))
