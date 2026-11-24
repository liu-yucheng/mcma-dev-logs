"""Step 1.1: the inner integral over r equals (2/3)a^3 (1 - |sin theta|^3)."""

import numpy as np
import sympy as sp

a, r, th = sp.symbols("a r theta", positive=True)
inner = sp.integrate(2 * r * sp.sqrt(a**2 - r**2), (r, 0, a * sp.cos(th)))
print("sympy inner integral:", sp.simplify(inner))
closed = lambda tv: (2.0 / 3.0) * (1.0 - abs(np.sin(tv)) ** 3)
worst = 0.0
for tv in [0.0, 0.3, 0.9, 1.2, float(np.pi / 2)]:
    rr = np.linspace(0.0, np.cos(tv), 20001)
    num = float(np.trapezoid(2.0 * rr * np.sqrt(np.maximum(1.0 - rr**2, 0.0)), rr))
    worst = max(worst, abs(num - closed(tv)))
print("max trapezoid error (a = 1):", round(worst, 7))
assert worst < 1e-4
print("PASS 1.1")
