"""Evaluate the triple integral of x over E for problem 15.7.17.

E is bounded by the paraboloid x = 4*y**2 + 4*z**2 and the plane x = 4.
For each x in [0, 4] the cross section is the disk y**2 + z**2 <= x/4.
"""

import sympy as sp

x = sp.symbols("x", positive=True)
y, z = sp.symbols("y z", real=True)

# Cross-section disk: 4*y**2 + 4*z**2 <= x  =>  y**2 + z**2 <= x/4
radius_squared = x / 4
cross_section_area = sp.pi * radius_squared

# Volume element: slice at x with area A(x)
integrand = x * cross_section_area
integral = sp.integrate(integrand, (x, 0, 4))
print("exact integral =", sp.simplify(integral))

# Independent check: iterated integral in cylindrical-like order (x outer).
r, phi = sp.symbols("r phi", nonnegative=True)
# r from 0 to sqrt(x)/2, phi over full circle, x from 0 to 4
inner = sp.integrate(sp.integrate(x * r, (r, 0, sp.sqrt(x) / 2)), (phi, 0, 2 * sp.pi))
check = sp.integrate(inner, (x, 0, 4))
print("iterated check  =", sp.simplify(check))
assert sp.simplify(integral - check) == 0
print("numerical value =", sp.N(integral))
