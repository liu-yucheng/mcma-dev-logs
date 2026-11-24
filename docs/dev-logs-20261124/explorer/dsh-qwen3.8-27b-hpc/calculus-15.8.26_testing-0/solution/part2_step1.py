"""Step 2.1: the intersection curve lies on both the sphere and the cylinder."""

import numpy as np
import sympy as sp

a, th = sp.symbols("a theta", positive=True)
x = a * sp.cos(th) ** 2
y = a * sp.cos(th) * sp.sin(th)
z = a * sp.sin(th)
on_sphere = sp.simplify(x**2 + y**2 + z**2 - a**2)
on_cyl = sp.simplify(x**2 + y**2 - a * x)
assert on_sphere == 0
assert on_cyl == 0
print("symbolic residuals: sphere =", on_sphere, ", cylinder =", on_cyl)
tt = np.linspace(-np.pi / 2, np.pi / 2, 1001)
X = np.cos(tt) ** 2
Y = np.cos(tt) * np.sin(tt)
Z = np.sin(tt)
e1 = float(np.abs(X**2 + Y**2 + Z**2 - 1.0).max())
e2 = float(np.abs(X**2 + Y**2 - X).max())
print("max grid residuals: sphere =", e1, ", cylinder =", e2)
assert e1 < 1e-12 and e2 < 1e-12
print("PASS 2.1")
