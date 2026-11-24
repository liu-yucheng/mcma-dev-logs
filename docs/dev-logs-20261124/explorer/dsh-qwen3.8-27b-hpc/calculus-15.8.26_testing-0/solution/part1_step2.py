"""Step 1.2: the theta integral gives V = (6*pi - 8)/9 for a = 1."""

import numpy as np
import sympy as sp

th = sp.symbols("theta")
exact = 2 * sp.Rational(2, 3) * sp.integrate(1 - sp.sin(th) ** 3, (th, 0, sp.pi / 2))
print("exact volume (a = 1):", exact, "=", float(exact))
rng = np.random.default_rng(11)
n = 2_000_000
box = rng.uniform(-1.0, 1.0, (n, 3))
keep = (box ** 2).sum(axis=1) <= 1.0
p = box[keep]
hit = (p[:, 0] - 0.5) ** 2 + p[:, 1] ** 2 <= 0.25
vol = (4.0 / 3.0) * np.pi * float(hit.sum()) / float(keep.sum())
print("monte carlo volume:", round(vol, 4), "kept:", int(keep.sum()))
assert abs(vol - float(exact)) < 0.02
print("PASS 1.2")
