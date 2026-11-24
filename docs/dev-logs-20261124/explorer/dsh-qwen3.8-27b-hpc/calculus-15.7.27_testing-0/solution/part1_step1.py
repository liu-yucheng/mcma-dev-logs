"""Step 1: the solid is 0<=x<=1, 0<=z<=1-x, 0<=y<=2(1-z); a pyramid with 4 base corners and apex (0,0,1)."""
import itertools
import numpy as np
import sympy as sp

x, y, z = sp.symbols("x y z")
planes = [x, y, z, 1 - x - z, 2 - y - 2 * z]  # each face as f >= 0
verts = set()
for tri in itertools.combinations(planes, 3):
    for s in sp.solve([sp.Eq(p, 0) for p in tri], [x, y, z], dict=True):
        pt = (sp.simplify(s[x]), sp.simplify(s[y]), sp.simplify(s[z]))
        if all(v >= 0 for v in pt) and all(sp.simplify(p.subs(s)) >= 0 for p in planes):
            verts.add(pt)
verts = sorted(verts)
base = [v for v in verts if v[2] == 0]
apex = [v for v in verts if v[2] == 1]
print("corners:", verts)
print("base (z=0):", base)
print("apex:", apex)
for zv in (0, sp.Rational(1, 2), 1):
    print(f"section z={zv}: x in [0, {1 - zv}], y in [0, {2 - 2 * zv}]")
o = sp.Matrix(base[0])
area = sp.simplify((sp.Matrix(base[1]) - o).cross(sp.Matrix(base[2]) - o).norm())
Vpyr = sp.Rational(1, 3) * area * 1  # apex height above z = 0
print("base area =", area, " pyramid V =", Vpyr)
rng = np.random.default_rng(7)
P = rng.random((300000, 3))
X, Y, Z = P[:, 0], 2 * P[:, 1], P[:, 2]
inS = (X <= 1) & (Z <= 1 - X) & (Y <= 2 - 2 * Z)
Vmc = float(inS.mean()) * 2.0
print("MC volume =", Vmc)
assert abs(float(Vpyr) - Vmc) < 0.03
print("PASS 1.1")
