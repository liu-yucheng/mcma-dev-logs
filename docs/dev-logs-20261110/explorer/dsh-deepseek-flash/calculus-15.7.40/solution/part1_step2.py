"""Evaluate the mass of E with symbolic integration.

The mass is the integral of the constant density 4 over E.  The inner integral
runs over x from 0 to 1 - z, the middle integral runs over z from 0 to 1 - y**2,
and the outer integral runs over y from -1 to 1.
"""

from sympy import Rational, integrate, simplify, symbols

x, y, z = symbols("x y z", real=True)

inner_integral = integrate(4, (x, 0, 1 - z))
print(f"inner integral over x: {inner_integral}")

middle_integrand = simplify(inner_integral)
middle_integral = simplify(integrate(middle_integrand, (z, 0, 1 - y**2)))
print(f"integrand after the z integration: {middle_integral}")
print(f"expanded form: {simplify(middle_integral).expand()}")

mass = simplify(integrate(middle_integral, (y, -1, 1)))
print(f"mass: {mass}")
print(f"decimal value of the mass: {float(mass):.6f}")
assert mass == Rational(16, 5)
print("the symbolic mass equals 16/5")
