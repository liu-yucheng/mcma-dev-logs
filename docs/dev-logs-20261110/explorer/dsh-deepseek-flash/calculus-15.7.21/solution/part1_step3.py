"""Verify 8/15 with two independent numerical quadratures.

The first order integrates the height over the projection in the xy-plane. The
second order integrates the area of the sections at a fixed height z.
"""

from mpmath import mp, quad, sqrt

mp.dps = 25

exact_value = mp.mpf(8) / mp.mpf(15)


# Order dz dy dx: outer x, then y, then the height 1 - y.
value_projection_first = quad(
    lambda x_value: quad(lambda y_value: 1 - y_value, [x_value**2, 1]),
    [-1, 1],
)

# Order dz dx dy: here the sections at a fixed height z are used.
value_sections_first = quad(
    lambda z_value: quad(
        lambda x_value: 1 - z_value - x_value**2,
        [-sqrt(1 - z_value), sqrt(1 - z_value)],
    ),
    [0, 1],
)

print(f"exact value 8/15:             {mp.nstr(exact_value, 15)}")
print(f"quadrature projection first:  {mp.nstr(value_projection_first, 15)}")
print(f"quadrature sections first:    {mp.nstr(value_sections_first, 15)}")
print(f"deviation projection first:   {mp.nstr(abs(value_projection_first - exact_value), 5)}")
print(f"deviation sections first:     {mp.nstr(abs(value_sections_first - exact_value), 5)}")
assert abs(value_projection_first - exact_value) < mp.mpf("1e-18")
assert abs(value_sections_first - exact_value) < mp.mpf("1e-18")
print("both numerical paths agree with 8/15")
