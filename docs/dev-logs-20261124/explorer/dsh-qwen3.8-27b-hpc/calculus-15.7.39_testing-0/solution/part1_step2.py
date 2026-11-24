"""The moments of E are M_yz = 137/105, M_xz = 14/15, and M_xy = 571/210."""
import numpy as np
import sympy as sp

x, y = sp.symbols("x y")
top = 1 + x + y
Myz = sp.integrate(sp.integrate(2 * x * top, (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxz = sp.integrate(sp.integrate(2 * y * top, (y, 0, sp.sqrt(x))), (x, 0, 1))
Mxy = sp.integrate(sp.integrate(x * top**2, (y, 0, sp.sqrt(x))), (x, 0, 1))
print(f"M_yz exact = {Myz} = {float(Myz):.6f}")
print(f"M_xz exact = {Mxz} = {float(Mxz):.6f}")
print(f"M_xy exact = {Mxy} = {float(Mxy):.6f}")
n = 800
h = 1.0 / n
X, Y = np.meshgrid((np.arange(n) + 0.5) * h, (np.arange(n) + 0.5) * h, indexing="ij")
inD = (Y <= np.sqrt(X) + 1e-12).astype(float)
T = 1 + X + Y
Myz_n = np.sum(2 * X * T * inD) * h * h
Mxz_n = np.sum(2 * Y * T * inD) * h * h
Mxy_n = np.sum(X * T**2 * inD) * h * h
print(f"M_yz grid = {Myz_n:.6f}, M_xz grid = {Mxz_n:.6f}, M_xy grid = {Mxy_n:.6f}")
err = max(abs(float(Myz) - Myz_n), abs(float(Mxz) - Mxz_n), abs(float(Mxy) - Mxy_n))
assert err < 10 * h
print("PASS 1.2")
