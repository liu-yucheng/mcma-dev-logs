"""Step 1.2: stacking the slices gives (pi/4) * integral of x^2 from 0 to 4."""

import numpy as np
import sympy as sp

x = sp.symbols("x", positive=True)
exact = sp.integrate(x * sp.pi * x / 4, (x, 0, 4))
r = np.linspace(0, 1, 4001)
inner = r * 0.5 * (16.0 - 16.0 * r**4)
num = float(2.0 * np.pi * np.trapezoid(inner, r))
print("exact value:", exact, "=", float(exact))
print("numeric value:", round(num, 4))
assert abs(num - float(exact)) < 0.01
print("PASS 1.2")
