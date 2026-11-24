"""Step 1.3: a midpoint grid over theta and phi matches the exact volume."""

import numpy as np
import sympy as sp

th, ph = sp.symbols("theta phi", positive=True)
rho = 1 + sp.Rational(1, 5) * sp.sin(6 * th) * sp.sin(5 * ph)
V_ex = sp.Rational(1, 3) * sp.integrate(sp.integrate(sp.expand(rho**3) * sp.sin(ph), (ph, 0, sp.pi)), (th, 0, 2 * sp.pi))

n_th, n_ph = 2400, 1200
t = (np.arange(n_th) + 0.5) * (2.0 * np.pi / n_th)
p = (np.arange(n_ph) + 0.5) * (np.pi / n_ph)
h_th, h_ph = 2.0 * np.pi / n_th, np.pi / n_ph
RH, PH = np.meshgrid(t, p, indexing="ij")
rho_g = 1.0 + 0.2 * np.sin(6.0 * RH) * np.sin(5.0 * PH)
grid_V = float((rho_g**3 * np.sin(PH) / 3.0).sum() * h_th * h_ph)
lo, hi = sp.Rational(4, 5), sp.Rational(6, 5)
Vlo = sp.Rational(4, 3) * sp.pi * lo**3
Vhi = sp.Rational(4, 3) * sp.pi * hi**3
print("grid volume:", round(grid_V, 6))
print("exact volume:", sp.simplify(V_ex), "=", round(float(V_ex), 6))
print("bounding spheres:", round(float(Vlo), 6), "and", round(float(Vhi), 6))
assert abs(grid_V - float(V_ex)) < h_ph
assert float(Vlo) < float(V_ex) < float(Vhi)
print("PASS 1.3")
