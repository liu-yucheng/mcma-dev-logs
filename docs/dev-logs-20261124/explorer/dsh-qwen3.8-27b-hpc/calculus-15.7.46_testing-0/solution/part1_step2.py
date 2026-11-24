"""Step 1.2: the z-axis moment of inertia is k*pi*h**5/10."""
import numpy as np
import sympy as sp

k, h = sp.symbols("k h", positive=True)
r, th, z = sp.symbols("r theta z", positive=True)
Iz = sp.integrate(k * r**3, (r, 0, z), (th, 0, 2 * sp.pi), (z, 0, h))
print("Iz exact:", Iz, "=", round(float(Iz.subs({k: 1, h: 1})), 5))
n, d = 120, 2.0 / 120
xs = -1.0 + (np.arange(n) + 0.5) * d
ys = -1.0 + (np.arange(n) + 0.5) * d
zs = (np.arange(n) + 0.5) / n
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
inside = (X * X + Y * Y) <= Z * Z
Iz_num = float(np.sum((X * X + Y * Y) * inside) * d * d * (1.0 / n))
print("Iz grid:", round(Iz_num, 5))
assert abs(Iz_num - float(Iz.subs({k: 1, h: 1}))) < 0.01
print("PASS 1.2")
