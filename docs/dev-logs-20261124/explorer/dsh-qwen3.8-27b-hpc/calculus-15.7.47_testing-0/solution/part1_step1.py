"""Step 1.1: the mass integral over the cylinder-plane solid."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = sp.sqrt(x**2 + y**2)
M = sp.integrate(sp.integrate(sp.integrate(rho, (z, 0, 1 - y)), (x, -sp.sqrt(y), sp.sqrt(y))), (y, 0, 1))
print("mass exact:", sp.N(M, 12))
rng = np.random.default_rng(1)
X = rng.uniform(-1, 1, 400000)
Y = rng.uniform(0, 1, 400000)
Z = rng.uniform(0, 1, 400000)
iv = (X * X <= Y) & (Z <= 1 - Y)
M_mc = 2.0 * float(np.mean(np.sqrt(X * X + Y * Y) * iv))
print("mass MC:", round(M_mc, 6))
assert abs(M_mc - float(M)) < 0.002
print("PASS 1.1")
