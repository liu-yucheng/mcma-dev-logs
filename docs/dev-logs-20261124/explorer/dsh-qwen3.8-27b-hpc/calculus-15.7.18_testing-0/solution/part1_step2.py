"""Step 1.2: the integral of z over E equals 27/8."""

import numpy as np
import sympy as sp

y = sp.symbols("y", nonnegative=True)
exact = sp.simplify(sp.integrate((y / 3) * (9 - y**2) / 2, (y, 0, 3)))
yy = np.linspace(0, 3, 4001)
num = float(np.trapezoid((yy / 3) * (9.0 - yy**2) / 2, yy))
print("exact value:", exact, "=", float(exact))
print("numeric value:", round(num, 4))
assert abs(num - float(exact)) < 0.01
print("PASS 1.2")
