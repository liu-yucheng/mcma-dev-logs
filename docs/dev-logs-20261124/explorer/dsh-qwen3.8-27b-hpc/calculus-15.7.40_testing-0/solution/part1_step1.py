"""The solid E has volume 4/5 and mass 16/5 under the parabolic cylinder."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
V = sp.integrate(1, (x, 0, 1 - z), (y, -sp.sqrt(1 - z), sp.sqrt(1 - z)), (z, 0, 1))
M = 4 * V
print(f"volume exact = {V} = {float(V):.6f}, mass exact = {M} = {float(M):.6f}")
for z0 in (0.0, 0.25, 0.75):
    a = 1 - z0
    s = np.sqrt(a)
    print(f"section at z = {z0}: corners (0,-{s:.4f}),(0,{s:.4f}),({a:.4f},{s:.4f}),({a:.4f},-{s:.4f})")
n = 120
dx = 1.0 / n; dy = 2.0 / n; dz = 1.0 / n
X, Y, Z = np.meshgrid((np.arange(n) + 0.5) * dx, -1 + (np.arange(n) + 0.5) * dy,
                      (np.arange(n) + 0.5) * dz, indexing="ij")
ind = ((Z <= 1 - Y**2) & (X <= 1 - Z)).astype(float)
Vn = np.sum(ind) * dx * dy * dz
print(f"volume grid = {Vn:.6f}, mass grid = {4 * Vn:.6f}")
assert abs(float(M) - 4 * Vn) < 10 * dx
print("PASS 1.1")
