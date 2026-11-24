"""The CAS antiderivatives of sqrt(1-y^2) and x sqrt(1-x^2) differentiate to the integrands."""
import sympy as sp
import numpy as np

y, x = sp.symbols("y x", nonnegative=True)
F1 = sp.simplify(sp.integrate(sp.sqrt(1 - y**2), y))
F2 = sp.simplify(sp.integrate(x * sp.sqrt(1 - x**2), x))
print("F1(y) =", F1)
print("F2(x) =", F2)

h = 1e-5
yy = np.linspace(0.1, 0.9, 17)
d1 = np.array([float((F1.subs(y, v + h) - F1.subs(y, v - h)) / (2 * h)) for v in yy])
g1 = np.sqrt(1 - yy**2)
print("max |F1' - g1| =", float(np.max(np.abs(d1 - g1))))
assert np.max(np.abs(d1 - g1)) < 1e-4, "F1 derivative"

xx = np.linspace(0.1, 0.9, 17)
d2 = np.array([float((F2.subs(x, v + h) - F2.subs(x, v - h)) / (2 * h)) for v in xx])
g2 = xx * np.sqrt(1 - xx**2)
print("max |F2' - g2| =", float(np.max(np.abs(d2 - g2))))
assert np.max(np.abs(d2 - g2)) < 1e-4, "F2 derivative"
print("PASS 2.1")
