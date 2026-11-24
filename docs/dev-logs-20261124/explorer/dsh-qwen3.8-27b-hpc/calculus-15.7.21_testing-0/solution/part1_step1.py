"""Print the base region D and verify its area."""
import numpy as np
import sympy as sp
y0 = sp.symbols("y0", positive=True)
a = 2 * sp.sqrt(y0)
A = sp.integrate(a, (y0, 0, 1))
print("exact area(D) =", A)
print("cross section y0=0: corner x=0; length=0")
print("cross section y0=1/4: corners x=-1/2, 1/2; length=1")
print("cross section y0=1: corners x=-1, 1; length=2")
n = 2000
ys = np.linspace(0, 1, n + 1)
mid = ys[:-1] + 0.5 * (ys[1] - ys[0])
area_grid = float(np.trapz(2 * np.sqrt(mid), mid))
print("numeric area(D) =", area_grid)
rng = np.random.default_rng(7)
xs = rng.uniform(-1, 1, 600_000)
ysm = rng.uniform(0, 1, 600_000)
hit = np.mean(xs ** 2 <= ysm)
area_mc = float(hit) * 2
print("monte carlo area(D) =", area_mc)
assert abs(area_grid - float(A)) < 50 / n, (area_grid, float(A))
print("PASS 1.1")
