"""The dz dy dx order is valid; trapezoid passes in the same order match the exact chain."""
import sympy as sp
import numpy as np

z, y, x = sp.symbols("z y x", nonnegative=True)
inner = sp.integrate(1, (z, 0, sp.sqrt(1 - y**2)))
mid = sp.simplify(sp.integrate(inner, (y, 0, x)))
V = sp.simplify(sp.integrate(mid, (x, 0, 1)))
print("middle integral A(x) =", mid)
print("V exact =", V, "=", float(V))
print("A(1) =", float(mid.subs(x, 1)))

trap = getattr(np, "trapezoid", np.trapz)
xs = np.linspace(0, 1, 401)
col = np.empty(401)
for i, xv in enumerate(xs):
    if xv > 0:
        ys = np.linspace(0, xv, 200)
        col[i] = float(trap(np.sqrt(np.clip(1 - ys**2, 0, None)), ys))
    else:
        col[i] = 0.0
V_num = float(trap(col, xs))
print(f"trapezoid V = {V_num:.8f}")
assert abs(V_num - float(V)) < 5e-4, "order check"
print("PASS 1.2")
