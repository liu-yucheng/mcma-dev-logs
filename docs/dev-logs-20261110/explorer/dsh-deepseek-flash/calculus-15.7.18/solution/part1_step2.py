"""Evaluate the triple integral of z over E with symbolic algebra.

The solid is described by 0 <= y <= 3, 0 <= x <= y/3 and
0 <= z <= sqrt(9 - y**2), so the integral is taken in the order dz dx dy.
"""

from sympy import Rational, integrate, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True)

inner_integral = integrate(z, (z, 0, sqrt(9 - y**2)))
print(f"inner integral over z:        {simplify(inner_integral)}")

middle_integrand = simplify(inner_integral)
middle_integral = integrate(middle_integrand, (x, 0, y / 3))
print(f"integrand after dz:           {middle_integrand}")
print(f"middle integral over x:       {simplify(middle_integral)}")

outer_integrand = simplify(middle_integral)
print(f"integrand 9y/6 - y^3/6:       {outer_integrand}")

# The page quotes the factor and the bracket of the last step, so print them.
z_height = simplify(inner_integral.subs(y, 0))
x_width = y / 3
print(f"z-height at x-free limit:     {z_height}")
print(f"coefficient 1/2 times 1/3:    {simplify(Rational(1, 2) * Rational(1, 3))}")

bracket = integrate(y * (9 - y**2), y)
print(f"integral of y(9-y^2) in y:    {bracket}")
print(f"value of bracket at y=3:      {bracket.subs(y, 3)}")
print(f"value of bracket at y=0:      {bracket.subs(y, 0)}")

total = simplify(integrate(outer_integrand, (y, 0, 3)))
print(f"outer integral over y:        {total}")
print(f"decimal value:                {float(total.evalf(15)):.12f}")

# Write the outer antiderivative explicitly, as the page quotes it.
antiderivative = integrate(outer_integrand, y)
at_upper = antiderivative.subs(y, 3)
at_lower = antiderivative.subs(y, 0)
print(f"antiderivative in y:          {simplify(antiderivative)}")
print(f"value at y=3:                 {simplify(at_upper)}")
print(f"value at y=0:                 {simplify(at_lower)}")

# Cross-check: sum the areas of the rectangular sections perpendicular to y.
section_area = simplify(x_width * sqrt(9 - y**2))
volume = simplify(integrate(section_area, (y, 0, 3)))
print(f"section area A(y):            {section_area}")
print(f"volume of E:                  {volume}")

# Cross-check: the same section area weighted by the mean height of z.
mean_height = simplify(integrate(z, (z, 0, sqrt(9 - y**2)))) / simplify(sqrt(9 - y**2))
weighted = simplify(integrate(section_area * mean_height, (y, 0, 3)))
print(f"mean height of z in a section: {mean_height}")
print(f"weighted section integral:    {weighted}")

assert total == Rational(27, 8)
assert volume == Rational(3, 1)
assert weighted == Rational(27, 8)
print("the symbolic result equals 27/8 and the volume of E is 3")