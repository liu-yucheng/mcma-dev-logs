"""Check the volume of the lens-shaped solid between the two paraboloids.

The solid is described in cylindrical coordinates by
0 <= r <= sqrt(5/2) and r^2 <= z <= 5 - r^2. The exact volume follows from
an elementary integration, and two independent numerical methods confirm it.
"""

from math import pi, sqrt

import numpy as np
from mpmath import mp, quad
from sympy import Rational, integrate, symbols


def exact_volume():
    """Return the exact volume with a symbolic integration."""
    radius, angle = symbols("r theta", positive=True)
    height = 5 - 2 * radius**2
    inner = integrate(height * radius, (radius, 0, sqrt(Rational(5, 2))))
    return integrate(inner, (angle, 0, 2 * pi))


def main():
    """Print the exact volume and two numerical confirmations."""
    volume = exact_volume()
    print(f"exact volume from the iterated integral: {volume}")
    print(f"decimal value: {float(volume):.6f}")

    mp.dps = 25
    rim = mp.sqrt(mp.mpf(5) / 2)
    quadrature = 2 * mp.pi * quad(lambda r: (5 - 2 * r**2) * r, [0, rim])
    print(f"mpmath quadrature: {quadrature}")

    rng = np.random.default_rng(20261110)
    samples = 4_000_000
    x = rng.uniform(-rim, rim, samples)
    y = rng.uniform(-rim, rim, samples)
    thickness = 5 - 2 * (x**2 + y**2)
    thickness = np.where(x**2 + y**2 <= rim**2, thickness, 0.0)
    estimate = (2 * float(rim)) ** 2 * np.mean(thickness)
    print(f"Monte Carlo estimate over a square of side {2 * float(rim):.4f}: {estimate:.4f}")
    print(f"exact value: {float(volume):.4f}")


if __name__ == "__main__":
    main()