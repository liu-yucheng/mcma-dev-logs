"""Verify the answer of Part 3 with a second order and with a different parametrisation.

Method one is the order dx dy dz with the antiderivatives written out.
Method two is adaptive quadrature in cylindrical coordinates of the (y, z) plane, which never uses
the three nested limits of Part 2.
Method three is a Monte Carlo average of z over a box that contains the solid.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import integrate

from check_registry import CheckRegistry, latex_fraction, write_values
from geometry_anchors import CYLINDER_RADIUS, MONTE_CARLO_SAMPLE_COUNT, PLANE_SLOPE, RANDOM_SEED

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

QUADRATURE_OPTIONS = {"epsabs": 1.0e-12, "epsrel": 1.0e-12, "limit": 400}
"""Options of every adaptive quadrature of the part."""

DERIVATIVE_POINT_COUNT = 121
"""Number of points at which the derivative test of the second order runs."""

DERIVATIVE_STEP = 1.0e-5
"""Step of the central difference of the derivative test."""

DERIVATIVE_TOLERANCE = 1.0e-6
"""Largest relative gap that the derivative test accepts."""

PARAMETER_SAMPLE_COUNT = 200_000
"""Number of parameter triples of the change of variables check."""


def second_order_antiderivative(z_value: Fraction) -> Fraction:
    """Return the exact antiderivative of the outer integrand of the order dx dy dz.

    Args:
        z_value: Rational value at which the antiderivative is evaluated.
    """
    return Fraction(int(CYLINDER_RADIUS**2), 4 * int(PLANE_SLOPE)) * z_value**2 - Fraction(
        1, 8 * int(PLANE_SLOPE)
    ) * z_value**4


def second_order_antiderivative_value(z_value: np.ndarray) -> np.ndarray:
    """Return the antiderivative of the order dx dy dz at floating point values.

    Args:
        z_value: Array of the value of z.
    """
    values = np.asarray(z_value, dtype=float)
    return 3.0 * values**2 / 4.0 - values**4 / 24.0


def second_order_integrand(z_value: np.ndarray) -> np.ndarray:
    """Return the outer integrand of the order dx dy dz.

    Args:
        z_value: Array of the value of z.
    """
    values = np.asarray(z_value, dtype=float)
    return (CYLINDER_RADIUS**2 * values - values**3) / (2.0 * PLANE_SLOPE)


def second_order_by_quad() -> float:
    """Return the value of the integral in the order dx dy dz by nested adaptive quadrature."""
    def middle_value(z_value: float) -> float:
        """Return the integral over x and then over y at one value of z."""
        upper_y = math.sqrt(CYLINDER_RADIUS**2 - z_value**2)
        return float(
            integrate.quad(
                lambda y: integrate.quad(lambda x: z_value, 0.0, y / PLANE_SLOPE, **QUADRATURE_OPTIONS)[0],
                0.0,
                upper_y,
                **QUADRATURE_OPTIONS,
            )[0]
        )

    return float(integrate.quad(middle_value, 0.0, CYLINDER_RADIUS, **QUADRATURE_OPTIONS)[0])


def polar_quadrature() -> float:
    """Return the value of the integral by adaptive quadrature in the cylindrical parameters.

    The parameters are the radius and the angle of the (y, z) plane, and the coordinate x.
    """
    def radius_value(radius: float, angle: float) -> float:
        """Return the integral over x of the height at one radius and one angle."""
        height = radius * math.sin(angle)
        width = radius * math.cos(angle) / PLANE_SLOPE
        return height * width * radius

    value, _ = integrate.dblquad(
        radius_value, 0.0, math.pi / 2.0, 0.0, CYLINDER_RADIUS, epsabs=1.0e-11, epsrel=1.0e-11
    )
    return float(value)


def polar_volume() -> float:
    """Return the volume of the solid by the same cylindrical parameters, for the Jacobian check."""
    def radius_value(radius: float, angle: float) -> float:
        """Return the length of the x segment at one radius and one angle."""
        return radius * math.cos(angle) / PLANE_SLOPE * radius

    value, _ = integrate.dblquad(
        radius_value, 0.0, math.pi / 2.0, 0.0, CYLINDER_RADIUS, epsabs=1.0e-11, epsrel=1.0e-11
    )
    return float(value)


def monte_carlo_height_integral() -> tuple[float, float]:
    """Return the Monte Carlo value of the integral and its standard error."""
    generator = np.random.default_rng(RANDOM_SEED + 1)
    x_values = generator.uniform(0.0, 1.0, MONTE_CARLO_SAMPLE_COUNT)
    y_values = generator.uniform(0.0, CYLINDER_RADIUS, MONTE_CARLO_SAMPLE_COUNT)
    z_values = generator.uniform(0.0, CYLINDER_RADIUS, MONTE_CARLO_SAMPLE_COUNT)
    inside = (
        (y_values * y_values + z_values * z_values <= CYLINDER_RADIUS**2)
        & (y_values >= PLANE_SLOPE * x_values)
    )
    box_volume = 1.0 * CYLINDER_RADIUS * CYLINDER_RADIUS
    samples = np.where(inside, z_values, 0.0) * box_volume
    return float(samples.mean()), float(samples.std(ddof=1) / math.sqrt(samples.size))


def main() -> None:
    """Run every check of Part 4 and write the values of the part."""
    registry = CheckRegistry("part4")
    values: dict[str, object] = {}

    derivative_points = np.linspace(0.2, 2.9, DERIVATIVE_POINT_COUNT)
    central_difference = (
        second_order_antiderivative_value(derivative_points + DERIVATIVE_STEP)
        - second_order_antiderivative_value(derivative_points - DERIVATIVE_STEP)
    ) / (2.0 * DERIVATIVE_STEP)
    closed_form = second_order_integrand(derivative_points)
    largest_gap = float(np.max(np.abs(central_difference - closed_form) / np.abs(closed_form)))
    registry.compare_absolute(
        "part4.second_order_derivative",
        largest_gap,
        0.0,
        DERIVATIVE_TOLERANCE,
        "Largest relative gap between the central difference of the second antiderivative and its integrand.",
    )

    exact_second = second_order_antiderivative(Fraction(int(CYLINDER_RADIUS))) - second_order_antiderivative(
        Fraction(0)
    )
    part3_record = json.loads((OUTPUT_DIRECTORY / "part3_values.json").read_text(encoding="utf-8"))
    reference_value = float(part3_record["p3_answer_decimal"])
    registry.compare(
        "part4.order_values_agree",
        float(exact_second),
        reference_value,
        1.0e-12,
        "Exact value of the order dx dy dz against the value that Part 3 computes in the order dz dx dy.",
    )
    print(f"second order exact value {exact_second} as a fraction, {float(exact_second):.12f} as a decimal")

    quad_second = second_order_by_quad()
    registry.compare(
        "part4.second_order_quad",
        quad_second,
        float(exact_second),
        1.0e-11,
        "Nested quadrature of the second order against the exact rational value of that order.",
    )

    polar_value = polar_quadrature()
    registry.compare(
        "part4.polar_quadrature",
        polar_value,
        reference_value,
        1.0e-10,
        "Cylindrical quadrature that never uses the nested limits against the exact value.",
    )
    volume_by_polar = polar_volume()
    registry.compare(
        "part4.polar_volume",
        volume_by_polar,
        CYLINDER_RADIUS**3 / (3.0 * PLANE_SLOPE),
        1.0e-10,
        "Volume by the cylindrical Jacobian against the volume of Part 1.",
    )

    generator = np.random.default_rng(RANDOM_SEED + 2)
    radius_values = generator.uniform(0.0, CYLINDER_RADIUS, PARAMETER_SAMPLE_COUNT)
    angle_values = generator.uniform(0.0, math.pi / 2.0, PARAMETER_SAMPLE_COUNT)
    x_share = generator.uniform(0.0, 1.0, PARAMETER_SAMPLE_COUNT)
    mapped_y = radius_values * np.cos(angle_values)
    mapped_z = radius_values * np.sin(angle_values)
    mapped_x = x_share * radius_values * np.cos(angle_values) / PLANE_SLOPE
    outside = int(
        np.count_nonzero(
            (mapped_y * mapped_y + mapped_z * mapped_z > CYLINDER_RADIUS**2 * (1.0 + 1.0e-12))
            | (mapped_y < PLANE_SLOPE * mapped_x - 1.0e-12)
        )
    )
    registry.compare_absolute(
        "part4.parameter_map_inside",
        float(outside),
        0.0,
        0.0,
        "Number of sampled parameter triples that leave the solid against zero.",
    )

    monte_carlo_value, monte_carlo_error = monte_carlo_height_integral()
    gap = abs(monte_carlo_value - reference_value)
    standard_errors = gap / monte_carlo_error
    print(
        f"monte carlo value {monte_carlo_value:.9f} error {monte_carlo_error:.9f} "
        f"gap {gap:.9f} gap in standard errors {standard_errors:.4f}"
    )
    registry.compare_absolute(
        "part4.monte_carlo_inside_five_errors",
        standard_errors,
        0.0,
        5.0,
        "Gap of the Monte Carlo average and the exact value in standard errors against five errors.",
    )

    registry.write(OUTPUT_DIRECTORY / "part4_checks.json")
    values.update(
        {
            "p4_second_order_latex": "dx\\,dy\\,dz",
            "p4_second_order_outer_latex": "\\dfrac{9z - z^{3}}{6}",
            "p4_second_order_answer_latex": latex_fraction(
                int(exact_second.numerator), int(exact_second.denominator)
            ),
            "p4_second_order_decimal": f"{float(exact_second):.9f}",
            "p4_polar_decimal": f"{polar_value:.9f}",
            "p4_polar_volume_decimal": f"{volume_by_polar:.9f}",
            "p4_monte_carlo_decimal": f"{monte_carlo_value:.9f}",
            "p4_monte_carlo_error": f"{monte_carlo_error:.9f}",
            "p4_monte_carlo_standard_errors": f"{standard_errors:.4f}",
            "p4_derivative_gap": f"{largest_gap:.3e}",
            "p4_parameter_sample_count": str(PARAMETER_SAMPLE_COUNT),
            "p4_check_count": str(registry.passed_count()),
        }
    )
    write_values(OUTPUT_DIRECTORY / "part4_values.json", values)


if __name__ == "__main__":
    main()
