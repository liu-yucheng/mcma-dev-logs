"""Confirm the volume of the bumpy sphere by numerical means.

Two checks are made: a fixed quadrature of the exact triple integral and a Monte
Carlo average over uniformly distributed directions.
"""

import numpy as np
from mpmath import mp, quad
from sympy import Rational, pi


def main():
    """Print the quadrature and Monte Carlo values."""
    mp.dps = 25
    exact = Rational(136, 99) * pi
    print(f"closed form: 136 pi / 99 = {float(exact):.9f}")

    def radius(theta, phi):
        """Return rho on the surface."""
        return 1.0 + 0.2 * mp.sin(6 * theta) * mp.sin(5 * phi)

    direction_integral = quad(
        lambda theta: quad(lambda phi: radius(theta, phi) ** 3 * mp.sin(phi), [0, mp.pi]),
        [0, 2 * mp.pi],
    )
    quadrature = direction_integral / 3
    print(f"mpmath double quadrature: {quadrature}")

    rng = np.random.default_rng(20261110)
    samples = 4_000_000
    cosine = rng.uniform(-1.0, 1.0, samples)
    azimuth = rng.uniform(0.0, 2.0 * np.pi, samples)
    polar = np.arccos(cosine)
    rho = 1.0 + 0.2 * np.sin(6.0 * azimuth) * np.sin(5.0 * polar)
    estimate = 4.0 * np.pi / 3.0 * np.mean(rho**3)
    print(f"Monte Carlo over 4 pi steradians: {estimate:.6f}")

    print()
    print("the mean of rho^3 over the directions is 34/33 = %.6f, so the solid is"
          % (34.0 / 33.0))
    print("slightly larger than the unit sphere though the mean of rho itself is 1")


if __name__ == "__main__":
    main()
