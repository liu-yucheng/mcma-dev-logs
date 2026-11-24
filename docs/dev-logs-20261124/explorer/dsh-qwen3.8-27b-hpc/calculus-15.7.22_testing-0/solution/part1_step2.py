"""The triple integral with y from -1 to 4-z over the disk x^2+z^2<=4 equals 20*pi."""
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", real=True)
y = sp.Symbol("y")
# polar: x = r*cos(th), z = r*sin(th); disk radius 2 in the xz-plane
V = sp.integrate(sp.integrate(sp.integrate(1, (y, -1, 4 - r*sp.sin(th))),
                              (r, 0, 2)), (th, 0, 2*sp.pi))
print("exact volume =", V, "=", float(V))
n = 800
xs = np.linspace(-2, 2, n)
zs = np.linspace(-2, 2, n)
dx = xs[1] - xs[0]
X, Z = np.meshgrid(xs, zs)
height = np.where(X**2 + Z**2 <= 4, (4 - Z) - (-1), 0.0)
num = float(np.sum(height)) * dx**2
print("grid volume =", num)
assert abs(num - float(V)) < 0.02
print("PASS 1.2")
