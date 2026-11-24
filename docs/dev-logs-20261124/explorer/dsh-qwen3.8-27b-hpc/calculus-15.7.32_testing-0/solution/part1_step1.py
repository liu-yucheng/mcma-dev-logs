"""Step 1.1: E is the tetrahedron bounded by x=2, y=2, z=0, x+y-2z=2, with volume 2/3.
"""
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
top = (x + y) / 2 - 1
V = sp.integrate(sp.integrate(top, (y, 2 - x, 2)), (x, 0, 2))
A = sp.Matrix([[0, -2, 0], [-2, 0, 0], [0, 0, 1]])
V3d = sp.Rational(1, 6) * abs(A.det())
for zz in [sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)]:
    corners = [(2, 2 * zz), (2 * zz, 2), (2, 2)]
    print("z =", zz, " section corners:", [tuple(map(float, c)) for c in corners])
rng = np.random.default_rng(2026)
P = 400000
pts = rng.uniform([0, 0, 0], [2, 2, 1], (P, 3))
hit = pts[:, 2] <= (pts[:, 0] + pts[:, 1]) / 2 - 1
Vmc = 4.0 * float(hit.mean())
print("V exact =", V, "=", float(sp.N(V, 9)), " V 3D law =", V3d, " V mc =", round(Vmc, 6))
assert abs(Vmc - float(V)) < 1e-2
assert V == sp.Rational(2, 3)
print("PASS 1.1")
