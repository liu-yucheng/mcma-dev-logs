"""Step 1.2: the exact volume is 136*pi/99; a Gauss rule confirms it."""

import numpy as np
import sympy as sp

th, ph = sp.symbols("theta phi", positive=True)
rho = 1 + sp.Rational(1, 5) * sp.sin(6 * th) * sp.sin(5 * ph)
V = sp.Rational(1, 3) * sp.integrate(sp.integrate(sp.expand(rho**3) * sp.sin(ph), (ph, 0, sp.pi)), (th, 0, 2 * sp.pi))
print("V exact:", sp.simplify(V), "=", round(float(V), 6))
for term in sp.Add.make_args(sp.expand(rho**3)):
    it = sp.integrate(sp.integrate(term * sp.sin(ph), (ph, 0, sp.pi)), (th, 0, 2 * sp.pi))
    print("term", sp.simplify(term), "integral =", sp.simplify(it))

x, w = np.polynomial.legendre.leggauss(160)
wT = w * np.pi
wP = w * (np.pi / 2)
T = np.pi * (x + 1.0)
P = 0.5 * np.pi * (x + 1.0)
F = (1.0 + 0.2 * np.sin(6.0 * T[:, None]) * np.sin(5.0 * P[None, :])) ** 3 * np.sin(P[None, :])
V_num = float((wT @ F) @ wP / 3.0)
print("gauss volume:", round(V_num, 9))
assert sp.simplify(V - 136 * sp.pi / 99) == 0
assert abs(V_num - float(V)) < 1e-6
print("PASS 1.2")
