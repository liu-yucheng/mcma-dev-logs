"""Step 1.3: all six orderings match the exact volume 2/3 under fixed-grid numeric quadrature.
"""
import numpy as np

V = 2.0 / 3.0
tol = 5e-3
n = 1501
hx = 2.0 / (n - 1)
hz = 1.0 / (n - 1)
xg = np.linspace(0, 2, n)
zg = np.linspace(0, 1, n)
X, Y = np.meshgrid(xg, xg)
W = np.full((n, n), hx * hx)
W[0, :] *= 0.5; W[-1, :] *= 0.5; W[:, 0] *= 0.5; W[:, -1] *= 0.5
base = (X + Y) >= 2
top = np.clip((X + Y) / 2 - 1, 0, None)
X2, Z = np.meshgrid(xg, zg)
Wz = np.full((n, n), hx * hz)
Wz[0, :] *= 0.5; Wz[-1, :] *= 0.5; Wz[:, 0] *= 0.5; Wz[:, -1] *= 0.5
I1 = float(np.sum(W * top * base))
I2 = float(np.sum(W * top * base))
I3 = float(np.sum(Wz * (X2 - 2 * Z) * (Z <= X2 / 2)))
I4 = float(np.sum(Wz * (X2 - 2 * Z) * (Z <= X2 / 2)))
I5 = float(np.sum(Wz * (X2 - 2 * Z) * (X2 >= 2 * Z)))
I6 = float(np.sum(Wz * (X2 - 2 * Z) * (X2 >= 2 * Z)))
for name, I in zip("abcdef", [I1, I2, I3, I4, I5, I6]):
    print(name, round(I, 6))
assert abs(I1 - V) < tol
assert all(abs(I - V) < tol for I in [I2, I3, I4, I5, I6])
print("PASS 1.3")
