"""Evaluate the triple integral of x over E with symbolic algebra.

The evaluation uses the cylindrical description about the x-axis,
E = {(x, r, theta) : 4*r**2 <= x <= 4, 0 <= r <= 1, 0 <= theta <= 2*pi},
with the volume element dV = r dr dtheta dx.
"""

from sympy import Rational, integrate, pi, simplify, symbols

x, radius, theta = symbols("x radius theta", real=True)

inner_integral = integrate(x, (x, 4 * radius**2, 4))
print(f"inner integral over x: {simplify(inner_integral)}")

middle_integrand = simplify(inner_integral * radius)
middle_integral = integrate(middle_integrand, (radius, 0, 1))
print(f"integrand after the area element r: {simplify(middle_integrand)}")
print(f"middle integral over r: {simplify(middle_integral)}")

total = simplify(integrate(middle_integral, (theta, 0, 2 * pi)))
print(f"outer integral over theta: {total}")
print(f"decimal value: {float(total.evalf(15)):.12f}")

# Expanded form of the radial integral for the written solution.
expanded = simplify(integrate(8 * (radius - radius**5), (radius, 0, 1)))
print(f"radial integral of 8*(r - r**5): {expanded}")
assert total == Rational(16, 1) * pi / 3
print("the symbolic result equals 16*pi/3")
