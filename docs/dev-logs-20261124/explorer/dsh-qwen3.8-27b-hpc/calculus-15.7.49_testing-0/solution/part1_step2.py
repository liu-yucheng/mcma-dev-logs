"""Step 1.2: the first moments give the center of mass of E."""

import numpy as np
import sympy as sp

r, th, z = sp.symbols("r theta z", positive=True)
rho = 1 + r * sp.cos(th) + r * sp.sin(th) + z
lims = [(z, 0, r * sp.sin(th)), (r, 0, 1), (th, 0, sp.pi / 2)]
mom = lambda f: sp.integrate(f, *lims)
m = mom(rho * r)
c = [sp.simplify(mom(cy * rho * r) / m) for cy in (r * sp.cos(th), r * sp.sin(th), z)]
print("moments exact:", [sp.simplify(mom(cy * rho * r)) for cy in (r * sp.cos(th), r * sp.sin(th), z)])
print("center exact:", c)
print("center approx:", [float(v) for v in c])

N, gen = 200_000, np.random.default_rng(11)
p = gen.random((N, 3))
keep = (p[:, 0] ** 2 + p[:, 1] ** 2 <= 1.0) & (p[:, 2] <= p[:, 1])
w = (1 + p[:, 0] + p[:, 1] + p[:, 2]) * keep
mc = [float(np.mean(p[:, i] * w) / np.mean(w)) for i in range(3)]
print("Monte Carlo center:", [round(v, 5) for v in mc])

assert all(abs(a - b) < 0.02 for a, b in zip(mc, map(float, c)))
print("PASS 1.2")
