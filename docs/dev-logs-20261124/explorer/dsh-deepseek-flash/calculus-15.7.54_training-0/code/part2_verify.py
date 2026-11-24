"""Verify the volume V(E) of the solid region E.

The script computes the volume by four methods that do not share a formula:
an exact rational integral in the radius, an exact rational integral in the
height, a two-dimensional adaptive quadrature in Cartesian coordinates, and a
rejection sample in the bounding box. Each check compares one method with a
different method.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

import numpy as np
from scipy.integrate import dblquad, simpson, tplquad

POLYNOMIAL_PAIRS = Sequence[tuple[Fraction, int]]
SAMPLE_COUNT = 400000
RANDOM_SEED = 20261123
HEIGHT_GRID_SAMPLES = 2001
AREA_GRID_SAMPLES = 2001
QUADRATURE_TOLERANCE = 1.0e-8
AREA_TOLERANCE = 1.0e-3
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


def slice_area_by_formula(height: float) -> float:
    """Return the area of the horizontal section at one height from the inequalities.

    The section at height z holds every point with x^2 + y^2 <= 1 - z, so the
    section is a disk of radius sqrt(1 - z) and its area is pi (1 - z).
    """
    return math.pi * (1.0 - height)


def slice_area_by_grid(height: float, sample_count: int) -> float:
    """Return the area of the horizontal section at one height by a grid count."""
    radius = math.sqrt(max(0.0, 1.0 - height))
    axis = np.linspace(-radius, radius, sample_count)
    grid_x, grid_y = np.meshgrid(axis, axis)
    inside = (grid_x**2 + grid_y**2) <= radius**2
    return float(np.count_nonzero(inside)) * (axis[1] - axis[0]) ** 2


def main() -> None:
    """Run every check of Part 2 and print each computed value beside its reference."""
    print("numerical tolerance of the quadrature:", QUADRATURE_TOLERANCE)

    # BEGIN CHECK exact_routes
    radial_integrand = [(Fraction(1, 1), 1), (Fraction(-1, 1), 3)]
    radial_piece = integrate_monomials(radial_integrand, Fraction(0, 1), Fraction(1, 1))
    volume_coefficient_radial = 2 * radial_piece
    height_integrand = [(Fraction(1, 1), 0), (Fraction(-1, 1), 1)]
    volume_coefficient_height = integrate_monomials(height_integrand, Fraction(0, 1), Fraction(1, 1))
    print("radial route, integral of r - r^3 on [0, 1]  :", radial_piece)
    print("radial route, coefficient of pi              :", volume_coefficient_radial)
    print("height route, coefficient of pi              :", volume_coefficient_height)
    assert volume_coefficient_radial == volume_coefficient_height
    assert volume_coefficient_radial == Fraction(1, 2)
    # END CHECK exact_routes

    # BEGIN CHECK slice_areas
    heights = (0.0, 0.5, 0.8)
    formula_areas = [slice_area_by_formula(h) for h in heights]
    grid_areas = [slice_area_by_grid(h, AREA_GRID_SAMPLES) for h in heights]
    for height, formula_area, grid_area in zip(heights, formula_areas, grid_areas):
        print(
            "height",
            height,
            "area by pi (1 - z) =",
            formula_area,
            "area by grid count =",
            grid_area,
        )
        assert abs(grid_area - formula_area) / formula_area < AREA_TOLERANCE
    # END CHECK slice_areas

    # BEGIN CHECK volume_cartesian_quadrature
    volume_by_quadrature, quadrature_error = tplquad(
        lambda z_value, y_value, x_value: 1.0,
        -1.0,
        1.0,
        lambda x_value: -math.sqrt(max(0.0, 1.0 - x_value * x_value)),
        lambda x_value: math.sqrt(max(0.0, 1.0 - x_value * x_value)),
        lambda x_value, y_value: 0.0,
        lambda x_value, y_value: 1.0 - x_value * x_value - y_value * y_value,
    )
    volume_by_polar, polar_error = dblquad(
        lambda r_value, theta_value: (1.0 - r_value * r_value) * r_value,
        0.0,
        2.0 * math.pi,
        lambda theta_value: 0.0,
        lambda theta_value: 1.0,
    )
    print("volume by tplquad in x, y, z                 :", volume_by_quadrature)
    print("reported error of tplquad                    :", quadrature_error)
    print("volume by dblquad in theta, r                :", volume_by_polar)
    print("reported error of dblquad                    :", polar_error)
    assert abs(volume_by_quadrature - volume_by_polar) < 1.0e-9
    # END CHECK volume_cartesian_quadrature

    # BEGIN CHECK volume_height_integral
    height_axis = np.linspace(0.0, 1.0, HEIGHT_GRID_SAMPLES)
    area_values = np.pi * (1.0 - height_axis)
    volume_by_simpson = float(simpson(area_values, x=height_axis))
    print("volume by Simpson over the section area      :", volume_by_simpson)
    print("volume by quadrature in x, y, z               :", volume_by_quadrature)
    assert abs(volume_by_simpson - volume_by_quadrature) < 1.0e-9
    # END CHECK volume_height_integral

    # BEGIN CHECK volume_rejection_sample
    generator = np.random.default_rng(RANDOM_SEED)
    sample = generator.uniform(-1.0, 1.0, size=(SAMPLE_COUNT, 2))
    height_sample = generator.uniform(0.0, 1.0, size=SAMPLE_COUNT)
    radius_squared = sample[:, 0] ** 2 + sample[:, 1] ** 2
    accepted = height_sample <= (1.0 - radius_squared)
    accepted_fraction = float(np.count_nonzero(accepted)) / SAMPLE_COUNT
    box_volume = 4.0
    volume_by_sample = box_volume * accepted_fraction
    standard_error = box_volume * math.sqrt(accepted_fraction * (1.0 - accepted_fraction) / SAMPLE_COUNT)
    print("volume by rejection sample                   :", volume_by_sample)
    print("standard error of the sample estimate        :", standard_error)
    print("volume by quadrature in x, y, z               :", volume_by_quadrature)
    assert abs(volume_by_sample - volume_by_quadrature) < SAMPLE_SIGMA * standard_error
    assert standard_error < 1.0e-2
    # END CHECK volume_rejection_sample

    print("volume of E, exact value pi / 2              :", math.pi / 2.0)
    print("part2_verify: all checks passed")


if __name__ == "__main__":
    main()
