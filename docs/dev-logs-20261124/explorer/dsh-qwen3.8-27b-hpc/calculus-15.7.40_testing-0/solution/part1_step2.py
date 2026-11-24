"""The moments of E are M_yz = 8/7, M_xz = 0, and M_xy = 32/35."""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
B = (y, -sp.sqrt(1 - z), sp.sqrt(1 - z))
Myz = sp.integrate(4 * x, (x, 0, 1 - z), B, (z, 0, 1))
Mxz = sp.integrate(4 * y, (x, 0, 1 - z), B, (z, 0, 1))
Mxy = sp.integrate(4 * z, (x, 0, 1 - z), B, (z, 0, 1))
print(f"M_yz exact = {Myz} = {float(Myz):.6f}")
print(f"M_xz exact = {Mxz} = {float(Mxz):.6f}")
print(f"M_xy exact = {Mxy} = {float(Mxy):.6f}")
n = 120
dx = 1.0 / n; dy = 2.0 / n; dz = 1.0 / n
X, Y, Z = np.meshgrid((np.arange(n) + 0.5) * dx, -1 + (np.arange(n) + 0.5) * dy,
                      (np.arange(n) + 0.5) * dz, indexing="ij")
ind = ((Z <= 1 - Y**2) & (X <= 1 - Z)).astype(float)
w = dx * dy * dz
Myz_n = np.sum(4 * X * ind) * w
Mxz_n = np.sum(4 * Y * ind) * w
Mxy_n = np.sum(4 * Z * ind) * w
print(f"M_yz grid = {Myz_n:.6f}, M_xz grid = {Mxz_n:.6f}, M_xy grid = {Mxy_n:.6f}")
err = max(abs(float(Myz) - Myz_n), abs(float(Mxz) - Mxz_n), abs(float(Mxy) - Mxy_n))
assert err < 10 * dx
print("PASS 1.2")
