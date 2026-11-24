"""Verify the moment M_xy, the coordinate z-bar, and the complete center of mass.

The first moment about the plane z = 0 is M_xy = integral of 2 z over E. This module
compares independent computations of M_xy, divides by the mass to get z-bar, assembles the
center of mass, and checks all three coordinates against one Monte Carlo average.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy.integrate import tplquad


TOLERANCE = 1.0e-12
"""The absolute tolerance of a comparison between two computed values."""

QUADRATURE_TOLERANCE = 1.0e-9
"""The tolerance of a numerical quadrature against an exact value, set by the quadrature."""

RANDOM_SEED = 20261122
"""The seed of the Monte Carlo estimate of the three coordinates."""

MONTE_CARLO_SAMPLES = 6_000_000
"""The number of uniform points of the Monte Carlo estimate of the coordinates."""

MONTE_CARLO_TOLERANCE = 6.0e-3
"""The tolerance of each Monte Carlo coordinate, taken as four standard errors."""


def moment_by_exact_terms() -> Fraction:
    """Return M_xy from the exact integrated terms 184/105, 5/6, and 2/15."""
    return Fraction(184, 105) + Fraction(5, 6) + Fraction(2, 15)


def moment_by_symbolic() -> sympy.Rational:
    """Return M_xy from a symbolic triple integral of 2 z over E."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    inner = sympy.integrate(2 * z, (z, 0, 1 + x + y))
    middle = sympy.integrate(inner, (y, 0, sympy.sqrt(x)))
    return sympy.integrate(middle, (x, 0, 1))


def moment_by_triple_quadrature() -> float:
    """Return M_xy from a numerical triple quadrature of 2 z over E."""
    value, _ = tplquad(
        lambda z, y, x: 2.0 * z,
        0.0,
        1.0,
        lambda x: 0.0,
        lambda x: float(np.sqrt(x)),
        lambda x, y: 0.0,
        lambda x, y: 1.0 + x + y,
    )
    return float(value)


def coordinates_by_monte_carlo() -> tuple[np.ndarray, np.ndarray]:
    """Return the Monte Carlo estimate of the center of mass and its standard errors.

    Returns:
        A pair of arrays of three items each. The first array holds x-bar, y-bar, and
        z-bar. The second array holds their standard errors.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    z_values = 3.0 * generator.random(MONTE_CARLO_SAMPLES)
    inside = (y_values <= np.sqrt(x_values)) & (z_values <= 1.0 + x_values + y_values)
    points = np.stack([x_values[inside], y_values[inside], z_values[inside]])
    estimates = points.mean(axis=1)
    standard_errors = points.std(axis=1) / np.sqrt(points.shape[1])
    return estimates, standard_errors


def main() -> None:
    """Run every check of Part 6 and print the computed value against the expected value."""
    exact_moment = moment_by_exact_terms()
    symbolic_moment = moment_by_symbolic()
    symbolic_as_fraction = Fraction(int(sympy.numer(symbolic_moment)), int(sympy.denom(symbolic_moment)))
    print(f"M_xy by exact terms: computed = {float(exact_moment):.15f} (exact {exact_moment}), "
          f"expected = {float(symbolic_as_fraction):.15f} (symbolic triple integral)")
    assert symbolic_as_fraction == exact_moment

    quadrature_moment = moment_by_triple_quadrature()
    print(f"M_xy by triple quadrature: computed = {quadrature_moment:.15f}, "
          f"expected = {float(exact_moment):.15f} (exact terms)")
    assert abs(quadrature_moment - float(exact_moment)) < QUADRATURE_TOLERANCE

    mass = Fraction(2, 1) * (Fraction(2, 3) + Fraction(2, 5) + Fraction(1, 4))
    z_bar = exact_moment / mass
    z_bar_symbolic = sympy.simplify(symbolic_moment / sympy.Rational(79, 30))
    symbolic_coordinate = Fraction(int(sympy.numer(z_bar_symbolic)), int(sympy.denom(z_bar_symbolic)))
    print(f"z-bar by fraction division: computed = {float(z_bar):.15f} (exact {z_bar}), "
          f"expected = {float(symbolic_coordinate):.15f} (symbolic moment over 79/30)")
    assert symbolic_coordinate == z_bar

    x_bar = Fraction(2, 1) * (Fraction(2, 5) + Fraction(2, 7) + Fraction(1, 6)) / mass
    y_bar = Fraction(2, 1) * (Fraction(5, 12) + Fraction(2, 15)) / mass
    center = (x_bar, y_bar, z_bar)
    print(f"center of mass (exact): computed = ({center[0]}, {center[1]}, {center[2]}), "
          f"expected = ({float(center[0]):.6f}, {float(center[1]):.6f}, "
          f"{float(center[2]):.6f}) as decimals")

    estimates, standard_errors = coordinates_by_monte_carlo()
    for index, name in enumerate(("x-bar", "y-bar", "z-bar")):
        computed = float(estimates[index])
        expected = float(center[index])
        print(f"{name} by Monte Carlo: computed = {computed:.15f} +- "
              f"{float(standard_errors[index]):.6f}, expected = {expected:.15f} "
              f"(exact quotient)")
        assert abs(computed - expected) < MONTE_CARLO_TOLERANCE

    height_at_center = 1.0 + float(center[0]) + float(center[1])
    below_ceiling = float(center[2]) < height_at_center
    print(f"z-bar below the ceiling above (x-bar, y-bar): computed = {float(center[2]):.15f}, "
          f"expected below {height_at_center:.15f} (the center of mass lies inside E)")
    assert below_ceiling

    mass_by_quadrature = tplquad(
        lambda z, y, x: 2.0,
        0.0,
        1.0,
        lambda x: 0.0,
        lambda x: float(np.sqrt(x)),
        lambda x, y: 0.0,
        lambda x, y: 1.0 + x + y,
    )[0]
    quotient_by_quadrature = quadrature_moment / float(mass_by_quadrature)
    print(f"z-bar by quadrature moment and quadrature mass: computed = "
          f"{quotient_by_quadrature:.15f}, expected = {float(z_bar):.15f} (exact quotient)")
    assert abs(quotient_by_quadrature - float(z_bar)) < QUADRATURE_TOLERANCE

    print("Part 6 checks passed.")


if __name__ == "__main__":
    main()
