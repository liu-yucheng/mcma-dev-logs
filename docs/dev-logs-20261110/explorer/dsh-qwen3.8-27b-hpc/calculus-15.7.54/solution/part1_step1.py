"""Average value of f(x,y,z) = x^2 z + y^2 z over E for problem 15.7.54.

E: enclosed by the paraboloid z = 1 - x^2 - y^2 and the plane z = 0.
In polar: x = r cos t, y = r sin t, 0 <= r <= 1, 0 <= t <= 2 pi, 0 <= z <= 1 - r^2.
f = (x^2 + y^2) z = r^2 z.
"""
import sympy as sp

r, t, z = sp.symbols("r t z", nonnegative=True)
f = r**2 * z
J = r

# Volume
V = sp.integrate(sp.integrate(sp.integrate(J, (z, 0, 1 - r**2)),
                              (r, 0, 1)), (t, 0, 2 * sp.pi))
# Integral of f
I = sp.integrate(sp.integrate(sp.integrate(f * J, (z, 0, 1 - r**2)),
                              (r, 0, 1)), (t, 0, 2 * sp.pi))
V, I = sp.simplify(V), sp.simplify(I)
print("Volume V  =", V, "=", sp.N(V, 15))
print("Integral I =", I)

fave = sp.simplify(I / V)
print("f_avg (exact) =", fave)
print("f_avg numeric =", sp.N(fave, 15))

# Independent Cartesian checks of V and I.
x, y = sp.symbols("x y", real=True)
V2 = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, 1 - x**2 - y**2)),
                               (y, -sp.sqrt(1 - x**2), sp.sqrt(1 - x**2))), (x, -1, 1))
I2 = sp.integrate(sp.integrate(sp.integrate((x**2 + y**2) * z, (z, 0, 1 - x**2 - y**2)),
                               (y, -sp.sqrt(1 - x**2), sp.sqrt(1 - x**2))), (x, -1, 1))
print("Volume V (cart.)  =", sp.simplify(V2))
print("Integral I (cart.) =", sp.simplify(I2))
assert sp.simplify(V - V2) == 0
assert sp.simplify(I - I2) == 0
print("OK: both coordinate systems agree")
