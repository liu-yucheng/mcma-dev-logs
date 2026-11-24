"""The base D has area 2/3, the solid volume is 79/60, and the mass is 79/30."""
import numpy as np
import sympy as sp

x, y = sp.symbols("x y")
top = 1 + x + y
area = sp.integrate(sp.sqrt(x), (x, 0, 1))
V = sp.integrate(sp.integrate(top, (y, 0, sp.sqrt(x))), (x, 0, 1))
M = 2 * V
print(f"area exact = {area}, V exact = {V} = {float(V):.6f}, mass exact = {M} = {float(M):.6f}")
for z0 in (0.5, 1.0, 1.5):
    c = z0 - 1
    if c <= 0:
        print(f"section at z = {z0}: full base D, corners (0,0),(1,0),(1,1)")
    else:
        u = float((-1 + np.sqrt(1 + 4 * c)) / 2)
        print(f"section at z = {z0}: corners ({c},0),(1,0),(1,1),({u**2:.4f},{u:.4f})")
n = 800
h = 1.0 / n
X, Y = np.meshgrid((np.arange(n) + 0.5) * h, (np.arange(n) + 0.5) * h, indexing="ij")
inD = (Y <= np.sqrt(X) + 1e-12).astype(float)
Vn = np.sum((1 + X + Y) * inD) * h * h
Mn = 2.0 * Vn
print(f"V grid = {Vn:.6f}, mass grid = {Mn:.6f}")
assert abs(float(M) - Mn) < 10 * h
print("PASS 1.1")
