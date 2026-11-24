"""The cross section of the cylinder x^2+z^2=4 is a disk of radius 2 with area 4*pi."""
import math
import numpy as np
import sympy as sp

r, th = sp.symbols("r theta", real=True)
area = sp.integrate(sp.integrate(r, (r, 0, 2)), (th, 0, 2*sp.pi))
print("exact area =", area, "=", float(area))
for y in (-1, 2.5, 6):
    ztop = min(2.0, 4.0 - y)
    print("slice y =", y, ": x in [-2, 2], z in [-2, %.1f]" % ztop)
print("corners at y=-1:", [(-2, 0), (0, 2), (2, 0), (0, -2)])
print("corners at y=6:", [(0, -2)])
n1 = np.array([0.0, 1.0, 0.0])
n2 = np.array([0.0, 1.0, 1.0])
ang = math.degrees(math.acos(float(n1 @ n2) / (np.linalg.norm(n1) * np.linalg.norm(n2))))
print("angle between the two planes (deg) =", round(ang, 1))
n = 400
xs = np.linspace(-2, 2, n)
zs = np.linspace(-2, 2, n)
dx = xs[1] - xs[0]
X, Z = np.meshgrid(xs, zs)
num = float(np.sum(X**2 + Z**2 <= 4)) * dx**2
print("grid area =", num)
assert abs(num - float(area)) < 0.02
print("PASS 1.1")
