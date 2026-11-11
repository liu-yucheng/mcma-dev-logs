"""Evaluate the setup integrals for the solid under a parabolic roof.

The solid is x^2 <= y <= 1, 0 <= z <= 1 - y, and the density is sqrt(x^2 + y^2).  The
problem asks only for the setup, so this script uses the setup to produce numbers and
checks that the three integral expressions agree with the geometric description.  The
inner integral over z is done by hand: the height of the solid at (x, y) is 1 - y.

Run:  python part1_step1.py
"""

from __future__ import annotations

from mpmath import mp, quad, sqrt

mp.dps = 15


def integrate_y(f) -> float:
    """Integrate f(x, y) over 0 <= y <= 1 and -sqrt(y) <= x <= sqrt(y)."""
    inner = lambda y: quad(lambda x: f(x, y), [-sqrt(y), sqrt(y)])
    return float(quad(inner, [0, 1]))


def main() -> None:
    density = lambda x, y: sqrt(x * x + y * y)
    height = lambda y: 1 - y

    mass = integrate_y(lambda x, y: height(y) * density(x, y))
    moment_yz = integrate_y(lambda x, y: x * height(y) * density(x, y))
    moment_xz = integrate_y(lambda x, y: y * height(y) * density(x, y))
    moment_xy = integrate_y(lambda x, y: height(y) ** 2 / 2 * density(x, y))
    inertia_z = integrate_y(lambda x, y: height(y) * (x * x + y * y) ** 1.5)

    print(f"mass            m    = {mass:.12f}")
    print(f"moment M_yz          = {moment_yz:.3e}")
    print(f"moment M_xz          = {moment_xz:.12f}")
    print(f"moment M_xy          = {moment_xy:.12f}")
    print(f"inertia I_z          = {inertia_z:.12f}")
    print(f"x bar                = {moment_yz / mass:.3e}")
    print(f"y bar                = {moment_xz / mass:.12f}")
    print(f"z bar                = {moment_xy / mass:.12f}")
    print(f"I_z / m              = {inertia_z / mass:.12f}")


if __name__ == "__main__":
    main()
