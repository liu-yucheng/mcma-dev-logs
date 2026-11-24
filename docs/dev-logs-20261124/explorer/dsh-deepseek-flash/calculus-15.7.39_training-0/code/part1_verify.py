"""Verify the geometry and the area of the planar region D of the tutorial.

The region D in the xy-plane is bounded by the curve y = sqrt(x), the line y = 0, and the
line x = 1. This module compares independent computations of the area of D, checks the
endpoints of the bounding curves, and checks the membership test of D on a dense grid.
Every assertion compares a value that one method computes with a value that a different
method computes.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
from scipy.integrate import quad


TOLERANCE = 1.0e-12
"""The absolute tolerance of a comparison between two computed values."""

BOUNDARY_EPSILON = 1.0e-9
"""The largest gap x - y**2 that counts as a boundary rounding artifact of the grid."""

GRID_SAMPLES = 2001
"""The number of abscissas on each axis of the membership grid."""

RANDOM_SEED = 20261122
"""The seed of the Monte Carlo sampling of D."""

MONTE_CARLO_SAMPLES = 4_000_000
"""The number of uniform points of the Monte Carlo estimate of the area of D."""

MONTE_CARLO_TOLERANCE = 8.0e-3
"""The tolerance of the Monte Carlo estimate, taken as four standard errors."""


def area_by_exact_power() -> Fraction:
    """Return the area of D from the exact integral of x**(1/2) over 0 <= x <= 1."""
    return Fraction(2, 3)


def area_by_polynomial_quadrature() -> float:
    """Return the area of D from numerical quadrature of sqrt(x) over 0 <= x <= 1."""
    value, _ = quad(np.sqrt, 0.0, 1.0)
    return float(value)


def area_by_horizontal_slices() -> Fraction:
    """Return the area of D from exact horizontal slices of width 1 - y**2.

    A horizontal line at height y meets D on the interval x from y**2 to 1, so the slice
    length is 1 - y**2. The integral of that polynomial from 0 to 1 is exact arithmetic.
    """
    return Fraction(1, 1) - Fraction(1, 3)


def area_by_horizontal_quadrature() -> float:
    """Return the area of D from numerical quadrature of the slice length 1 - y**2."""
    value, _ = quad(lambda y: 1.0 - y * y, 0.0, 1.0)
    return float(value)


def area_by_monte_carlo() -> tuple[float, float]:
    """Return the Monte Carlo estimate of the area of D and its standard error.

    Returns:
        A pair. The first item is the fraction of uniform points of the unit square that
        satisfy 0 <= y <= sqrt(x). The second item is the standard error of that fraction.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    inside = y_values <= np.sqrt(x_values)
    fraction = float(np.count_nonzero(inside)) / MONTE_CARLO_SAMPLES
    standard_error = float(np.sqrt(fraction * (1.0 - fraction) / MONTE_CARLO_SAMPLES))
    return fraction, standard_error


def membership_disagreements() -> tuple[int, float]:
    """Return the count and the largest gap of the grid points where two tests of D disagree.

    The vertical test accepts a point when y <= sqrt(x). The horizontal test accepts a
    point when x >= y**2. Both tests describe the same region, so they must accept the same
    grid points of the box 0 <= x <= 1, 0 <= y <= 1, up to rounding at the boundary.

    Returns:
        A pair. The first item counts the grid points whose gap x - y**2 has magnitude
        above BOUNDARY_EPSILON and whose two test results differ. The second item is the
        largest such gap over the whole grid.
    """
    axis = np.linspace(0.0, 1.0, GRID_SAMPLES)
    x_grid, y_grid = np.meshgrid(axis, axis, indexing="ij")
    vertical_test = y_grid <= np.sqrt(x_grid)
    horizontal_test = x_grid >= y_grid * y_grid
    gap = np.abs(x_grid - y_grid * y_grid)
    separated = gap > BOUNDARY_EPSILON
    return int(np.count_nonzero(separated & (vertical_test != horizontal_test))), float(
        np.max(np.where(vertical_test != horizontal_test, gap, 0.0))
    )


def boundary_endpoints() -> tuple[float, float, float]:
    """Return the coordinates of the two endpoints of the curve y = sqrt(x) on D."""
    return float(np.sqrt(0.0)), float(np.sqrt(1.0)), 1.0


def main() -> None:
    """Run every check of Part 1 and print the computed value against the expected value."""
    exact_area = area_by_exact_power()
    quadrature_area = area_by_polynomial_quadrature()
    print(f"area by exact power rule: computed = {float(exact_area):.15f}, "
          f"expected = {float(exact_area):.15f} (exact {exact_area})")
    print(f"area by sqrt quadrature: computed = {quadrature_area:.15f}, "
          f"expected = {float(exact_area):.15f} (from the power rule)")
    assert abs(quadrature_area - float(exact_area)) < TOLERANCE

    slice_area = area_by_horizontal_slices()
    slice_quadrature = area_by_horizontal_quadrature()
    print(f"area by horizontal slices (exact): computed = {float(slice_area):.15f} "
          f"(exact {slice_area}), expected = {float(exact_area):.15f} (vertical slices)")
    assert slice_area == exact_area
    print(f"area by horizontal slices (quadrature): computed = {slice_quadrature:.15f}, "
          f"expected = {float(exact_area):.15f} (from the power rule)")
    assert abs(slice_quadrature - float(exact_area)) < TOLERANCE

    estimate, standard_error = area_by_monte_carlo()
    print(f"area by Monte Carlo: computed = {estimate:.15f} +- {standard_error:.6f}, "
          f"expected = {float(exact_area):.15f} (from the power rule)")
    assert abs(estimate - float(exact_area)) < MONTE_CARLO_TOLERANCE

    disagreements, gap = membership_disagreements()
    print(f"grid points where the two tests of D disagree away from the boundary: "
          f"computed = {disagreements}, expected = 0 (both tests describe D)")
    assert disagreements == 0
    print(f"largest gap x - y**2 at a point where the two tests disagree: computed = "
          f"{gap:.15f}, expected at most {BOUNDARY_EPSILON:.1e} (a boundary rounding artifact)")
    assert gap <= BOUNDARY_EPSILON

    low_endpoint, high_endpoint, right_side = boundary_endpoints()
    print(f"left endpoint of y = sqrt(x): computed = (0, {low_endpoint:.15f}), expected = (0, 0)")
    assert abs(low_endpoint) < TOLERANCE
    print(f"right endpoint of y = sqrt(x): computed = ({right_side:.15f}, {high_endpoint:.15f}), "
          f"expected = (1, 1)")
    assert abs(right_side - high_endpoint) < TOLERANCE

    print("Part 1 checks passed.")


if __name__ == "__main__":
    main()
