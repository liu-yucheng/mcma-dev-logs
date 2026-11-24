"""Each ordering's inner integral is exact; the 2-D outer part is numeric and equals 4*pi."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
S = sp.sqrt
inner = {
    1: sp.integrate(1, (z, -S(4 - x**2 - y)/2, S(4 - x**2 - y)/2)),
    2: sp.integrate(1, (x, -S(4 - 4*z**2 - y), S(4 - 4*z**2 - y))),
    3: sp.integrate(1, (z, -S(4 - y - x**2)/2, S(4 - y - x**2)/2)),
    4: sp.integrate(1, (y, 0, 4 - x**2 - 4*z**2)),
    5: sp.integrate(1, (y, 0, 4 - x**2 - 4*z**2)),
    6: sp.integrate(1, (x, -S(4 - 4*z**2 - y), S(4 - 4*z**2 - y))),
}
print("inner forms: I1= sqrt, I2= 2 sqrt, I3= sqrt, I4= I5= dome height, I6= 2 sqrt")
V_target = 4.0*np.pi
n = 400
def w1(t):
    h = (t[-1] - t[0])/(len(t) - 1)
    w = np.full(len(t), h)
    w[0] = w[-1] = 0.5*h
    return w
def trap2(a, b, g, dom):
    A = np.linspace(a[0], a[1], n)
    B = np.linspace(b[0], b[1], n)
    GA, GB = np.meshgrid(A, B, indexing="ij")
    wA, wB = w1(A), w1(B)
    return float(np.sum(g(GA, GB) * dom(GA, GB) * wA[:, None] * wB[None, :]))
I1 = trap2((-2, 2), (0, 4), lambda a, b: np.sqrt(np.clip(4 - a**2 - b, 0, None)), lambda a, b: (a**2 + b <= 4).astype(float))
I2 = trap2((-1, 1), (0, 4), lambda a, b: 2*np.sqrt(np.clip(4 - 4*a**2 - b, 0, None)), lambda a, b: (4*a**2 + b <= 4).astype(float))
I3 = trap2((0, 4), (-2, 2), lambda a, b: np.sqrt(np.clip(4 - a - b**2, 0, None)), lambda a, b: (a + b**2 <= 4).astype(float))
I4 = trap2((-2, 2), (-1, 1), lambda a, b: np.clip(4 - a**2 - 4*b**2, 0, None), lambda a, b: (a**2 + 4*b**2 <= 4).astype(float))
I5 = trap2((-1, 1), (-2, 2), lambda a, b: np.clip(4 - b**2 - 4*a**2, 0, None), lambda a, b: (b**2 + 4*a**2 <= 4).astype(float))
I6 = trap2((0, 4), (-1, 1), lambda a, b: 2*np.sqrt(np.clip(4 - 4*b**2 - a, 0, None)), lambda a, b: (a + 4*b**2 <= 4).astype(float))
print(f"grid n = {n}, tol = 0.08, target 4*pi = {V_target:.6f}")
for i, val in enumerate([I1, I2, I3, I4, I5, I6], 1):
    print(f"I{i} = {val:.6f}")
    assert abs(val - V_target) < 0.08, f"I{i} deviates from 4*pi"
print("PASS 2.1")
