"""Verify the moment M_yz and the coordinate x-bar of the center of mass.

The first moment about the plane x = 0 is M_yz = integral of 2 x over E. This module
compares four independent computations of M_yz, then divides by the mass to get x-bar, and
checks that x-bar lies inside the x-extent of D.
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
"""The seed of the Monte Carlo estimate of x-bar."""

MONTE_CARLO_SAMPLES = 4_000_000
"""The number of uniform points of the Monte Carlo estimate of x-bar."""

MONTE_CARLO_TOLERANCE = 6.0e-3
"""The tolerance of the Monte Carlo estimate, taken as four standard errors."""


def moment_by_exact_terms() -> Fraction:
    """Return M_yz from the exact integrated terms 2/5, 2/7, and 1/6 multiplied by the density."""
    return Fraction(2, 1) * (Fraction(2, 5) + Fraction(2, 7) + Fraction(1, 6))


def moment_by_symbolic() -> sympy.Rational:
    """Return M_yz from a symbolic triple integral of 2 x over E."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    inner = sympy.integrate(2 * x, (z, 0, 1 + x + y))
    middle = sympy.integrate(inner, (y, 0, sympy.sqrt(x)))
    return sympy.integrate(middle, (x, 0, 1))


def moment_by_triple_quadrature() -> float:
    """Return M_yz from a numerical triple quadrature of 2 x over E."""
    value, _ = tplquad(
        lambda z, y, x: 2.0 * x,
        0.0,
        1.0,
        lambda x: 0.0,
        lambda x: float(np.sqrt(x)),
        lambda x, y: 0.0,
        lambda x, y: 1.0 + x + y,
    )
    return float(value)


def moment_by_monte_carlo() -> tuple[float, float]:
    """Return the Monte Carlo estimate of M_yz and its standard error.

    Returns:
        A pair. The first item is the box volume times the mean value of 2 x over the
        sampled points of E. The second item is the standard error of that estimate.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    z_values = 3.0 * generator.random(MONTE_CARLO_SAMPLES)
    inside = (y_values <= np.sqrt(x_values)) & (z_values <= 1.0 + x_values + y_values)
    integrand = 2.0 * x_values * inside
    box_volume = 3.0
    standard_error = box_volume * float(np.std(integrand)) / np.sqrt(integrand.size)
    return box_volume * float(np.mean(integrand)), standard_error


def mass_by_exact_terms() -> Fraction:
    """Return the mass as twice the exact volume 2/3 + 2/5 + 1/4."""
    return Fraction(2, 1) * (Fraction(2, 3) + Fraction(2, 5) + Fraction(1, 4))


def coordinate_from_fractions(moment: Fraction) -> Fraction:
    """Return x-bar as the exact moment M_yz divided by the exact mass."""
    return moment / mass_by_exact_terms()


def coordinate_by_symbolic(moment: sympy.Rational) -> sympy.Rational:
    """Return x-bar as a symbolic moment divided by a symbolic mass, both from sympy."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    mass = sympy.integrate(
        sympy.integrate(sympy.integrate(2, (z, 0, 1 + x + y)), (y, 0, sympy.sqrt(x))),
        (x, 0, 1),
    )
    return sympy.simplify(moment / mass)


def main() -> None:
    """Run every check of Part 4 and print the computed value against the expected value."""
    exact_moment = moment_by_exact_terms()
    symbolic_moment = moment_by_symbolic()
    symbolic_as_fraction = Fraction(int(sympy.numer(symbolic_moment)), int(sympy.denom(symbolic_moment)))
    print(f"M_yz by exact terms: computed = {float(exact_moment):.15f} (exact {exact_moment}), "
          f"expected = {float(symbolic_as_fraction):.15f} (symbolic triple integral)")
    assert symbolic_as_fraction == exact_moment

    quadrature_moment = moment_by_triple_quadrature()
    print(f"M_yz by triple quadrature: computed = {quadrature_moment:.15f}, "
          f"expected = {float(exact_moment):.15f} (exact terms)")
    assert abs(quadrature_moment - float(exact_moment)) < QUADRATURE_TOLERANCE

    estimate, standard_error = moment_by_monte_carlo()
    print(f"M_yz by Monte Carlo: computed = {estimate:.15f} +- {standard_error:.6f}, "
          f"expected = {float(exact_moment):.15f} (exact terms)")
    assert abs(estimate - float(exact_moment)) < MONTE_CARLO_TOLERANCE

    x_bar = coordinate_from_fractions(exact_moment)
    x_bar_symbolic = coordinate_by_symbolic(symbolic_moment)
    symbolic_coordinate = Fraction(int(sympy.numer(x_bar_symbolic)), int(sympy.denom(x_bar_symbolic)))
    print(f"x-bar by fraction division: computed = {float(x_bar):.15f} "
          f"(exact {x_bar}), expected = {float(symbolic_coordinate):.15f} "
          f"(symbolic moment over symbolic mass)")
    assert symbolic_coordinate == x_bar

    quotient_by_quadrature = quadrature_moment / float(mass_by_exact_terms())
    print(f"x-bar by quadrature moment over exact mass: computed = {quotient_by_quadrature:.15f}, "
          f"expected = {float(x_bar):.15f} (fraction division)")
    assert abs(quotient_by_quadrature - float(x_bar)) < QUADRATURE_TOLERANCE

    inside_extent = 0.0 < float(x_bar) < 1.0
    print(f"x-bar inside the x-extent [0, 1] of D: computed = {inside_extent}, expected = True")
    assert inside_extent

    print("Part 4 checks passed.")


if __name__ == "__main__":
    main()
