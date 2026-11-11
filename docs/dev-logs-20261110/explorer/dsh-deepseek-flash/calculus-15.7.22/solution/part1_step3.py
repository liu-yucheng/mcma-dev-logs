"""Evaluate the volume numerically with mpmath in two different orders.

The first order uses cylindrical coordinates about the y-axis. The second order
integrates (5 - z) over the disk in Cartesian coordinates. Both results must agree
with 20*pi to working precision.
"""

from mpmath import mp

mp.dps = 20
exact_value = 20 * mp.pi

cylindrical_value = mp.quad(
    lambda angle: mp.quad(
        lambda radius: mp.quad(lambda height: radius, [-1, 4 - radius * mp.sin(angle)]),
        [0, 2],
    ),
    [0, 2 * mp.pi],
)
print(f"cylindrical order (theta, r, y): {mp.nstr(cylindrical_value, 16)}")

cartesian_value = mp.quad(
    lambda x_coordinate: mp.quad(
        lambda z_coordinate: 5 - z_coordinate,
        [-mp.sqrt(4 - x_coordinate**2), mp.sqrt(4 - x_coordinate**2)],
    ),
    [-2, 2],
)
print(f"Cartesian order (x, z):          {mp.nstr(cartesian_value, 16)}")

# The mean value of z over the disk is zero; this is the symmetry used in the text.
z_moment = mp.quad(
    lambda angle: mp.quad(lambda radius: radius**2 * mp.sin(angle), [0, 2]),
    [0, 2 * mp.pi],
)
print(f"integral of z over the disk:     {mp.nstr(z_moment, 16)}")

print(f"exact value 20*pi:               {mp.nstr(exact_value, 16)}")
print(f"first difference:  {mp.nstr(cylindrical_value - exact_value, 3)}")
print(f"second difference: {mp.nstr(cartesian_value - exact_value, 3)}")
