"""Check the average value with independent numerical quadrature.

The triple integral of f = x**2*z + y**2*z over the cap is evaluated twice with
mpmath: once in polar coordinates and once in Cartesian coordinates. Both values
are compared with the exact integral pi/24 and the exact average value 1/12.
"""

from mpmath import mp, pi, quad, sqrt

mp.dps = 20

exact_integral = pi / 24
exact_average = mp.mpf(1) / 12

# Polar order: theta, then radius, then z.
polar_value = quad(
    lambda theta_value: quad(
        lambda radius_value: quad(
            lambda z_value: radius_value**2 * z_value * radius_value,
            [0, 1 - radius_value**2],
        ),
        [0, 1],
    ),
    [0, 2 * pi],
)


def cap_height_integral(radius_value):
    """Integrate the polar volume element r over the cap height at fixed radius."""
    return radius_value * (1 - radius_value**2)


volume_value = quad(
    lambda theta_value: quad(cap_height_integral, [0, 1]),
    [0, 2 * pi],
)


def inner_over_z(x_value, y_value):
    """Integrate (x**2 + y**2)*z over the vertical range of the cap."""
    cap_height = 1 - x_value**2 - y_value**2
    if cap_height <= 0:
        return mp.mpf(0)
    return (x_value**2 + y_value**2) * cap_height**2 / 2


def inner_over_y(x_value):
    """Integrate the z-result over the chord of the unit disk at fixed x."""
    half_width = sqrt(1 - x_value**2)
    return quad(lambda y_value: inner_over_z(x_value, y_value), [-half_width, half_width])


cartesian_value = quad(inner_over_y, [-1, 1])

volume_value = quad(
    lambda theta_value: quad(lambda radius_value: radius_value * (1 - radius_value**2), [0, 1]),
    [0, 2 * pi],
)

print(f"exact integral pi/24:        {mp.nstr(exact_integral, 15)}")
print(f"polar quadrature:            {mp.nstr(polar_value, 15)}")
print(f"Cartesian quadrature:        {mp.nstr(cartesian_value, 15)}")
print(f"volume by quadrature:        {mp.nstr(volume_value, 15)}")
print(f"average from polar value:    {mp.nstr(polar_value / volume_value, 12)}")
print(f"exact average 1/12:          {mp.nstr(exact_average, 12)}")

assert abs(polar_value - exact_integral) / exact_integral < mp.mpf("1e-14")
assert abs(cartesian_value - exact_integral) / exact_integral < mp.mpf("1e-12")
assert abs(volume_value - pi / 2) / (pi / 2) < mp.mpf("1e-14")
print("both quadratures reproduce pi/24 and the average 1/12")
