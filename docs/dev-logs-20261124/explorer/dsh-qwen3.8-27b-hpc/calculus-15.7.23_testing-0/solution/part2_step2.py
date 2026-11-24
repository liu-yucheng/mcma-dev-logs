"""The exact volume is pi/4 - 1/3; a Monte Carlo pass over the unit cube agrees."""
import sympy as sp
import numpy as np

z, y, x = sp.symbols("z y x", nonnegative=True)
V = sp.simplify(sp.integrate(sp.integrate(sp.integrate(1, (z, 0, sp.sqrt(1 - y**2))), (y, 0, x)), (x, 0, 1)))
closed = sp.Rational(1, 4) * sp.pi - sp.Rational(1, 3)
assert sp.simplify(V - closed) == 0, "closed form"
t1 = sp.Rational(1, 2) * sp.integrate(x * sp.sqrt(1 - x**2), (x, 0, 1))
t2 = sp.Rational(1, 2) * (sp.pi / 2 - 1)
print("term1 =", t1, "=", float(t1), " term2 =", t2, "=", float(t2))
print("V =", V, "=", float(V))

rng = np.random.default_rng(7)
n = 300000
p = rng.random((n, 3))
hit = (p[:, 1] <= p[:, 0]) & (p[:, 1] ** 2 + p[:, 2] ** 2 <= 1)
est = float(hit.mean())
sig = float(hit.std()) / np.sqrt(n)
print(f"monte carlo {est:.6f} sigma {sig:.6f}")
assert abs(est - float(closed)) < 4 * sig, "monte carlo"
print("PASS 2.2")
