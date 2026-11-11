"""Compute the three moments and the center of mass of E.

The density is constant, so each moment reduces to a double integral over the
plane region D. The z-integration is done first in every case.
"""

from sympy import Rational, integrate, simplify, sqrt, symbols

x, y, z = symbols("x y z", real=True, nonnegative=True)
density = Rational(2)
height = 1 + x + y


def integrate_over_d(integrand):
    """Integrate a function of x and y over D, with x as the outer variable."""
    inner = integrate(integrand, (y, 0, sqrt(x)))
    return simplify(integrate(inner, (x, 0, 1)))


def fibre_z(integrand):
    """Integrate an integrand with respect to z from 0 to the plane."""
    return simplify(integrate(integrand, (z, 0, height)))


mass = simplify(density * integrate_over_d(height))
print(f"mass: {mass}")

moment_yz_inner = fibre_z(density * x)
moment_yz = integrate_over_d(moment_yz_inner)
print(f"z-integral for M_yz: {moment_yz_inner}")
print(f"M_yz = {moment_yz}, decimal {float(moment_yz.evalf(15)):.12f}")

moment_xz_inner = fibre_z(density * y)
moment_xz = integrate_over_d(moment_xz_inner)
print(f"z-integral for M_xz: {moment_xz_inner}")
print(f"M_xz = {moment_xz}, decimal {float(moment_xz.evalf(15)):.12f}")

moment_xy_inner = fibre_z(density * z)
moment_xy = integrate_over_d(moment_xy_inner)
print(f"z-integral for M_xy: {moment_xy_inner}")
print(f"M_xy = {moment_xy}, decimal {float(moment_xy.evalf(15)):.12f}")

centroid_x = simplify(moment_yz / mass)
centroid_y = simplify(moment_xz / mass)
centroid_z = simplify(moment_xy / mass)
print(f"x-bar = M_yz/m = {centroid_x} = {float(centroid_x.evalf(15)):.12f}")
print(f"y-bar = M_xz/m = {centroid_y} = {float(centroid_y.evalf(15)):.12f}")
print(f"z-bar = M_xy/m = {centroid_z} = {float(centroid_z.evalf(15)):.12f}")

# A point of the solid must satisfy 0 <= x <= 1, 0 <= y <= sqrt(x), and
# 0 <= z <= 1 + x + y.
print(f"0 <= x-bar <= 1: {0 <= centroid_x <= 1}")
print(f"0 <= y-bar <= sqrt(x-bar): {0 <= centroid_y <= sqrt(centroid_x)}")
roof_height = simplify(1 + centroid_x + centroid_y)
print(f"roof height at (x-bar, y-bar): {roof_height} = {float(roof_height.evalf(15)):.9f}")
print(f"0 <= z-bar <= roof height: {0 <= centroid_z <= roof_height}")
print(f"z-bar as a multiple of the roof height: {float(centroid_z / roof_height.evalf(15)):.9f}")

assert simplify(mass * centroid_x - moment_yz) == 0
assert simplify(mass * centroid_y - moment_xz) == 0
assert simplify(mass * centroid_z - moment_xy) == 0
print("m * centroid equals the moment vector in every coordinate")
