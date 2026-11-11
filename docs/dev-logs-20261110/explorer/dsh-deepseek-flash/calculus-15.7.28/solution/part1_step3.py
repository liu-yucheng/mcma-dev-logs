"""Confirm the volume with numerical quadrature in two different orders."""

from mpmath import mp, mpf, quad, sqrt

mp.dps = 20


def width_in_x(y_value):
    """Return the length of the x-fibre at height y."""
    return 4 - y_value**2


def height_in_y(x_value):
    """Return the largest y at which the plane x = const meets the solid."""
    return sqrt(4 - x_value)


order_dx_dz_dy = quad(
    lambda y_value: quad(
        lambda z_value: quad(lambda x_value: mpf(1), [0, width_in_x(y_value)]),
        [0, 2 - y_value],
    ),
    [0, 2],
)

order_dz_dy_dx = quad(
    lambda x_value: quad(
        lambda y_value: quad(lambda z_value: mpf(1), [0, 2 - y_value]),
        [0, height_in_y(x_value)],
    ),
    [0, 4],
)

exact_volume = mpf(20) / mpf(3)

print(f"order dx dz dy: {mp.nstr(order_dx_dz_dy, 16)}")
print(f"order dz dy dx: {mp.nstr(order_dz_dy_dx, 16)}")
print(f"exact 20/3:     {mp.nstr(exact_volume, 16)}")
print(f"difference dx dz dy: {mp.nstr(order_dx_dz_dy - exact_volume, 5)}")
print(f"difference dz dy dx: {mp.nstr(order_dz_dy_dx - exact_volume, 5)}")
