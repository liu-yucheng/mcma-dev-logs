"""The center of mass of E is (5/14, 0, 2/7), checked by Monte Carlo."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
B = (y, -sp.sqrt(1 - z), sp.sqrt(1 - z))
V = sp.integrate(1, (x, 0, 1 - z), B, (z, 0, 1))
M = 4 * V
Myz = sp.integrate(4 * x, (x, 0, 1 - z), B, (z, 0, 1))
Mxy = sp.integrate(4 * z, (x, 0, 1 - z), B, (z, 0, 1))
cx, cy, cz = Myz / M, 0, Mxy / M
print(f"center exact = ({cx}, {cy}, {cz})")
print(f"center decimal = ({float(cx):.6f}, {float(cy):.6f}, {float(cz):.6f})")
rng = np.random.default_rng(7)
N = 300000
X = rng.uniform(0, 1, N); Y = rng.uniform(-1, 1, N); Z = rng.uniform(0, 1, N)
keep = (Z <= 1 - Y**2) & (X <= 1 - Z)
mx, my, mz = X[keep].mean(), Y[keep].mean(), Z[keep].mean()
print(f"Monte Carlo = ({mx:.6f}, {my:.6f}, {mz:.6f}), kept = {int(keep.sum())}")
assert max(abs(float(cx) - mx), abs(cy - my), abs(float(cz) - mz)) < 0.01
print("PASS 1.3")
