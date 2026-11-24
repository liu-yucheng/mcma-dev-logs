"""Verify the value 20 pi of Part 4 with three independent computations.

The first computation uses polar coordinates in the plane of the disk.
The second computation uses adaptive quadrature of the triple integral.
The third computation uses the Monte Carlo method on the bounding box.

The script prints each value, the difference from 20 pi, and the standard error of the
Monte Carlo estimate. The random seed is recorded.
"""

import math
from typing import Final

import numpy as np
from scipy.integrate import quad, tplquad

RANDOM_SEED: Final[int] = 20261122
"""Seed of the pseudo random number generator of the Monte Carlo method."""

RADIUS: Final[float] = 2.0
"""Radius of the disk of the cylinder."""

BOTTOM_HEIGHT: Final[float] = -1.0
"""Height of the bottom plane y = -1."""

BOX_TOP_HEIGHT: Final[float] = 6.0
"""Top of the bounding box in y, equal to the largest value of 4 - z on the disk."""

EXACT_VOLUME_FACTOR: Final[float] = 20.0
"""Factor of the closed form volume 20 pi."""

MONTE_CARLO_SAMPLE_COUNT: Final[int] = 4_000_000
"""Number of random points of the Monte Carlo method."""

POLAR_TOLERANCE: Final[float] = 1.0e-9
"""Largest difference from 20 pi that the polar computation may show."""

TRIPLE_TOLERANCE: Final[float] = 1.0e-6
"""Largest difference from 20 pi that the triple quadrature may show."""


def volume_by_polar_integral() -> float:
    """Return the volume from the polar form of the double integral over the disk."""

    def radial_integral(angle: float) -> float:
        """Return the integral in r at one angle."""
        value, _ = quad(
            lambda r_value: (5.0 - r_value * math.sin(angle)) * r_value,
            0.0,
            RADIUS,
            epsabs=1.0e-12,
        )
        return value

    value, _ = quad(radial_integral, 0.0, 2.0 * math.pi, epsabs=1.0e-12, limit=200)
    return value


def volume_by_triple_quadrature() -> float:
    """Return the volume from the triple integral with the limits of the inequalities."""
    value, _ = tplquad(
        lambda height, z_value, x_value: 1.0,
        -RADIUS,
        RADIUS,
        lambda x_value: -math.sqrt(4.0 - x_value * x_value),
        lambda x_value: math.sqrt(4.0 - x_value * x_value),
        lambda x_value, z_value: -1.0,
        lambda x_value, z_value: 4.0 - z_value,
        epsabs=1.0e-10,
        epsrel=1.0e-10,
    )
    return value


def volume_by_monte_carlo(generator: np.random.Generator, sample_count: int) -> tuple[float, float]:
    """Return the Monte Carlo estimate of the volume and its standard error.

    Args:
        generator: Random number generator with a recorded seed.
        sample_count: Number of random points in the bounding box.

    Returns:
        The estimate of the volume and the standard error of the estimate.
    """
    inside_count = 0
    chunk_count = 4
    chunk_size = sample_count // chunk_count
    for _ in range(chunk_count):
        x_value = generator.uniform(-RADIUS, RADIUS, chunk_size)
        z_value = generator.uniform(-RADIUS, RADIUS, chunk_size)
        y_value = generator.uniform(BOTTOM_HEIGHT, BOX_TOP_HEIGHT, chunk_size)
        inside = (
            (x_value**2 + z_value**2 <= RADIUS**2)
            & (y_value >= BOTTOM_HEIGHT)
            & (y_value <= 4.0 - z_value)
        )
        inside_count += int(np.count_nonzero(inside))
    box_volume = (2.0 * RADIUS) * (BOX_TOP_HEIGHT - BOTTOM_HEIGHT) * (2.0 * RADIUS)
    fraction = inside_count / float(chunk_size * chunk_count)
    estimate = box_volume * fraction
    standard_error = box_volume * math.sqrt(fraction * (1.0 - fraction) / sample_count)
    return estimate, standard_error


def main() -> None:
    """Run the three checks of Part 4 and print each computed value with its expected value."""
    exact_volume = EXACT_VOLUME_FACTOR * math.pi
    print(f"closed form volume: {exact_volume:.12f}")

    polar_volume = volume_by_polar_integral()
    print(f"polar integral:     {polar_volume:.12f}, difference {abs(polar_volume - exact_volume):.3e}")
    assert abs(polar_volume - exact_volume) <= POLAR_TOLERANCE, "the polar integral is not 20 pi"

    triple_volume = volume_by_triple_quadrature()
    difference = abs(triple_volume - exact_volume)
    print(f"triple quadrature:  {triple_volume:.12f}, difference {difference:.3e}")
    assert difference <= TRIPLE_TOLERANCE, "the triple quadrature is not 20 pi"

    generator = np.random.default_rng(RANDOM_SEED)
    estimate, standard_error = volume_by_monte_carlo(generator, MONTE_CARLO_SAMPLE_COUNT)
    deviation = abs(estimate - exact_volume)
    print(f"monte carlo:        {estimate:.6f}, standard error {standard_error:.6f}")
    print(f"monte carlo:        {deviation / standard_error:.3f} standard errors from 20 pi")
    assert deviation <= 3.0 * standard_error, "the Monte Carlo estimate is too far from 20 pi"
    assert abs(estimate - triple_volume) <= 3.0 * standard_error, "the two methods disagree"

    print("part 4: all checks passed")


if __name__ == "__main__":
    main()
