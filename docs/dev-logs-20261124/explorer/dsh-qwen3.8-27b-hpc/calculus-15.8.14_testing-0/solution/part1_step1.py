"""The two paraboloids meet at the circle r=sqrt(5/2), z=5/2, and the enclosed volume is 25*pi/4."""
import numpy as np
import sympy as sp

r, t = sp.symbols("r t", positive=True)
r_i = sp.solve(sp.Eq(r**2, 5 - r**2), r)[0]
z_i = sp.simplify(r_i**2)
V = sp.simplify(sp.integrate(sp.integrate((5 - 2*r**2)*r, (r, 0, r_i)), (t, 0, 2*sp.pi)))
a = float(r_i)
n = 4000
rg = np.linspace(0.0, a, n + 1)
f = (5.0 - 2.0*rg**2)*rg
h = a / n
Vnum = h*(0.5*f[0] + f[1:-1].sum() + 0.5*f[-1])*2.0*np.pi
print("r_intersection =", round(a, 4))
print("z_intersection =", float(z_i))
print("V_exact =", V, "=", round(float(V), 4))
print("V_trapz =", round(Vnum, 4), " n =", n)
assert abs(Vnum - float(V)) <= 10*h, "volume mismatch"
print("PASS 1.1")
