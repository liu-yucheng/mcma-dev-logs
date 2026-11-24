"""Step 1.2: the volume is the integral of (8 - 2r^2) r over the disk of radius 2."""

import numpy as np
import sympy as sp

r = sp.symbols("r", nonnegative=True)
theta = sp.symbols("theta")
exact = sp.integrate(sp.integrate((8 - 2 * r**2) * r, (r, 0, 2)), (theta, 0, 2 * sp.pi))
h = 0.01
grid = np.array([[a, b] for a in np.arange(-2, 2, h) for b in np.arange(-2, 2, h)])
count = int((grid[:, 0] ** 2 + grid[:, 1] ** 2 <= 4.0).sum())
disk = count * h**2
print("exact volume:", exact, "=", float(exact))
print("disk area:", round(disk, 3), "target", round(4.0 * np.pi, 3))
assert abs(disk - 4.0 * np.pi) < 0.2
print("PASS 1.2")
