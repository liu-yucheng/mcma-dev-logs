"""Step 1.2: all six iterated orderings of the volume integral equal 2/3 exactly.
"""
import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
V = sp.Rational(1, 6) * abs(sp.Matrix([[0, -2, 0], [-2, 0, 0], [0, 0, 1]]).det())
top = (x + y) / 2 - 1
I1 = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, top)), (y, 2 - x, 2)), (x, 0, 2))
I2 = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, top)), (x, 2 - y, 2)), (y, 0, 2))
I3 = sp.integrate(sp.integrate(sp.integrate(1, (y, 2 - x + 2 * z, 2)), (z, 0, x / 2)), (x, 0, 2))
I4 = sp.integrate(sp.integrate(sp.integrate(1, (x, 2 - y + 2 * z, 2)), (z, 0, y / 2)), (y, 0, 2))
I5 = sp.integrate(sp.integrate(sp.integrate(1, (y, 2 + 2 * z - x, 2)), (x, 2 * z, 2)), (z, 0, 1))
I6 = sp.integrate(sp.integrate(sp.integrate(1, (x, 2 + 2 * z - y, 2)), (y, 2 * z, 2)), (z, 0, 1))
for name, I in zip("abcdef", [I1, I2, I3, I4, I5, I6]):
    print(name, I)
assert all(I == V for I in [I1, I2, I3, I4, I5, I6])
assert V == sp.Rational(2, 3)
print("PASS 1.2")
