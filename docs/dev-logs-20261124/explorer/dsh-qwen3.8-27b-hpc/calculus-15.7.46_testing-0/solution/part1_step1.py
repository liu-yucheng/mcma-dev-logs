"""Step 1.1: the cone mass equals k*pi*h**3/3 in polar form."""
import numpy as np
import sympy as sp

k, h = sp.symbols("k h", positive=True)
r, th, z = sp.symbols("r theta z", positive=True)
M = sp.integrate(k * r, (r, 0, z), (th, 0, 2 * sp.pi), (z, 0, h))
print("mass exact:", M, "=", round(float(M.subs({k: 1, h: 1})), 5))
n, d = 120, 2.0 / 120
xs = -1.0 + (np.arange(n) + 0.5) * d
ys = -1.0 + (np.arange(n) + 0.5) * d
zs = (np.arange(n) + 0.5) / n
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
inside = (X * X + Y * Y) <= Z * Z
M_num = float(np.sum(inside) * d * d * (1.0 / n))
print("mass grid:", round(M_num, 5))
assert abs(M_num - float(M.subs({k: 1, h: 1}))) < 0.01
print("PASS 1.1")
