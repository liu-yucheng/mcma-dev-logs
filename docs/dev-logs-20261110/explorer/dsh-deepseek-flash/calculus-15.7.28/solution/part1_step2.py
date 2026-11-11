"""Evaluate the volume of the solid with symbolic algebra, step by step.

The order of the integral is dx dz dy: x is the inner variable, z is the middle
variable, and y is the outer variable.  The final section repeats the volume in
the order dz dy dx to confirm the region description.
"""

from sympy import Rational, expand, integrate, simplify, symbols, sqrt

x, y, z = symbols("x y z", real=True)

inner_integral = integrate(1, (x, 0, 4 - y**2))
print(f"inner integral over x:       {simplify(inner_integral)}")

middle_integral = integrate(simplify(inner_integral), (z, 0, 2 - y))
print(f"middle integral over z:      {simplify(middle_integral)}")
print(f"expanded middle result:      {expand(middle_integral)}")

outer_integral = integrate(expand(middle_integral), (y, 0, 2))
print(f"outer integral over y:       {simplify(outer_integral)}")
print(f"decimal value:               {float(outer_integral):.6f}")

print()
print("The same solid in the order dz dy dx, with x as the outer variable.")
for given_x in (0.0, 1.0, 2.0, 3.0, 4.0):
    print(f"  x = {given_x:.1f}: y runs 0 to {sqrt(4 - given_x):.3f}" if given_x < 4
          else f"  x = {given_x:.1f}: the cross-section collapses to the line x = 4")

alternative = integrate(integrate(integrate(1, (z, 0, 2 - y)), (y, 0, sqrt(4 - x))), (x, 0, 4))
print(f"volume from the order dz dy dx: {simplify(alternative)}")

assert simplify(outer_integral - Rational(20, 3)) == 0
assert simplify(alternative - Rational(20, 3)) == 0
print("both orders give 20/3")
