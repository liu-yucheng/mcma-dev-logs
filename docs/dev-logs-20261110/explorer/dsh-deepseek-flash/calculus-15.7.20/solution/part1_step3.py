"""Verify 16*pi with two independent numerical quadratures.

The first order integrates the height over the disk. The second order
integrates the area of the horizontal sections and splits the y-range at 4.
"""

from mpmath import mp, pi, quad, sqrt

mp.dps = 25

exact_value = 16 * pi


def height_at(radius):
    """Return the height 8 - 2 r**2 of the solid at the given radius."""
    return 8 - 2 * radius**2


# Order dy dr dtheta: outer theta, then r, then the height.
value_height_first = quad(
    lambda theta_value: quad(
        lambda radius: quad(lambda y_value: 1, [radius**2, 8 - radius**2]) * radius,
        [0, 2],
    ),
    [0, 2 * pi],
)

# Order dy with horizontal sections: outer y, inner disk of radius r(y).
def section_radius(y_value):
    """Return the radius of the disk that cuts the solid at height y."""
    if y_value <= 4:
        return sqrt(y_value)
    return sqrt(8 - y_value)


value_sections_first = quad(
    lambda y_value: pi * section_radius(y_value) ** 2,
    [0, 4, 8],
)

print(f"exact value 16*pi:            {mp.nstr(exact_value, 15)}")
print(f"quadrature height first:      {mp.nstr(value_height_first, 15)}")
print(f"quadrature sections first:    {mp.nstr(value_sections_first, 15)}")
print(f"deviation height first:       {mp.nstr(abs(value_height_first - exact_value), 5)}")
print(f"deviation sections first:     {mp.nstr(abs(value_sections_first - exact_value), 5)}")
assert abs(value_height_first - exact_value) < mp.mpf("1e-18")
assert abs(value_sections_first - exact_value) < mp.mpf("1e-18")
print("both numerical paths agree with 16*pi")
