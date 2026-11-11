"""Compute the mass of E with symbolic integration in both orders.

The density is the constant rho = 2. The solid lies above the plane region D
bounded by y = 0, y = sqrt(x), and x = 1, and below the plane z = 1 + x + y.
"""

from sympy import Rational, integrate, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True, nonnegative=True)
density = Rational(2)
height = 1 + x + y

# Order 1: for fixed x, y runs from 0 to sqrt(x), and x runs from 0 to 1.
inner_over_y = integrate(density * height, (y, 0, sqrt(x)))
print(f"inner y-integral at fixed x: {simplify(inner_over_y)}")
mass_x_outer = integrate(inner_over_y, (x, 0, 1))
print(f"mass with x outside: {simplify(mass_x_outer)}")
print(f"mass with x outside, decimal: {float(mass_x_outer.evalf(15)):.12f}")

# Order 2: for fixed y, x runs from y**2 to 1, and y runs from 0 to 1.
inner_over_x = integrate(density * height, (x, y**2, 1))
print(f"inner x-integral at fixed y: {simplify(inner_over_x)}")
mass_y_outer = integrate(inner_over_x, (y, 0, 1))
print(f"mass with y outside: {simplify(mass_y_outer)}")
print(f"mass with y outside, decimal: {float(mass_y_outer.evalf(15)):.12f}")

assert simplify(mass_x_outer - mass_y_outer) == 0
print("both orders give the same mass")

# The volume of E is the mass divided by the constant density.
volume_value = simplify(mass_x_outer / density)
print(f"volume of E = mass / rho = {volume_value}")
print(f"base area of D = 2/3, mean height of the roof = {simplify(volume_value / (Rational(2, 3)))}")
