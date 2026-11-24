"""The exact volume is 20/3, matching a trapezoid sum of the slice area over y."""
import sympy as sp
import numpy as np
x, z, y = sp.symbols("x z y")
V_exact = sp.integrate(sp.integrate(sp.integrate(1, (x, 0, 4 - y**2)), (z, 0, 2 - y)), (y, 0, 2))
A = (4 - y**2) * (2 - y)
print("expanded slice area:", sp.expand(A))
print("exact volume:", V_exact, "=", float(V_exact))
print("rounded:", "%.6f" % float(V_exact))
yy = np.linspace(0.0, 2.0, 401)
A_n = (4 - yy**2) * (2 - yy)
trap = getattr(np, "trapezoid", np.trapz)
V_num = float(trap(A_n, yy))
print("trapezoid volume:", V_num)
assert abs(float(V_exact) - V_num) < 1e-3
print("PASS 1.2")
