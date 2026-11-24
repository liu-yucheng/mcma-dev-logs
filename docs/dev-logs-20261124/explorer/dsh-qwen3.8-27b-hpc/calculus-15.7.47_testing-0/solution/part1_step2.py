"""Step 1.2: the center of mass is (0, My/M, Mz/M)."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
rho = sp.sqrt(x**2 + y**2)

def inner(f):
    return sp.integrate(sp.integrate(f, (z, 0, 1 - y)), (x, -sp.sqrt(y), sp.sqrt(y)))

M = sp.integrate(inner(rho), (y, 0, 1))
Mx = sp.integrate(inner(x * rho), (y, 0, 1))
My = sp.integrate(inner(y * rho), (y, 0, 1))
Mz = sp.integrate(inner(z * rho), (y, 0, 1))
ybar, zbar = sp.simplify(My / M), sp.simplify(Mz / M)
print("xbar exact:", Mx, " ybar:", sp.N(ybar, 12), " zbar:", sp.N(zbar, 12))
rng = np.random.default_rng(2)
X = rng.uniform(-1, 1, 400000)
Y = rng.uniform(0, 1, 400000)
Z = rng.uniform(0, 1, 400000)
iv = (X * X <= Y) & (Z <= 1 - Y)
w = 2.0 * np.sqrt(X * X + Y * Y) * iv
ybar_mc = float(np.mean(Y * w) / np.mean(w))
zbar_mc = float(np.mean(Z * w) / np.mean(w))
Mx_mc = 2.0 * float(np.mean(X * w))
print("MC ybar zbar Mx:", round(ybar_mc, 6), round(zbar_mc, 6), round(Mx_mc, 6))
assert abs(ybar_mc - float(ybar)) < 0.004 and abs(zbar_mc - float(zbar)) < 0.004 and abs(Mx_mc) < 0.003
print("PASS 1.2")
