"""Step 1.3: the moment of inertia of E about the z-axis is 17/60 + pi/16."""

import numpy as np
import sympy as sp

r, th, z = sp.symbols("r theta z", positive=True)
rho = 1 + r * sp.cos(th) + r * sp.sin(th) + z
iz = sp.integrate(r ** 2 * rho * r, (z, 0, r * sp.sin(th)), (r, 0, 1), (th, 0, sp.pi / 2))
print("Iz exact:", sp.simplify(iz), "approx:", float(iz))

N, gen = 200_000, np.random.default_rng(13)
p = gen.random((N, 3))
keep = (p[:, 0] ** 2 + p[:, 1] ** 2 <= 1.0) & (p[:, 2] <= p[:, 1])
vals = (p[:, 0] ** 2 + p[:, 1] ** 2) * (1 + p[:, 0] + p[:, 1] + p[:, 2]) * keep
mc = float(vals.mean())
print("Monte Carlo Iz:", round(mc, 5))

assert abs(mc - float(iz)) < 0.02
print("PASS 1.3")
