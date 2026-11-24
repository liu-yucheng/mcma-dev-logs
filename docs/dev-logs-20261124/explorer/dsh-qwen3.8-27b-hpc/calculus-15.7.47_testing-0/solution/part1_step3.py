"""Step 1.3: the z-axis inertia integral of the solid."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = sp.sqrt(x**2 + y**2)
Iz = sp.integrate(sp.integrate(sp.integrate(rho**3, (z, 0, 1 - y)), (x, -sp.sqrt(y), sp.sqrt(y))), (y, 0, 1))
print("Iz exact:", sp.N(Iz, 12))
rng = np.random.default_rng(3)
X = rng.uniform(-1, 1, 400000)
Y = rng.uniform(0, 1, 400000)
Z = rng.uniform(0, 1, 400000)
iv = (X * X <= Y) & (Z <= 1 - Y)
Iz_mc = 2.0 * float(np.mean((X * X + Y * Y) ** 1.5 * iv))
print("Iz MC:", round(Iz_mc, 6))
assert abs(Iz_mc - float(Iz)) < 0.002
print("PASS 1.3")
