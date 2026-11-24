"""A Monte Carlo pass over the box [-2,2]x[-1,6]x[-2,2] confirms the volume 20*pi."""
import numpy as np
import sympy as sp

n = 400000
print("n =", n)
rng = np.random.default_rng(22)
x = rng.uniform(-2, 2, n)
y = rng.uniform(-1, 6, n)
z = rng.uniform(-2, 2, n)
in_solid = (x**2 + z**2 <= 4) & (y >= -1) & (y <= 4 - z)
V_box = 4 * 7 * 4
print("box volume =", V_box)
est = float(in_solid.sum()) / n * V_box
exact = float(20*sp.pi)
print("estimate =", round(est, 3), "exact =", round(exact, 4))
assert abs(est - exact) < 0.2
print("PASS 1.3")
