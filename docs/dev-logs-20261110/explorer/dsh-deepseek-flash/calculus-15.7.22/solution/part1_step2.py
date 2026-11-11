"""Evaluate the volume symbolically in cylindrical coordinates about the y-axis.

With x = r*cos(theta) and z = r*sin(theta) the cylinder is r = 2 and the volume
element is dV = r dy dr dtheta. The script also evaluates the double integral over
the disk to show that the term linear in z vanishes by symmetry.
"""

from sympy import Rational, integrate, pi, simplify, sin, symbols

radius, theta, y = symbols("radius theta y", real=True)

inner_integral = integrate(radius, (y, -1, 4 - radius * sin(theta)))
print(f"inner integral over y: {simplify(inner_integral)}")

middle_integral = integrate(inner_integral, (radius, 0, 2))
print(f"middle integral over r: {simplify(middle_integral)}")

total = integrate(middle_integral, (theta, 0, 2 * pi))
print(f"outer integral over theta: {simplify(total)}")
print(f"decimal value: {float(total.evalf(16)):.12f}")

# The same volume as a double integral over the disk: the thickness is 5 - z.
area_part = integrate(integrate(5 * radius, (radius, 0, 2)), (theta, 0, 2 * pi))
slope_part = integrate(integrate(radius * sin(theta) * radius, (radius, 0, 2)), (theta, 0, 2 * pi))
print(f"integral of the constant 5 over the disk: {simplify(area_part)}")
print(f"integral of z over the disk:              {simplify(slope_part)}")
print(f"double integral check:                    {simplify(area_part - slope_part)}")

assert simplify(total) == 20 * pi
assert simplify(area_part - slope_part) == 20 * pi
print("both routes give 20*pi")
