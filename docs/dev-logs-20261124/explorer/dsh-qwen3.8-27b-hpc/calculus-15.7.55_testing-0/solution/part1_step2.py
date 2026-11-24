"""Step 1.2: the change of variables maps the ellipsoid to the unit ball."""
import numpy as np
import sympy as sp

u, v, w = sp.symbols("u v w")
Jdet = 1/sp.sqrt(6)
print("Jacobian =", Jdet)
Iball = sp.simplify(sp.integrate(sp.integrate(sp.integrate((1 - (u**2 + v**2 + w**2)),
    (u, -1, 1), (v, -sp.sqrt(1 - u**2), sp.sqrt(1 - u**2)),
    (w, -sp.sqrt(1 - u**2 - v**2), sp.sqrt(1 - u**2 - v**2))))*Jdet)
print("integral over the ellipsoid (exact):", Iball)

rng = np.random.default_rng(5)
N = 200000
U = rng.normal(size=(N, 3))
q = (U**2).sum(axis=1)
k = q < 1.0
Vball = 4.0/3.0*np.pi
est = Vball*float(np.mean(1 - q[k]))/float(np.sqrt(6))
print("Monte Carlo ellipsoid integral:", round(est, 4))
assert abs(est - float(Iball)) < 0.1
print("PASS 1.2")
