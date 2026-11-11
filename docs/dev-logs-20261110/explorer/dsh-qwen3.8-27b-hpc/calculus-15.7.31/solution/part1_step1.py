import sympy as sp

x, y, z = sp.symbols('x y z', real=True)
f = 1  # all six orders with f = 1 must give the volume of E

# E: x^2 <= y <= 4 - 2z,  z >= 0   (equivalently: x^2 <= y <= 4, 0 <= z <= (4-y)/2)
#
# Order 1: dx dy dz  (z 0..2 outer, y 0..4-2z middle, x -sqrt(y)..sqrt(y) inner)
I1 = sp.integrate(sp.integrate(sp.integrate(f, (x, -sp.sqrt(y), sp.sqrt(y))),
                               (y, 0, 4 - 2*z)),
                              (z, 0, 2))
# Order 2: dx dz dy  (y 0..4 outer, z 0..(4-y)/2 middle, x -sqrt(y)..sqrt(y) inner)
I2 = sp.integrate(sp.integrate(sp.integrate(f, (x, -sp.sqrt(y), sp.sqrt(y))),
                               (z, 0, (4 - y)/2)),
                              (y, 0, 4))
# Order 3: dy dx dz  (z 0..2 outer, x -sqrt(4-2z)..sqrt(4-2z) middle, y x^2..4-2z inner)
I3 = sp.integrate(sp.integrate(sp.integrate(f, (y, x**2, 4 - 2*z)),
                               (x, -sp.sqrt(4 - 2*z), sp.sqrt(4 - 2*z))),
                              (z, 0, 2))
# Order 4: dy dz dx  (x -2..2 outer, z 0..(4-x^2)/2 middle, y x^2..4-2z inner)
I4 = sp.integrate(sp.integrate(sp.integrate(f, (y, x**2, 4 - 2*z)),
                               (z, 0, (4 - x**2)/2)),
                              (x, -2, 2))
# Order 5: dz dx dy  (y 0..4 outer, x -sqrt(y)..sqrt(y) middle, z 0..(4-y)/2 inner)
I5 = sp.integrate(sp.integrate(sp.integrate(f, (z, 0, (4 - y)/2)),
                               (x, -sp.sqrt(y), sp.sqrt(y))),
                              (y, 0, 4))
# Order 6: dz dy dx  (x -2..2 outer, y x^2..4 middle, z 0..(4-y)/2 inner)
I6 = sp.integrate(sp.integrate(sp.integrate(f, (z, 0, (4 - y)/2)),
                               (y, x**2, 4)),
                              (x, -2, 2))

expected = sp.Rational(128, 15)
for name, I in [("dx dy dz", I1), ("dx dz dy", I2), ("dy dx dz", I3),
                ("dy dz dx", I4), ("dz dx dy", I5), ("dz dy dx", I6)]:
    v = sp.simplify(I)
    print(name, "->", v, " (float", float(v), ")")
    assert sp.simplify(v - expected) == 0, name
print("OK: all six orders equal 128/15 =", float(expected))
