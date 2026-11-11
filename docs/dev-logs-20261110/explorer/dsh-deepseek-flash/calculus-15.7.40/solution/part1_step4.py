"""Confirm the mass and the moments with numerical integration in another order.

This script uses the reverse order of the symbolic evaluation: x outermost,
z in the middle, and y innermost.  At a fixed point (x, z) the floor of the
parabolic cylinder gives y = +-sqrt(1 - z), so the inner integral is independent
of x.  The check is independent of the algebra in part1_step3.py.
"""

import mpmath as mp

mp.mp.dps = 15


def outer_integral(integrand_of_xz):
    """Integrate a function of (x, z) over 0 <= x <= 1 and 0 <= z <= 1 - x."""
    return mp.quad(
        lambda x: mp.quad(
            lambda z: mp.quad(
                lambda y: integrand_of_xz(x, z, y), [-mp.sqrt(1 - z), mp.sqrt(1 - z)]
            ),
            [0, 1 - x],
        ),
        [0, 1],
    )


mass = outer_integral(lambda x, z, y: mp.mpf(4))
moment_yz = outer_integral(lambda x, z, y: 4 * x)
moment_xz = outer_integral(lambda x, z, y: 4 * y)
moment_xy = outer_integral(lambda x, z, y: 4 * z)

print(f"numerical mass:     {mp.nstr(mass, 15)}")
print(f"reference 16/5:     {mp.nstr(mp.mpf(16) / 5, 15)}")
print(f"numerical M_yz:     {mp.nstr(moment_yz, 15)}")
print(f"reference 8/7:      {mp.nstr(mp.mpf(8) / 7, 15)}")
print(f"numerical M_xz:     {mp.nstr(moment_xz, 15)}")
print(f"numerical M_xy:     {mp.nstr(moment_xy, 15)}")
print(f"reference 32/35:    {mp.nstr(mp.mpf(32) / 35, 15)}")
print(f"center of mass:     ({mp.nstr(moment_yz / mass, 10)}, "
      f"{mp.nstr(moment_xz / mass, 10)}, {mp.nstr(moment_xy / mass, 10)})")
