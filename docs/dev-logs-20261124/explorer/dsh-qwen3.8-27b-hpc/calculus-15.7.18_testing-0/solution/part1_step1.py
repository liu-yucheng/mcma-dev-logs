"""Step 1.1: for 0 <= y <= 3, z runs to sqrt(9 - y^2) and x runs to y/3."""

import numpy as np
import sympy as sp

y = sp.symbols("y", nonnegative=True)
ztop = sp.sqrt(9 - y**2)
for yy in (0, 1.5, 3):
    print(f"section at y = {yy}: z in [0, {float(ztop.subs(y, yy)):.4f}], x in [0, {yy / 3:.4f}]")
step = 0.02
axis = np.arange(0, 3.0, step)
yy, zz = np.meshgrid(axis, axis)
count = int((yy**2 + zz**2 <= 9.0).sum())
area = count * step**2
print("quarter disk area:", round(area, 3), "target", round(9.0 * np.pi / 4.0, 3))
assert abs(area - 9.0 * np.pi / 4.0) < 0.15
print("PASS 1.1")
