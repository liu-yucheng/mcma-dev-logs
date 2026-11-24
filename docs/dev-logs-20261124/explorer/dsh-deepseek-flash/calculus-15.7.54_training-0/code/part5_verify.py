"""Verify the whole chain of the solution with one independent computation.

The script repeats the answer with a single rejection sample of the solid and a
polynomial integration of the reduced one-dimensional forms. It compares the
two routes with the exact rational values of Part 2, Part 3, and Part 4, and it
prints the summary table of the tutorial.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

SAMPLE_COUNT = 800000
RANDOM_SEED = 20261123
SAMPLE_SIGMA = 4.0
EXPECTED_VOLUME = math.pi / 2.0
EXPECTED_INTEGRAL = math.pi / 24.0
EXPECTED_AVERAGE = 1.0 / 12.0


def volume_of_region() -> float:
    """Return the volume of E from the reduced one-dimensional integral."""
    return math.pi * float(np.polynomial.Polynomial([1.0, -1.0]).integ()(1.0))


def integral_over_region() -> float:
    """Return the triple integral of f from the reduced one-dimensional integral."""
    radial = np.polynomial.Polynomial([0.0, 0.0, 0.0, 0.5, 0.0, -1.0, 0.0, 0.5])
    return 2.0 * math.pi * float(radial.integ()(1.0))


def main() -> None:
    """Run the whole-chain check and print the summary of every result."""
    # BEGIN CHECK reduced_polynomial_route
    volume_by_polynomial = volume_of_region()
    integral_by_polynomial = integral_over_region()
    average_by_polynomial = integral_by_polynomial / volume_by_polynomial
    print("volume by polynomial integration             :", volume_by_polynomial)
    print("integral by polynomial integration            :", integral_by_polynomial)
    print("average value by polynomial integration       :", average_by_polynomial)
    print("volume of E, pi / 2                           :", EXPECTED_VOLUME)
    print("triple integral of f, pi / 24                 :", EXPECTED_INTEGRAL)
    print("average value of f, 1 / 12                    :", EXPECTED_AVERAGE)
    assert abs(volume_by_polynomial - EXPECTED_VOLUME) < 1.0e-12
    assert abs(integral_by_polynomial - EXPECTED_INTEGRAL) < 1.0e-12
    assert abs(average_by_polynomial - EXPECTED_AVERAGE) < 1.0e-14
    # END CHECK reduced_polynomial_route

    # BEGIN CHECK direct_rejection_sample
    generator = np.random.default_rng(RANDOM_SEED)
    points = generator.uniform(-1.0, 1.0, size=(SAMPLE_COUNT, 2))
    heights = generator.uniform(0.0, 1.0, size=SAMPLE_COUNT)
    radius_squared = points[:, 0] ** 2 + points[:, 1] ** 2
    accepted = heights <= (1.0 - radius_squared)
    accepted_count = int(np.count_nonzero(accepted))
    values = radius_squared[accepted] * heights[accepted]
    average_by_sample = float(np.mean(values))
    standard_error = float(np.std(values, ddof=1)) / math.sqrt(accepted_count)
    print("accepted points of the sample                 :", accepted_count)
    print("average value by rejection sample             :", average_by_sample)
    print("standard error of that average                :", standard_error)
    print("average value, 1 / 12                         :", EXPECTED_AVERAGE)
    assert abs(average_by_sample - EXPECTED_AVERAGE) < SAMPLE_SIGMA * standard_error
    assert standard_error < 1.0e-3
    # END CHECK direct_rejection_sample

    # BEGIN CHECK volume_and_integral_from_sample
    box_volume = 4.0
    accepted_fraction = accepted_count / SAMPLE_COUNT
    volume_by_sample = box_volume * accepted_fraction
    integral_by_sample = volume_by_sample * average_by_sample
    print("volume by the same sample                     :", volume_by_sample)
    print("integral by the same sample                    :", integral_by_sample)
    print("product of the exact volume and the average    :", EXPECTED_VOLUME * EXPECTED_AVERAGE)
    assert abs(integral_by_sample - EXPECTED_INTEGRAL) < 1.0e-3
    # END CHECK volume_and_integral_from_sample

    # BEGIN CHECK exact_chain_identity
    volume_coefficient = Fraction(1, 2)
    integral_coefficient = Fraction(1, 24)
    chain = integral_coefficient / volume_coefficient
    print("coefficient ratio, exact                      :", chain)
    print("one twelfth, exact                            :", Fraction(1, 12))
    print("integral coefficient times two               :", 2 * integral_coefficient)
    assert chain == Fraction(1, 12)
    assert chain * volume_coefficient == integral_coefficient
    assert float(chain) == EXPECTED_AVERAGE
    assert float(integral_coefficient) * math.pi == EXPECTED_INTEGRAL
    # END CHECK exact_chain_identity

    print()
    print("summary of the solution")
    print("region E              : x^2 + y^2 <= 1, 0 <= z <= 1 - x^2 - y^2")
    print("projection on z = 0   : the closed disk x^2 + y^2 <= 1, area", math.pi)
    print("volume V(E)           : pi / 2 =", EXPECTED_VOLUME)
    print("triple integral of f  : pi / 24 =", EXPECTED_INTEGRAL)
    print("average value f_ave   : 1 / 12 =", EXPECTED_AVERAGE)
    print("largest value of f    : 1 / 4 at r^2 = 1/2 and z = 1/2")
    print("part5_verify: all checks passed")


if __name__ == "__main__":
    main()
