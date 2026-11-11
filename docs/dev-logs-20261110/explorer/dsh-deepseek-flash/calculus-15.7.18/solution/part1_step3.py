"""Verify 27/8 with two independent numerical quadratures.

The first order integrates z, then x, then y. The second order integrates z,
then y, then x, so the two paths use different limits for the outer variables.
"""

from mpmath import mp, quad, sqrt

mp.dps = 25

exact_value = mp.mpf(27) / 8


def height_at(y_value):
    """Return the upper limit sqrt(9 - y**2) of the z-range at height y."""
    return sqrt(9 - y_value**2)


# Order dz dx dy: outer y, then x, then z.
value_dz_dx_dy = quad(
    lambda y_value: quad(
        lambda x_value: quad(lambda z_value: z_value, [0, height_at(y_value)]),
        [0, y_value / 3],
    ),
    [0, 3],
)

# Order dz dy dx: outer x, then y from the plane to the rim, then z.
value_dz_dy_dx = quad(
    lambda x_value: quad(
        lambda y_value: quad(lambda z_value: z_value, [0, height_at(y_value)]),
        [3 * x_value, 3],
    ),
    [0, 1],
)

print(f"exact value 27/8:             {mp.nstr(exact_value, 15)}")
print(f"quadrature dz dx dy:          {mp.nstr(value_dz_dx_dy, 15)}")
print(f"quadrature dz dy dx:          {mp.nstr(value_dz_dy_dx, 15)}")
print(f"deviation of dz dx dy:        {mp.nstr(abs(value_dz_dx_dy - exact_value), 5)}")
print(f"deviation of dz dy dx:        {mp.nstr(abs(value_dz_dy_dx - exact_value), 5)}")
assert abs(value_dz_dx_dy - exact_value) < mp.mpf("1e-18")
assert abs(value_dz_dy_dx - exact_value) < mp.mpf("1e-14")
print("both numerical paths agree with 27/8")
