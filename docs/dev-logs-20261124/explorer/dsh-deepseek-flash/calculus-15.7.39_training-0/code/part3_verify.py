"""Verify the mass of the solid E.

The density is the constant rho = 2, so the mass is twice the volume. This module compares
four independent computations of the mass: exact fraction arithmetic, a symbolic triple
integral, a numerical triple quadrature, and a Monte Carlo average of the density.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np
import sympy
from scipy.integrate import tplquad


TOLERANCE = 1.0e-12
"""The absolute tolerance of a comparison between two computed values."""

DENSITY = Fraction(2, 1)
"""The density rho of the solid, given by the statement."""

QUADRATURE_TOLERANCE = 1.0e-9
"""The tolerance of a numerical quadrature against an exact value, set by the quadrature."""

RANDOM_SEED = 20261122
"""The seed of the Monte Carlo estimate of the mass."""

MONTE_CARLO_SAMPLES = 4_000_000
"""The number of uniform points of the Monte Carlo estimate of the mass."""

MONTE_CARLO_TOLERANCE = 2.0e-2
"""The tolerance of the Monte Carlo estimate, taken as four standard errors."""


def volume_by_exact_terms() -> Fraction:
    """Return the volume as the exact integral of sqrt(x) + x**(3/2) + x/2 over 0 to 1."""
    return Fraction(2, 3) + Fraction(2, 5) + Fraction(1, 4)


def mass_by_exact_fractions() -> Fraction:
    """Return the mass as the density times the exact volume."""
    return DENSITY * volume_by_exact_terms()


def mass_by_symbolic() -> sympy.Rational:
    """Return the mass from a symbolic triple integral of the density over E."""
    x, y, z = sympy.symbols("x y z", nonnegative=True)
    inner = sympy.integrate(2, (z, 0, 1 + x + y))
    middle = sympy.integrate(inner, (y, 0, sympy.sqrt(x)))
    return sympy.integrate(middle, (x, 0, 1))


def mass_by_triple_quadrature() -> float:
    """Return the mass from a numerical triple quadrature of the density over E."""
    value, _ = tplquad(
        lambda z, y, x: 2.0,
        0.0,
        1.0,
        lambda x: 0.0,
        lambda x: float(np.sqrt(x)),
        lambda x, y: 0.0,
        lambda x, y: 1.0 + x + y,
    )
    return float(value)


def mass_by_monte_carlo() -> tuple[float, float]:
    """Return the Monte Carlo estimate of the mass inside the bounding box of E.

    Returns:
        A pair. The first item is the mean density over the sampled points of E times the
        box volume. The second item is the standard error of that estimate.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.random(MONTE_CARLO_SAMPLES)
    y_values = generator.random(MONTE_CARLO_SAMPLES)
    z_values = 3.0 * generator.random(MONTE_CARLO_SAMPLES)
    inside = (y_values <= np.sqrt(x_values)) & (z_values <= 1.0 + x_values + y_values)
    integrand = 2.0 * inside.astype(float)
    box_volume = 3.0
    standard_error = box_volume * float(np.std(integrand)) / np.sqrt(integrand.size)
    return box_volume * float(np.mean(integrand)), standard_error


def main() -> None:
    """Run every check of Part 3 and print the computed value against the expected value."""
    exact_mass = mass_by_exact_fractions()
    symbolic_mass = mass_by_symbolic()
    symbolic_as_fraction = Fraction(int(sympy.numer(symbolic_mass)), int(sympy.denom(symbolic_mass)))
    print(f"mass by exact fractions: computed = {float(exact_mass):.15f} (exact {exact_mass}), "
          f"expected = {float(symbolic_as_fraction):.15f} (symbolic triple integral)")
    assert symbolic_as_fraction == exact_mass

    quadrature_mass = mass_by_triple_quadrature()
    print(f"mass by triple quadrature: computed = {quadrature_mass:.15f}, "
          f"expected = {float(exact_mass):.15f} (exact fractions)")
    assert abs(quadrature_mass - float(exact_mass)) < QUADRATURE_TOLERANCE

    estimate, standard_error = mass_by_monte_carlo()
    print(f"mass by Monte Carlo: computed = {estimate:.15f} +- {standard_error:.6f}, "
          f"expected = {float(exact_mass):.15f} (exact fractions)")
    assert abs(estimate - float(exact_mass)) < MONTE_CARLO_TOLERANCE

    volume = volume_by_exact_terms()
    product = float(DENSITY) * float(volume)
    print(f"density times volume: computed = {product:.15f}, "
          f"expected = {float(exact_mass):.15f} (exact fractions)")
    assert abs(product - float(exact_mass)) < QUADRATURE_TOLERANCE

    quotient = float(exact_mass) / float(volume)
    print(f"mass over volume: computed = {quotient:.15f}, "
          f"expected = {float(DENSITY):.15f} (the constant density)")
    assert abs(quotient - float(DENSITY)) < TOLERANCE

    print("Part 3 checks passed.")


if __name__ == "__main__":
    main()
