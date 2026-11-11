"""Evaluate the volume and the triple integral over the cap with symbolic algebra.

The solid is described in polar coordinates about the z-axis,
E = {(r, theta, z) : 0 <= z <= 1 - r**2, 0 <= r <= 1, 0 <= theta <= 2*pi},
with the volume element dV = r dz dr dtheta.
"""

from sympy import Rational, integrate, pi, simplify, symbols

radius, theta, z = symbols("radius theta z", real=True)

# Volume of E.
volume_inner = integrate(radius, (z, 0, 1 - radius**2))
volume_middle = integrate(volume_inner, (radius, 0, 1))
volume_total = integrate(volume_middle, (theta, 0, 2 * pi))
print(f"volume inner integrand after dz: {simplify(volume_inner)}")
print(f"volume after dr:                {simplify(volume_middle)}")
print(f"volume V(E):                    {volume_total}")

# The integrand f = x**2*z + y**2*z becomes r**2*z in polar coordinates.
function_polar = radius**2 * z
print(f"integrand in polar coordinates: {function_polar}")

integral_inner = integrate(function_polar * radius, (z, 0, 1 - radius**2))
integral_middle = integrate(integral_inner, (radius, 0, 1))
integral_total = integrate(integral_middle, (theta, 0, 2 * pi))
print(f"inner integral after dz:        {simplify(integral_inner)}")
print(f"radial integral:                {simplify(integral_middle)}")
print(f"triple integral of f:           {integral_total}")

# Expanded radial polynomial for the written solution.
expanded_middle = integrate((radius**3 - 2 * radius**5 + radius**7) / 2, (radius, 0, 1))
print(f"radial integral of (r^3 - 2 r^5 + r^7)/2: {expanded_middle}")

average_value = simplify(integral_total / volume_total)
print(f"average value:                  {average_value}")
print(f"decimal value:                  {float(average_value.evalf(15)):.12f}")

assert volume_total == pi / 2
assert integral_total == pi / 24
assert average_value == Rational(1, 12)
print("the symbolic results are pi/2, pi/24, and 1/12")
