"""Print the cross section A(y0) and verify its mean value."""
import numpy as np
import sympy as sp
y0 = sp.symbols("y0", positive=True)
width = 2 * sp.sqrt(y0)
height = 1 - y0
A = sp.simplify(width * height)
print("A(y0) =", A)
E = sp.integrate(height, (y0, 0, 1))
print("E[(1-y0)] =", E)
n = 2000
ys = np.linspace(0, 1, n + 1)
mid = ys[:-1] + 0.5 * (ys[1] - ys[0])
E_num = float(np.trapz(1 - mid, mid))
print("numeric E =", E_num)
rng = np.random.default_rng(11)
ysm = rng.uniform(0, 1, 600_000)
E_mc = float(np.mean(1 - ysm))
print("monte carlo E =", E_mc)
assert abs(E_num - float(E)) < 50 / n, (E_num, float(E))
assert abs(E_mc - float(E)) < 0.03, (E_mc, float(E))
print("PASS 1.2")
