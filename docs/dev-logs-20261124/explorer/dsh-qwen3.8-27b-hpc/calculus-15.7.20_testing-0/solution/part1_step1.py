"""Step 1.1: the paraboloids meet at r = 2 where both give y = 4."""

import numpy as np
import sympy as sp

r = sp.symbols("r", nonnegative=True)
meet = sp.solve(sp.Eq(r**2, 8 - r**2), r)
print("intersection radius:", meet)
for rv in (0.0, 1.0, 2.0):
    print(f"slice at r = {rv}: y from {rv**2:.3f} to {8.0 - rv**2:.3f}")
axis = np.linspace(0, 2.0, 4001)
band = (8.0 - axis**2) - axis**2
num = float(2.0 * np.pi * np.trapezoid(band * axis, axis))
print("shell volume numeric:", round(num, 4))
assert abs(num - float(16 * np.pi)) < 0.05
print("PASS 1.1")
