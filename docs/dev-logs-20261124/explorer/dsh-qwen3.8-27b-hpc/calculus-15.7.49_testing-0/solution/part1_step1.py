"""Step 1.1: the volume of E is 1/3 and the mass is (44 + 9*pi)/96."""

import numpy as np
import sympy as sp

r, th, z = sp.symbols("r theta z", positive=True)
rho = 1 + r * sp.cos(th) + r * sp.sin(th) + z
vol = sp.integrate(r, (z, 0, r * sp.sin(th)), (r, 0, 1), (th, 0, sp.pi / 2))
mass = sp.integrate(rho * r, (z, 0, r * sp.sin(th)), (r, 0, 1), (th, 0, sp.pi / 2))
print("volume exact:", vol, "mass exact:", sp.simplify(mass), "approx:", float(mass))

N, gen = 200_000, np.random.default_rng(7)
p = gen.random((N, 3))
keep = (p[:, 0] ** 2 + p[:, 1] ** 2 <= 1.0) & (p[:, 2] <= p[:, 1])
mc_vol = float(keep.mean())
mc_mass = float(((1 + p[:, 0] + p[:, 1] + p[:, 2]) * keep).mean())
print("Monte Carlo volume:", round(mc_vol, 5), "mass:", round(mc_mass, 5))

assert abs(mc_vol - float(vol)) < 0.01 and abs(mc_mass - float(mass)) < 0.02
print("PASS 1.1")
