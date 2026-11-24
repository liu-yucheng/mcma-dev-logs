"""The center of mass of E is (358/553, 33/79, 337/474), checked by Monte Carlo."""
import numpy as np
import sympy as sp

x, y = sp.symbols("x y")
top = 1 + x + y
V = sp.integrate(sp.integrate(top, (y, 0, sp.sqrt(x))), (x, 0, 1))
Myz = sp.integrate(sp.integrate(2 * x * top, (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxz = sp.integrate(sp.integrate(2 * y * top, (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxy = sp.integrate(sp.integrate(x * top**2, (y, 0, sp.sqrt(x))), (x, 0, 1))
M = 2 * V
cx, cy, cz = Myz / M, Mxz / M, Mxy / M
print(f"center exact = ({cx}, {cy}, {cz})")
print(f"center decimal = ({float(cx):.6f}, {float(cy):.6f}, {float(cz):.6f})")
rng = np.random.default_rng(42)
N = 400000
X = rng.uniform(0, 1, N); Y = rng.uniform(0, 1, N)
keep = Y <= np.sqrt(X)
Xk, Yk = X[keep], Y[keep]
T = 1 + Xk + Yk
mx = np.sum(2 * Xk * T) / np.sum(2 * T)
my = np.sum(2 * Yk * T) / np.sum(2 * T)
mz = np.sum(Xk * T**2) / np.sum(2 * T)
print(f"Monte Carlo = ({mx:.6f}, {my:.6f}, {mz:.6f}), kept = {int(keep.sum())}")
assert max(abs(float(cx) - mx), abs(float(cy) - my), abs(float(cz) - mz)) < 0.01
print("PASS 1.3")
