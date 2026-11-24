"""Each of the six iterated integral orderings integrates to the exact volume 36*pi of E."""
import math
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
Ry = sp.sqrt(9 - y**2)
Rz = sp.sqrt(9 - z**2)
forms = [
    ("dz dy dx", sp.Integral(1, (z, -Ry, Ry), (y, -3, 3), (x, -2, 2))),
    ("dy dz dx", sp.Integral(1, (y, -Rz, Rz), (z, -3, 3), (x, -2, 2))),
    ("dx dy dz", sp.Integral(1, (x, -2, 2), (z, -Ry, Ry), (y, -3, 3))),
    ("dx dz dy", sp.Integral(1, (x, -2, 2), (y, -Rz, Rz), (z, -3, 3))),
    ("dz dx dy", sp.Integral(1, (z, -Ry, Ry), (x, -2, 2), (y, -3, 3))),
    ("dy dx dz", sp.Integral(1, (y, -Rz, Rz), (x, -2, 2), (z, -3, 3))),
]
V_geom = 4 * sp.pi * 3**2
for name, I in forms:
    val = I.doit()
    assert sp.simplify(val - V_geom) == 0, name
    print(name, "=", val)
n = 20000
zs = [-3.0 + 6.0 * k / n for k in range(n + 1)]
trap = sum(0.5 * (2 * math.sqrt(9 - a*a) + 2 * math.sqrt(9 - b*b)) * (b - a)
           for a, b in zip(zs, zs[1:]))
V_num = 4.0 * trap
print("trapezoid dy dz dx =", round(V_num, 6), "exact =", float(V_geom))
assert abs(V_num - float(V_geom)) < 1e-3
print("PASS 1.2")
