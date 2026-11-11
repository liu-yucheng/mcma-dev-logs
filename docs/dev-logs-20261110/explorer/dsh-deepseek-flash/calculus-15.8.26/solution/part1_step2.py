"""Confirm the volume of the cylinder and sphere intersection numerically.

Take a = 1 and compare the closed form with mpmath quadrature and with a Monte
Carlo estimate of the same region.
"""

import numpy as np
from mpmath import mp, quad
from sympy import Rational, pi


def main():
    """Print three independent values for the volume with a = 1."""
    mp.dps = 25
    exact = Rational(2, 3) * (pi - Rational(4, 3))
    print(f"closed form for a = 1: {exact} = {float(exact):.9f}")

    half = mp.pi / 2
    inner = quad(
        lambda theta: quad(lambda r: 2 * mp.sqrt(1 - r**2) * r, [0, mp.cos(theta)]),
        [0, half],
    )
    quadrature = 2 * inner
    print(f"mpmath double quadrature: {quadrature}")

    rng = np.random.default_rng(20261110)
    samples = 6_000_000
    x = rng.uniform(-1.0, 1.0, samples)
    y = rng.uniform(-1.0, 1.0, samples)
    z = rng.uniform(-1.0, 1.0, samples)
    inside_sphere = x**2 + y**2 + z**2 <= 1.0
    inside_cylinder = x**2 + y**2 <= x
    fraction = np.mean(inside_sphere & inside_cylinder)
    estimate = fraction * 8.0
    print(f"Monte Carlo over the cube [-1,1]^3: {estimate:.6f}")

    print()
    print("the cylinder has radius a/2 and axis at (a/2, 0), so its own volume is")
    print(f"  pi (a/2)^2 (2a) = {float(mp.pi * 0.25 * 2):.6f} for a = 1")
    print("the sphere has volume 4 pi/3 = %.6f for a = 1" % (4 * float(mp.pi) / 3))


if __name__ == "__main__":
    main()
