"""Verify the answer with a second integration order and with a Monte Carlo estimate.

The script integrates over x last, and it estimates the same integral from random points in a box.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import quad

PARABOLOID_FACTOR = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_X = 4.0
"""Coordinate x of the plane that closes the solid."""

EXACT_ANSWER = 16.0 * np.pi / 3.0
"""Value of the integral that parts 2 and 3 give."""

NUMERIC_TOLERANCE = 1.0e-9
"""Absolute tolerance for a one-dimensional quadrature."""

MONTE_CARLO_TOLERANCE = 5.0e-3
"""Largest accepted relative error of the Monte Carlo estimate."""

RANDOM_SEED = 20261122
"""Seed of the random points of the Monte Carlo estimate."""

NUMBER_OF_SAMPLES = 4_000_000
"""Number of random points of the Monte Carlo estimate."""


def check(name: str, computed: float, expected: float, tolerance: float) -> bool:
    """Print one checked value and its expected value.

    Args:
        name: Short name of the checked fact.
        computed: Value that the script computed.
        expected: Value that the reasoning predicts.
        tolerance: Largest accepted absolute difference.

    Returns:
        True when the absolute difference is at most the tolerance.
    """
    difference = abs(computed - expected)
    passed = difference <= tolerance
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    print(f"       computed   = {computed!r}")
    print(f"       expected   = {expected!r}")
    print(f"       difference = {difference:.3e}   tolerance = {tolerance:.1e}")
    return passed


def main() -> int:
    """Run the second order, the Monte Carlo estimate, and the rounding check.

    Returns:
        The number of failed checks.
    """
    failures = 0
    print("Part 4: independent checks")
    print("")

    # Step 4.1. Hold x fixed. The section of E is a disk of radius sqrt(x) / 2.
    print("Step 4.1: the order with x outermost")
    section_area = quad(lambda x: np.pi * x / PARABOLOID_FACTOR, 0.0, PLANE_X)[0]
    failures += not check("volume from the section areas", section_area, 2.0 * np.pi, 1.0e-9)
    section_at_plane = np.pi * PLANE_X / PARABOLOID_FACTOR
    failures += not check("area of the top section", section_at_plane, np.pi, 1.0e-12)
    by_sections = quad(lambda x: x * np.pi * x / PARABOLOID_FACTOR, 0.0, PLANE_X)[0]
    closed_form = (np.pi / PARABOLOID_FACTOR) * PLANE_X**3 / 3.0
    failures += not check("integral with x outermost", by_sections, EXACT_ANSWER, NUMERIC_TOLERANCE)
    failures += not check("closed form (pi / 4) (4^3 / 3)", closed_form, EXACT_ANSWER,
                          NUMERIC_TOLERANCE)
    print("")

    # Step 4.2. Average x over the bounding box, weighed by the volume of the box.
    print("Step 4.2: the Monte Carlo estimate")
    generator = np.random.default_rng(RANDOM_SEED)
    sample_x = generator.uniform(0.0, PLANE_X, NUMBER_OF_SAMPLES)
    sample_y = generator.uniform(-1.0, 1.0, NUMBER_OF_SAMPLES)
    sample_z = generator.uniform(-1.0, 1.0, NUMBER_OF_SAMPLES)
    in_solid = sample_x >= PARABOLOID_FACTOR * (sample_y**2 + sample_z**2)
    weights = np.where(in_solid, sample_x, 0.0)
    box_volume = float(PLANE_X * 2.0 * 2.0)
    estimate = box_volume * float(weights.mean())
    standard_error = box_volume * float(weights.std(ddof=1)) / np.sqrt(NUMBER_OF_SAMPLES)
    relative_error = abs(estimate - EXACT_ANSWER) / EXACT_ANSWER
    print(f"       samples in E        = {int(in_solid.sum())}")
    print(f"       estimate            = {estimate:.6f}")
    print(f"       exact value         = {EXACT_ANSWER:.6f}")
    print(f"       standard error      = {standard_error:.6f}")
    print(f"       relative difference = {relative_error:.5f}")
    passed = relative_error <= MONTE_CARLO_TOLERANCE
    print(f"[{'PASS' if passed else 'FAIL'}] relative difference within {MONTE_CARLO_TOLERANCE:.1e}")
    failures += not passed
    print("")

    rounding = round(EXACT_ANSWER, 4)
    failures += not check("answer rounded to four decimals", rounding, 16.7552, 1.0e-12)
    print(f"exact value = {EXACT_ANSWER!r}")
    print(f"checks failed: {failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
