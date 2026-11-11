"""Verify the symbolic value of the integral with independent quadrature.

The triple integral is evaluated numerically with mpmath, first in the
cylindrical order and then in Cartesian coordinates, so that two independent
numerical paths are compared with the exact value 16*pi/3.
"""

from mpmath import mp, pi, quad, sqrt

mp.dps = 25

exact_value = 16 * pi / 3

# Cylindrical order: theta, then radius, then x.
cylindrical_value = quad(
    lambda theta_value: quad(
        lambda radius_value: quad(
            lambda x_value: x_value * radius_value,
            [4 * radius_value**2, 4],
        ),
        [0, 1],
    ),
    [0, 2 * pi],
)

# Cartesian order: integrate over z, then over y, then over x.
def inner_over_z(x_value, y_value):
    """Integrate x over the vertical z-range of the solid at fixed x and y."""
    if x_value <= 4 * y_value**2:
        return mp.mpf("0")
    upper_z = sqrt(x_value / 4 - y_value**2)
    return quad(lambda z_value: x_value, [-upper_z, upper_z])


def inner_over_y(x_value):
    """Integrate the z-integral over the y-range at fixed x."""
    if x_value <= 0:
        return mp.mpf("0")
    limit = sqrt(x_value / 4)
    return quad(lambda y_value: inner_over_z(x_value, y_value), [-limit, limit])


cartesian_value = quad(inner_over_y, [0, 4])

print(f"exact value:              {mp.nstr(exact_value, 15)}")
print(f"cylindrical quadrature:   {mp.nstr(cylindrical_value, 15)}")
print(f"Cartesian quadrature:     {mp.nstr(cartesian_value, 15)}")
print(f"relative deviation (cyl): {mp.nstr(abs(cylindrical_value - exact_value) / exact_value, 5)}")
print(f"relative deviation (cart):{mp.nstr(abs(cartesian_value - exact_value) / exact_value, 5)}")
assert abs(cylindrical_value - exact_value) / exact_value < mp.mpf("1e-12")
assert abs(cartesian_value - exact_value) / exact_value < mp.mpf("1e-9")
print("both numerical checks agree with 16*pi/3")
