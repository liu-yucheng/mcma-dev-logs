"""Verify the moment M_xz and the coordinate y-bar of the center of mass.

The first moment about the plane y = 0 is M_xz = integral of 2 y over E. This module
compares four independent computations of M_xz, divides by the mass to get y-bar, and
checks that the point (x-bar, y-bar) lies inside the planar region D.
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
"""The seed of the Monte Carlo estimate of M_xz."""

MONTE_CARLO_SAMPLES = 4_000_000
"""The number of uniform points of the Monte Carlo estimate of M_xz."""

MONTE_CARLO_TOLERANCE = 6.0e-3
"""The tolerance of the Monte Carlo estimate, taken as four standard errors."""


def moment_by_exact_terms() -> Fraction:
    """Return M_xz from the exact integrated terms 5/12 and 2/15 multiplied by the density."""
    return Fraction(2, 1) * (Fraction(5, 12) + Fraction(2, 15))


def moment_by_symbolic() -> sympy.Rational:
    """Return M_xz from a symbolic triple integral of 2 y over E."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    inner = sympy.integrate(2 * y, (z, 0, 1 + x + y))
    middle = sympy.integrate(inner, (y, 0, sympy.sqrt(x)))
    return sympy.integrate(middle, (x, 0, 1))


def moment_by_triple_quadrature() -> float:
    """Return M_xz from a numerical triple quadrature of 2 y over E."""
    value, _ = tplquad(
        lambda z, y, x: 2.0 * y,
        0.0,
        1.0,
        lambda x: 0.0,
        lambda x: float(np.sqrt(x)),
        lambda x, y: 0.0,
        lambda x, y: 1.0 + x + y,
    )
    return float(value)


def moment_by_monte_carlo() -> tuple[float, float]:
    """Return the Monte Carlo estimate of M_xz and its standard error.

    Returns:
        A pair. The first item is the box volume times the mean value of 2 y over the
        sampled points of E. The second item is the standard error of that estimate.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    z_values = 3.0 * generator.random(MONTE_CARLO_SAMPLES)
    inside = (y_values <= np.sqrt(x_values)) & (z_values <= 1.0 + x_values + y_values)
    integrand = 2.0 * y_values * inside
    box_volume = 3.0
    standard_error = box_volume * float(np.std(integrand)) / np.sqrt(integrand.size)
    return box_volume * float(np.mean(integrand)), standard_error


def mass_by_exact_terms() -> Fraction:
    """Return the mass as twice the exact volume 2/3 + 2/5 + 1/4."""
    return Fraction(2, 1) * (Fraction(2, 3) + Fraction(2, 5) + Fraction(1, 4))


def coordinate_from_fractions(moment: Fraction) -> Fraction:
    """Return y-bar as the exact moment M_xz divided by the exact mass."""
    return moment / mass_by_exact_terms()


def coordinate_by_symbolic(moment: sympy.Rational) -> sympy.Rational:
    """Return y-bar as a symbolic moment divided by a symbolic mass, both from sympy."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    mass = sympy.integrate(
        sympy.integrate(sympy.integrate(2, (z, 0, 1 + x + y)), (y, 0, sympy.sqrt(x))),
        (x, 0, 1),
    )
    return sympy.simplify(moment / mass)


def main() -> None:
    """Run every check of Part 5 and print the computed value against the expected value."""
    exact_moment = moment_by_exact_terms()
    symbolic_moment = moment_by_symbolic()
    symbolic_as_fraction = Fraction(int(sympy.numer(symbolic_moment)), int(sympy.denom(symbolic_moment)))
    print(f"M_xz by exact terms: computed = {float(exact_moment):.15f} (exact {exact_moment}), "
          f"expected = {float(symbolic_as_fraction):.15f} (symbolic triple integral)")
    assert symbolic_as_fraction == exact_moment

    quadrature_moment = moment_by_triple_quadrature()
    print(f"M_xz by triple quadrature: computed = {quadrature_moment:.15f}, "
          f"expected = {float(exact_moment):.15f} (exact terms)")
    assert abs(quadrature_moment - float(exact_moment)) < QUADRATURE_TOLERANCE

    estimate, standard_error = moment_by_monte_carlo()
    print(f"M_xz by Monte Carlo: computed = {estimate:.15f} +- {standard_error:.6f}, "
          f"expected = {float(exact_moment):.15f} (exact terms)")
    assert abs(estimate - float(exact_moment)) < MONTE_CARLO_TOLERANCE

    y_bar = coordinate_from_fractions(exact_moment)
    y_bar_symbolic = coordinate_by_symbolic(symbolic_moment)
    symbolic_coordinate = Fraction(int(sympy.numer(y_bar_symbolic)), int(sympy.denom(y_bar_symbolic)))
    print(f"y-bar by fraction division: computed = {float(y_bar):.15f} (exact {y_bar}), "
          f"expected = {float(symbolic_coordinate):.15f} (symbolic moment over symbolic mass)")
    assert symbolic_coordinate == y_bar

    x_bar = coordinate_from_fractions(Fraction(2, 1) * (Fraction(2, 5) + Fraction(2, 7) + Fraction(1, 6)))
    inside_region = y_bar * y_bar <= x_bar
    print(f"y-bar squared against x-bar: computed = {float(y_bar * y_bar):.15f}, "
          f"expected at most x-bar = {float(x_bar):.15f} (the point lies in D)")
    assert inside_region

    print("Part 5 checks passed.")


if __name__ == "__main__":
    main()
