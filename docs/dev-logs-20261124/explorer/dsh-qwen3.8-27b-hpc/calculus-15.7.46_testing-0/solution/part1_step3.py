"""Step 1.3: slicing by horizontal disks reproduces Iz and Iz/M = 3*h**2/10."""
import numpy as np
import sympy as sp

k, h = sp.symbols("k h", positive=True)
z = sp.symbols("z", positive=True)
dm = k * sp.pi * z**2
Iz_slice = sp.integrate(sp.Rational(1, 2) * dm * z**2, (z, 0, h))
ratio = sp.simplify(Iz_slice / (k * sp.pi * h**3 / 3))
print("Iz slice:", Iz_slice, " ratio Iz/M:", ratio)
n, d = 120, 2.0 / 120
xs = -1.0 + (np.arange(n) + 0.5) * d
ys = -1.0 + (np.arange(n) + 0.5) * d
zs = (np.arange(n) + 0.5) / n
X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
inside = (X * X + Y * Y) <= Z * Z
Iz_num = float(np.sum((X * X + Y * Y) * inside) * d * d * (1.0 / n))
assert abs(Iz_num - float(Iz_slice.subs({k: 1, h: 1}))) < 0.01
print("PASS 1.3")
