"""Evaluate the volume of the wedge with symbolic integration.

The inner integral runs over x from y to 1, the middle integral runs over z from 0 to
sqrt(1 - y**2), and the outer integral runs over y from 0 to 1. The script evaluates
the two terms of the final one-dimensional integral separately.
"""

from sympy import Rational, asin, integrate, pi, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True)

inner_integral = integrate(1, (x, y, 1))
print(f"inner integral over x: {simplify(inner_integral)}")

middle_integral = integrate(inner_integral, (z, 0, sqrt(1 - y**2)))
print(f"middle integral over z: {simplify(middle_integral)}")

print(f"antiderivative of sqrt(1 - y**2): {simplify(integrate(sqrt(1 - y**2), y))}")
print(f"antiderivative of y*sqrt(1 - y**2): {simplify(integrate(y * sqrt(1 - y**2), y))}")

quarter_disk = integrate(sqrt(1 - y**2), (y, 0, 1))
second_term = integrate(y * sqrt(1 - y**2), (y, 0, 1))
print(f"integral of sqrt(1 - y**2) over 0 <= y <= 1: {quarter_disk}")
print(f"integral of y*sqrt(1 - y**2):               {second_term}")

total = integrate((1 - y) * sqrt(1 - y**2), (y, 0, 1))
print(f"full integral over y: {simplify(total)}")
print(f"decimal value:        {float(total.evalf(16)):.12f}")

# The order dz dx dy must give the same number.
other_order = integrate(integrate(integrate(1, (z, 0, sqrt(1 - y**2))), (x, y, 1)), (y, 0, 1))
print(f"order dz dx dy:       {simplify(other_order)}")

assert simplify(total - (pi / 4 - Rational(1, 3))) == 0
assert simplify(other_order - total) == 0
print("both orders give pi/4 - 1/3")
