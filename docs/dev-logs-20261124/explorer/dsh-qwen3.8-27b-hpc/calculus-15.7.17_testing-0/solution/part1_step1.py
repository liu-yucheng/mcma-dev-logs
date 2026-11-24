"""Step 1.1: the slice of E at x is a disk of radius sqrt(x)/2 with area pi*x/4."""

import numpy as np
import sympy as sp

x = sp.symbols("x", positive=True)
area = sp.pi * sp.sqrt(x) ** 2 / 4
assert sp.simplify(area - sp.pi * x / 4) == 0
step = 0.005
axis = np.arange(-1.0, 1.0, step)
yy, zz = np.meshgrid(axis, axis)
count = int((yy**2 + zz**2 <= 1.0).sum())
num = count * step**2
print("exact area at x = 4:", float(sp.pi))
print("grid area at x = 4:", round(num, 4))
assert abs(num - float(sp.pi)) < 0.02
print("PASS 1.1")
