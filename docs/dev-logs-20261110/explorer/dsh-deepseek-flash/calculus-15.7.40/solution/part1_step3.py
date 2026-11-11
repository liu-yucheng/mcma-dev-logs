"""Evaluate the three first moments of E and the center of mass.

Each moment is the integral of the density 4 times one coordinate, taken over the
same region as the mass.  The center of mass is the moment divided by the mass.
"""

from sympy import Rational, integrate, simplify, symbols

x, y, z = symbols("x y z", real=True)

mass_value = Rational(16, 5)

# Moment about the yz-plane: the integrand is 4*x.
moment_yz = simplify(integrate(integrate(integrate(4 * x, (x, 0, 1 - z)), (z, 0, 1 - y**2)), (y, -1, 1)))
print(f"moment about the yz-plane, M_yz: {moment_yz}")

# Moment about the xz-plane: the integrand is 4*y, and the region is symmetric in y.
moment_xz = simplify(integrate(integrate(integrate(4 * y, (x, 0, 1 - z)), (z, 0, 1 - y**2)), (y, -1, 1)))
print(f"moment about the xz-plane, M_xz: {moment_xz}")

# Moment about the xy-plane: the integrand is 4*z.
moment_xy = simplify(integrate(integrate(integrate(4 * z, (x, 0, 1 - z)), (z, 0, 1 - y**2)), (y, -1, 1)))
print(f"moment about the xy-plane, M_xy: {moment_xy}")

centroid_x = simplify(moment_yz / mass_value)
centroid_y = simplify(moment_xz / mass_value)
centroid_z = simplify(moment_xy / mass_value)
print(f"x-coordinate of the center of mass: {centroid_x} = {float(centroid_x):.6f}")
print(f"y-coordinate of the center of mass: {centroid_y}")
print(f"z-coordinate of the center of mass: {centroid_z} = {float(centroid_z):.6f}")

assert moment_yz == Rational(8, 7)
assert moment_xz == 0
assert moment_xy == Rational(32, 35)
assert centroid_x == Rational(5, 14)
assert centroid_z == Rational(2, 7)
print("the symbolic moments equal 8/7, 0, 32/35 and the center of mass is (5/14, 0, 2/7)")
