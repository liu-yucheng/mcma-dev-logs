"""All six orderings match 4*pi by nested trapezoid rules on 500-point grids."""
import numpy as np

n = 500
V_target = 4.0*np.pi
def w1(t):
    h = (t[-1] - t[0])/(len(t) - 1)
    w = np.full(len(t), h)
    w[0] = w[-1] = 0.5*h
    return w
X = np.linspace(-2, 2, n)
Y = np.linspace(0, 4, n)
Z = np.linspace(-1, 1, n)
wx, wy, wz = w1(X), w1(Y), w1(Z)
def g2(A, B, wA, wB, fn):
    GA, GB = np.meshgrid(A, B, indexing="ij")
    return float(np.sum(fn(GA, GB) * wA[:, None] * wB[None, :]))
I1 = g2(X, Y, wx, wy, lambda a, b: np.sqrt(np.clip(4 - a**2 - b, 0.0, None)))
I2 = g2(Z, Y, wz, wy, lambda a, b: 2.0*np.sqrt(np.clip(4 - 4*a**2 - b, 0.0, None)))
I3 = g2(Y, X, wy, wx, lambda a, b: np.sqrt(np.clip(4 - a - b**2, 0.0, None)))
I4 = g2(X, Z, wx, wz, lambda a, b: np.clip(4 - a**2 - 4*b**2, 0.0, None))
I5 = g2(Z, X, wz, wx, lambda a, b: np.clip(4 - b**2 - 4*a**2, 0.0, None))
I6 = g2(Y, Z, wy, wz, lambda a, b: 2.0*np.sqrt(np.clip(4 - 4*b**2 - a, 0.0, None)))
print(f"grid n = {n}, tol = 0.08")
for i, val in enumerate([I1, I2, I3, I4, I5, I6], 1):
    print(f"I{i} = {val:.6f}")
    assert abs(val - V_target) < 0.08, f"I{i} deviates from 4*pi"
print("PASS 3.1")
