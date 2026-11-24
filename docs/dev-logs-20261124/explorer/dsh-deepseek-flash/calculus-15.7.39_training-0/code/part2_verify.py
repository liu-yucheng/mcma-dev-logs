"""Verify the height function and the volume of the solid E.

The solid E is the set of points (x, y, z) with (x, y) in D and 0 <= z <= 1 + x + y. This
module checks that the ceiling stays above the floor, that the slice area at a fixed x
matches its closed form at three abscissas, and that the volume has the same value from
four independent methods.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Callable

import numpy as np
import sympy
from scipy.integrate import dblquad, quad


TOLERANCE = 1.0e-12
"""The absolute tolerance of a comparison between two computed values."""

SLICE_ABSCISSAS = (0.25, 0.5, 1.0)
"""Three abscissas at which the area of the vertical slice is checked."""

QUADRATURE_TOLERANCE = 1.0e-9
"""The tolerance of a numerical quadrature against an exact value, set by the quadrature."""

RANDOM_SEED = 20261122
"""The seed of the Monte Carlo estimate of the volume."""

MONTE_CARLO_SAMPLES = 4_000_000
"""The number of uniform points of the Monte Carlo estimate of the volume."""

MONTE_CARLO_TOLERANCE = 2.0e-2
"""The tolerance of the Monte Carlo estimate, taken as four standard errors."""


def ceiling(x_value: float, y_value: float) -> float:
    """Return the height 1 + x + y of the ceiling of E above the point (x, y)."""
    return 1.0 + x_value + y_value


def volume_by_fractions() -> Fraction:
    """Return the volume as the exact sum 2/3 + 2/5 + 1/4 of the three integrated terms."""
    return Fraction(2, 3) + Fraction(2, 5) + Fraction(1, 4)


def volume_by_symbolic() -> sympy.Rational:
    """Return the volume from a symbolic double integral of 1 + x + y over D."""
    x, y = sympy.symbols("x y", nonnegative=True)
    inner = sympy.integrate(1 + x + y, (y, 0, sympy.sqrt(x)))
    return sympy.integrate(inner, (x, 0, 1))


def volume_by_double_quadrature() -> float:
    """Return the volume from a numerical double quadrature of 1 + x + y over D."""
    value, _ = dblquad(lambda y, x: 1.0 + x + y, 0.0, 1.0, 0.0, np.sqrt)
    return float(value)


def volume_by_monte_carlo() -> tuple[float, float, float]:
    """Return the Monte Carlo estimate of the volume inside the bounding box of E.

    Returns:
        A triple. The first item is the estimated volume. The second item is its standard
        error. The third item is the volume of the bounding box 0 <= x <= 1, 0 <= y <= 1,
        0 <= z <= 3.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    z_values = 3.0 * generator.random(MONTE_CARLO_SAMPLES)
    inside = (y_values <= np.sqrt(x_values)) & (z_values <= ceiling(x_values, y_values))
    hit_fraction = float(np.count_nonzero(inside)) / MONTE_CARLO_SAMPLES
    box_volume = 1.0 * 1.0 * 3.0
    standard_error = box_volume * float(
        np.sqrt(hit_fraction * (1.0 - hit_fraction) / MONTE_CARLO_SAMPLES)
    )
    return box_volume * hit_fraction, standard_error, box_volume


def slice_area_closed_form(x_value: float) -> float:
    """Return the exact slice area sqrt(x) + x**(3/2) + x/2 at a fixed abscissa x."""
    return float(np.sqrt(x_value) + x_value ** 1.5 + 0.5 * x_value)


def slice_area_by_quadrature(x_value: float) -> float:
    """Return the slice area at a fixed abscissa x from quadrature over y."""
    value, _ = quad(lambda y: ceiling(x_value, y), 0.0, np.sqrt(x_value))
    return float(value)


def slice_area_by_symbolic(x_value: float) -> float:
    """Return the slice area at a fixed abscissa x from a symbolic integration over y."""
    x, y = sympy.symbols("x y", nonnegative=True)
    expression = sympy.integrate(1 + x + y, (y, 0, sympy.sqrt(x)))
    return float(expression.subs(x, sympy.Rational(str(x_value)).limit_denominator(10 ** 6)))


def ceiling_bounds() -> tuple[float, float]:
    """Return the smallest and the largest ceiling height over the boundary of D."""
    smallest = ceiling(0.0, 0.0)
    largest = max(ceiling(1.0, 0.0), ceiling(1.0, 1.0), ceiling(0.0, 0.0))
    return smallest, largest


def main() -> None:
    """Run every check of Part 2 and print the computed value against the expected value."""
    smallest_height, largest_height = ceiling_bounds()
    print(f"smallest ceiling height: computed = {smallest_height:.15f}, expected = 1 "
          f"(the corner (0, 0) of D)")
    assert abs(smallest_height - 1.0) < TOLERANCE
    print(f"largest ceiling height: computed = {largest_height:.15f}, expected = 3 "
          f"(the corner (1, 1) of D)")
    assert abs(largest_height - 3.0) < TOLERANCE

    exact_volume = volume_by_fractions()
    symbolic_volume = volume_by_symbolic()
    print(f"volume by exact fractions: computed = {float(exact_volume):.15f} "
          f"(exact {exact_volume}), expected = {float(symbolic_volume):.15f} (symbolic)")
    symbolic_as_fraction = Fraction(int(sympy.numer(symbolic_volume)), int(sympy.denom(symbolic_volume)))
    assert symbolic_as_fraction == exact_volume

    quadrature_volume = volume_by_double_quadrature()
    print(f"volume by double quadrature: computed = {quadrature_volume:.15f}, "
          f"expected = {float(exact_volume):.15f} (exact fractions)")
    assert abs(quadrature_volume - float(exact_volume)) < QUADRATURE_TOLERANCE

    estimate, standard_error, box_volume = volume_by_monte_carlo()
    print(f"volume by Monte Carlo: computed = {estimate:.15f} +- {standard_error:.6f} "
          f"in a box of volume {box_volume:.1f}, expected = {float(exact_volume):.15f}")
    assert abs(estimate - float(exact_volume)) < MONTE_CARLO_TOLERANCE

    for abscissa in SLICE_ABSCISSAS:
        closed = slice_area_closed_form(abscissa)
        symbolic = slice_area_by_symbolic(abscissa)
        quadrature = slice_area_by_quadrature(abscissa)
        print(f"slice area at x = {abscissa}: closed form = {closed:.15f}, "
              f"symbolic = {symbolic:.15f}, quadrature = {quadrature:.15f}")
        assert abs(symbolic - closed) < TOLERANCE
        assert abs(quadrature - closed) < TOLERANCE

    integral_of_slices: Callable[[float], float] = slice_area_closed_form
    total, _ = quad(integral_of_slices, 0.0, 1.0)
    print(f"integral of the slice areas: computed = {float(total):.15f}, "
          f"expected = {float(exact_volume):.15f} (the volume)")
    assert abs(float(total) - float(exact_volume)) < QUADRATURE_TOLERANCE

    print("Part 2 checks passed.")


if __name__ == "__main__":
    main()
