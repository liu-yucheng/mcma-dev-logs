"""Check the algebraic steps that reduce the setup integrals.

The inner integral over z removes the z-dependence.  The inertia integrand combines the
distance squared with the density.  The y-limits x^2 <= y <= 1 also fix the x-range.

Run:  python part1_step3.py
"""

from __future__ import annotations

import sympy as sp

x, y, z = sp.symbols("x y z", real=True)
height = 1 - y
density = sp.sqrt(x**2 + y**2)

height_integral = sp.integrate(1, (z, 0, height))
moment_integral = sp.integrate(z, (z, 0, height))
print(f"integral of 1 over z: {height_integral}")
print(f"integral of z over z: {sp.factor(moment_integral)}")

inertia_integrand = sp.simplify((x**2 + y**2) * density - (x**2 + y**2) ** sp.Rational(3, 2))
print(f"(x^2 + y^2) * density - (x^2 + y^2)^(3/2) = {inertia_integrand}")

area = sp.integrate(sp.integrate(1, (x, -sp.sqrt(y), sp.sqrt(y))), (y, 0, 1))
print(f"area of the base, 0 <= y <= 1 and |x| <= sqrt(y): {area}")

volume = sp.integrate(sp.integrate(sp.integrate(1, (z, 0, height)), (y, x**2, 1)), (x, -1, 1))
print(f"volume of the solid: {volume}")

assert sp.simplify(height_integral - (1 - y)) == 0
assert sp.simplify(moment_integral - (1 - y) ** 2 / 2) == 0
assert sp.simplify(inertia_integrand) == 0
assert sp.simplify(area - sp.Rational(4, 3)) == 0
print("assertions passed")
