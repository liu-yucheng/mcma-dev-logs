"""Verify the triple integral of f(x, y, z) = x^2 z + y^2 z over the region E.

The script computes the integral by four methods that do not share a formula:
an exact rational integral in the radius, an exact rational integral over the
horizontal sections, a three-dimensional adaptive quadrature in Cartesian
coordinates, and a rejection sample in the bounding box. It also computes the
value of each common wrong integrand, so that the tutorial can name the error
that produces that value.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

import numpy as np
from scipy.integrate import dblquad, tplquad

POLYNOMIAL_PAIRS = Sequence[tuple[Fraction, int]]
SAMPLE_COUNT = 400000
RANDOM_SEED = 20261123
SAMPLE_SIGMA = 4.0


def integrate_monomials(terms: POLYNOMIAL_PAIRS, lower: Fraction, upper: Fraction) -> Fraction:
    """Integrate a sum of monomials exactly on an interval of rational numbers.

    Args:
        terms: A sequence of pairs. Each pair holds a rational coefficient and an
            integer exponent.
        lower: The lower limit of the integral.
        upper: The upper limit of the integral.

    Returns:
        The exact value of the integral as a rational number.
    """
    total = Fraction(0, 1)
    for coefficient, exponent in terms:
        power = exponent + 1
        total += coefficient * (Fraction(upper) ** power - Fraction(lower) ** power) / power
    return total


def integrand_for_quadrature(z_value: float, y_value: float, x_value: float) -> float:
    """Return f(x, y, z) = x^2 z + y^2 z in the argument order of tplquad.

    The function scipy.integrate.tplquad calls its integrand with the innermost
    variable first, so the height z is the first argument here.
    """
    return (x_value * x_value + y_value * y_value) * z_value


def main() -> None:
    """Run every check of Part 3 and print each computed value beside its reference."""
    # BEGIN CHECK exact_cylindrical_route
    radial_terms = [
        (Fraction(1, 2), 3),
        (Fraction(-1, 1), 5),
        (Fraction(1, 2), 7),
    ]
    radial_piece = integrate_monomials(radial_terms, Fraction(0, 1), Fraction(1, 1))
    coefficient_cylindrical = 2 * radial_piece
    print("integral of r^3 (1 - r^2)^2 / 2 on [0, 1]    :", radial_piece)
    print("coefficient of pi, cylindrical route         :", coefficient_cylindrical)
    assert coefficient_cylindrical == Fraction(1, 24)
    # END CHECK exact_cylindrical_route

    # BEGIN CHECK exact_horizontal_route
    section_terms = [
        (Fraction(1, 2), 1),
        (Fraction(-1, 1), 2),
        (Fraction(1, 2), 3),
    ]
    coefficient_horizontal = integrate_monomials(section_terms, Fraction(0, 1), Fraction(1, 1))
    print("coefficient of pi, horizontal route           :", coefficient_horizontal)
    print("coefficient of pi, cylindrical route          :", coefficient_cylindrical)
    assert coefficient_horizontal == coefficient_cylindrical
    # END CHECK exact_horizontal_route

    integral_reference = float(coefficient_cylindrical) * math.pi
    print("triple integral, exact value pi / 24          :", integral_reference)

    # BEGIN CHECK integral_cartesian_quadrature
    integral_by_quadrature, quadrature_error = tplquad(
        integrand_for_quadrature,
        -1.0,
        1.0,
        lambda x_value: -math.sqrt(max(0.0, 1.0 - x_value * x_value)),
        lambda x_value: math.sqrt(max(0.0, 1.0 - x_value * x_value)),
        lambda x_value, y_value: 0.0,
        lambda x_value, y_value: 1.0 - x_value * x_value - y_value * y_value,
    )
    print("integral by tplquad in x, y, z                :", integral_by_quadrature)
    print("reported error of tplquad                     :", quadrature_error)
    assert abs(integral_by_quadrature - integral_reference) < 1.0e-7
    # END CHECK integral_cartesian_quadrature

    # BEGIN CHECK integral_polar_quadrature
    integral_by_polar, polar_error = dblquad(
        lambda r_value, theta_value: r_value * r_value * 0.5 * (1.0 - r_value * r_value) ** 2 * r_value,
        0.0,
        2.0 * math.pi,
        lambda theta_value: 0.0,
        lambda theta_value: 1.0,
    )
    print("integral by dblquad in theta, r               :", integral_by_polar)
    print("reported error of dblquad                     :", polar_error)
    assert abs(integral_by_polar - integral_by_quadrature) < 1.0e-9
    # END CHECK integral_polar_quadrature

    # BEGIN CHECK integral_rejection_sample
    generator = np.random.default_rng(RANDOM_SEED)
    sample = generator.uniform(-1.0, 1.0, size=(SAMPLE_COUNT, 2))
    height_sample = generator.uniform(0.0, 1.0, size=SAMPLE_COUNT)
    radius_squared = sample[:, 0] ** 2 + sample[:, 1] ** 2
    accepted = height_sample <= (1.0 - radius_squared)
    accepted_fraction = float(np.count_nonzero(accepted)) / SAMPLE_COUNT
    mean_value = float(np.mean(radius_squared[accepted] * height_sample[accepted]))
    box_volume = 4.0
    integral_by_sample = box_volume * accepted_fraction * mean_value
    value_spread = float(np.std(radius_squared[accepted] * height_sample[accepted]))
    standard_error = box_volume * math.sqrt(
        accepted_fraction * (value_spread**2 + mean_value**2 * (1.0 - accepted_fraction)) / SAMPLE_COUNT
    )
    print("integral by rejection sample                  :", integral_by_sample)
    print("standard error of the sample estimate         :", standard_error)
    print("integral by tplquad                           :", integral_by_quadrature)
    assert abs(integral_by_sample - integral_by_quadrature) < SAMPLE_SIGMA * standard_error
    assert standard_error < 2.0e-3
    # END CHECK integral_rejection_sample

    # BEGIN CHECK wrong_integrands
    missing_jacobian_terms = [
        (Fraction(1, 2), 2),
        (Fraction(-1, 1), 4),
        (Fraction(1, 2), 6),
    ]
    coefficient_without_radius = 2 * integrate_monomials(
        missing_jacobian_terms, Fraction(0, 1), Fraction(1, 1)
    )
    density_only_terms = [(Fraction(1, 2), 1), (Fraction(-1, 1), 3), (Fraction(1, 2), 5)]
    coefficient_density_only = 2 * integrate_monomials(density_only_terms, Fraction(0, 1), Fraction(1, 1))
    print("coefficient of pi when the factor r is dropped:", coefficient_without_radius)
    print("ratio of that wrong value to the correct value:", coefficient_without_radius / coefficient_cylindrical)
    print("coefficient of pi for the bare integral of z  :", coefficient_density_only)
    print("ratio of that wrong value to the correct value:", coefficient_density_only / coefficient_cylindrical)
    assert coefficient_without_radius == Fraction(8, 105)
    assert coefficient_without_radius / coefficient_cylindrical == Fraction(64, 35)
    assert coefficient_density_only == Fraction(1, 6)
    assert coefficient_density_only / coefficient_cylindrical == Fraction(4, 1)
    # END CHECK wrong_integrands

    print("part3_verify: all checks passed")


if __name__ == "__main__":
    main()
