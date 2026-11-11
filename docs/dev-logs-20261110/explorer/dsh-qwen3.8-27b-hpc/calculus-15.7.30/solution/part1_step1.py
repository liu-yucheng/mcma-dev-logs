import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
f = 1  # all six orders with f = 1 must give the volume of the cylinder

# E: y^2 + z^2 <= 9,  -2 <= x <= 2
# Order 1: dx dy dz
I1 = sp.integrate(sp.integrate(sp.integrate(f, (x, -2, 2)),
                               (z, -sp.sqrt(9 - y**2), sp.sqrt(9 - y**2))),
                              (y, -3, 3))
# Order 2: dx dz dy
I2 = sp.integrate(sp.integrate(sp.integrate(f, (x, -2, 2)),
                               (y, -sp.sqrt(9 - z**2), sp.sqrt(9 - z**2))),
                              (z, -3, 3))
# Order 3: dy dx dz
I3 = sp.integrate(sp.integrate(sp.integrate(f, (y, -sp.sqrt(9 - z**2), sp.sqrt(9 - z**2))),
                               (x, -2, 2)),
                              (z, -3, 3))
# Order 4: dy dz dx
I4 = sp.integrate(sp.integrate(sp.integrate(f, (y, -sp.sqrt(9 - z**2), sp.sqrt(9 - z**2))),
                               (z, -3, 3)),
                              (x, -2, 2))
# Order 5: dz dx dy
I5 = sp.integrate(sp.integrate(sp.integrate(f, (z, -sp.sqrt(9 - y**2), sp.sqrt(9 - y**2))),
                               (x, -2, 2)),
                              (y, -3, 3))
# Order 6: dz dy dx
I6 = sp.integrate(sp.integrate(sp.integrate(f, (z, -sp.sqrt(9 - y**2), sp.sqrt(9 - y**2))),
                               (y, -3, 3)),
                              (x, -2, 2))

expected = 36*sp.pi
for name, I in [("dx dz dy", I1), ("dx dy dz", I2), ("dy dx dz", I3),
                ("dy dz dx", I4), ("dz dx dy", I5), ("dz dy dx", I6)]:
    v = sp.simplify(I)
    print(name, "->", v, " (float", float(v), ")")
    assert sp.simplify(v - expected) == 0, name
print("OK: all six orders equal 36*pi =", float(expected))
