"""Verify the evaluation of Part 3 in the order dz dx dy.

Method one is the iterated integral with the antiderivatives written out.
Method two is adaptive quadrature of the same order.
Method three is exact rational arithmetic on the antiderivative.
The script also computes the value of one common mistake, so that the tutorial can print it.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy import integrate

from check_registry import CheckRegistry, latex_fraction, write_values
from geometry_anchors import CYLINDER_RADIUS, PLANE_SLOPE, SAMPLE_HEIGHTS_Y
from limit_expression import ConstantLimit, LinearShare, SqrtRemainder

OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "outputs"
"""Directory that holds the JSON record of every part."""

DERIVATIVE_POINT_COUNT = 401
"""Number of points at which the derivative test compares the antiderivative with the integrand."""

DERIVATIVE_STEP = 1.0e-5
"""Step of the central difference of the derivative test."""

DERIVATIVE_TOLERANCE = 1.0e-6
"""Largest relative gap between the central difference and the closed form of the integrand."""

QUADRATURE_OPTIONS = {"epsabs": 1.0e-12, "epsrel": 1.0e-12, "limit": 400}
"""Options of every adaptive quadrature of the part."""


def inner_integral_closed_form(y: np.ndarray) -> np.ndarray:
    """Return the value of the integral over z at fixed y.

    Args:
        y: Array of the value of y.
    """
    return (CYLINDER_RADIUS**2 - np.asarray(y, dtype=float) ** 2) / 2.0


def middle_integral_closed_form(y: np.ndarray) -> np.ndarray:
    """Return the value of the integral over z and then over x at fixed y.

    Args:
        y: Array of the value of y.
    """
    return np.asarray(y, dtype=float) / PLANE_SLOPE * inner_integral_closed_form(y)


def outer_integrand(y: np.ndarray) -> np.ndarray:
    """Return the integrand of the outer integral over y.

    Args:
        y: Array of the value of y.
    """
    return (CYLINDER_RADIUS**2 * np.asarray(y, dtype=float) - np.asarray(y, dtype=float) ** 3) / (
        2.0 * PLANE_SLOPE
    )


def outer_antiderivative(y: Fraction) -> Fraction:
    """Return the exact antiderivative of the outer integrand at one rational point.

    Args:
        y: Rational value at which the antiderivative is evaluated.
    """
    return Fraction(int(CYLINDER_RADIUS**2), 4 * int(PLANE_SLOPE)) * y**2 - Fraction(
        1, 8 * int(PLANE_SLOPE)
    ) * y**4


def outer_antiderivative_value(y: np.ndarray) -> np.ndarray:
    """Return the antiderivative of the outer integrand at floating point values.

    Args:
        y: Array of the value of y.
    """
    values = np.asarray(y, dtype=float)
    return values**2 * 3.0 / 4.0 - values**4 / 24.0


def inner_integral_by_quad(y_value: float) -> float:
    """Return the integral over z at one value of y by adaptive quadrature.

    Args:
        y_value: Value of y at which the section is integrated.
    """
    upper = math.sqrt(CYLINDER_RADIUS**2 - y_value**2)
    return float(integrate.quad(lambda z: z, 0.0, upper, **QUADRATURE_OPTIONS)[0])


def middle_integral_by_quad(y_value: float) -> float:
    """Return the integral over x of the section area at one value of y by adaptive quadrature.

    Args:
        y_value: Value of y at which the section is integrated.
    """
    return float(integrate.quad(lambda x: inner_integral_by_quad(y_value), 0.0, y_value / PLANE_SLOPE, **QUADRATURE_OPTIONS)[0])


def triple_integral_by_quad() -> float:
    """Return the triple integral of z over the solid by nested adaptive quadrature."""
    inner_lower, inner_upper = ConstantLimit(0.0), SqrtRemainder(CYLINDER_RADIUS**2, "y")
    middle_lower, middle_upper = ConstantLimit(0.0), LinearShare("y", PLANE_SLOPE)

    def inner_value(y_value: float) -> float:
        """Return the integral over z at one value of y."""
        named = {"x": np.asarray(0.0), "y": np.asarray(y_value), "z": np.asarray(0.0)}
        upper = float(np.asarray(inner_upper.evaluate(named)))
        return float(integrate.quad(lambda z: z, float(np.asarray(inner_lower.evaluate(named))), upper, **QUADRATURE_OPTIONS)[0])

    def middle_value(y_value: float) -> float:
        """Return the integral over x of the inner integral at one value of y."""
        named = {"x": np.asarray(0.0), "y": np.asarray(y_value), "z": np.asarray(0.0)}
        upper = float(np.asarray(middle_upper.evaluate(named)))
        return float(integrate.quad(lambda x: inner_value(y_value), float(np.asarray(middle_lower.evaluate(named))), upper, **QUADRATURE_OPTIONS)[0])

    return float(integrate.quad(middle_value, 0.0, CYLINDER_RADIUS, **QUADRATURE_OPTIONS)[0])


def wrong_value_of_full_width_x() -> Fraction:
    """Return the exact value of the integral that takes x up to one at every height y.

    The integral is the one of a reader who drops the plane y = 3x and keeps the full width x = 1.
    """
    wrong_inner = Fraction(int(CYLINDER_RADIUS**2), 2)
    return wrong_inner * Fraction(int(CYLINDER_RADIUS)) - Fraction(
        int(CYLINDER_RADIUS**3), 3 * 2
    )


def main() -> None:
    """Run every check of Part 3 and write the values of the part."""
    registry = CheckRegistry("part3")
    values: dict[str, object] = {}

    heights = np.asarray(SAMPLE_HEIGHTS_Y, dtype=float)
    for height in heights:
        registry.compare(
            f"part3.inner_at_y_{height:.1f}",
            inner_integral_by_quad(float(height)),
            float(inner_integral_closed_form(np.asarray(height))),
            1.0e-11,
            "Quadrature of the z-section against the closed form of the inner integral.",
        )
        registry.compare(
            f"part3.middle_at_y_{height:.1f}",
            middle_integral_by_quad(float(height)),
            float(middle_integral_closed_form(np.asarray(height))),
            1.0e-9,
            "Quadrature of the x-section against the closed form of the middle integral.",
        )

    derivative_points = np.linspace(0.2, 2.9, DERIVATIVE_POINT_COUNT)
    central_difference = (
        outer_antiderivative_value(derivative_points + DERIVATIVE_STEP)
        - outer_antiderivative_value(derivative_points - DERIVATIVE_STEP)
    ) / (2.0 * DERIVATIVE_STEP)
    closed_form = outer_integrand(derivative_points)
    largest_relative_gap = float(np.max(np.abs(central_difference - closed_form) / np.abs(closed_form)))
    registry.compare_absolute(
        "part3.antiderivative_derivative",
        largest_relative_gap,
        0.0,
        DERIVATIVE_TOLERANCE,
        "Largest relative gap between the central difference of the antiderivative and the integrand.",
    )

    exact_value = outer_antiderivative(Fraction(int(CYLINDER_RADIUS))) - outer_antiderivative(Fraction(0))
    registry.compare_absolute(
        "part3.exact_value_denominator",
        float(exact_value.denominator),
        8.0,
        0.0,
        "Denominator of the exact value against the denominator that the arithmetic produces.",
    )
    quadrature_value = float(integrate.quad(lambda y: float(outer_integrand(np.asarray(y))), 0.0, CYLINDER_RADIUS, **QUADRATURE_OPTIONS)[0])
    registry.compare(
        "part3.outer_quad_against_exact",
        quadrature_value,
        float(exact_value),
        1.0e-12,
        "Adaptive quadrature of the outer integral against the exact rational arithmetic.",
    )
    nested_value = triple_integral_by_quad()
    registry.compare(
        "part3.nested_quad_against_exact",
        nested_value,
        float(exact_value),
        1.0e-11,
        "Nested quadrature of the triple integral in the chosen order against the exact value.",
    )

    volume = CYLINDER_RADIUS**3 / (3.0 * PLANE_SLOPE)
    mean_height = float(exact_value) / volume
    registry.compare(
        "part3.mean_height",
        mean_height,
        9.0 / 8.0,
        1.0e-12,
        "Quotient of the integral by the volume against the exact mean height.",
    )

    wrong_value = wrong_value_of_full_width_x()
    wrong_by_quad = float(
        integrate.quad(
            lambda y: (CYLINDER_RADIUS**2 - y**2) / 2.0, 0.0, CYLINDER_RADIUS, **QUADRATURE_OPTIONS
        )[0]
    )
    registry.compare(
        "part3.common_mistake_mass",
        wrong_by_quad,
        float(wrong_value),
        1.0e-12,
        "Quadrature of the integral with the full width in x against its exact rational value.",
    )
    ratio = float(wrong_value) / float(exact_value)
    print(f"wrong value with the full width in x: {float(wrong_value):.9f}, ratio to the answer {ratio:.6f}")

    registry.write(OUTPUT_DIRECTORY / "part3_checks.json")
    values.update(
        {
            "p3_answer_decimal": f"{float(exact_value):.9f}",
            "p3_answer_latex": latex_fraction(int(exact_value.numerator), int(exact_value.denominator)),
            "p3_inner_latex": "\\dfrac{9 - y^{2}}{2}",
            "p3_middle_latex": "\\dfrac{y\\,(9 - y^{2})}{6}",
            "p3_antiderivative_latex": "\\dfrac{3y^{2}}{4} - \\dfrac{y^{4}}{24}",
            "p3_mean_height_decimal": f"{mean_height:.9f}",
            "p3_mean_height_latex": latex_fraction(9, 8),
            "p3_outer_integrand_latex": "\\dfrac{9y - y^{3}}{6}",
            "p3_wrong_value_decimal": f"{float(wrong_value):.9f}",
            "p3_wrong_ratio_decimal": f"{ratio:.6f}",
            "p3_derivative_gap": f"{largest_relative_gap:.3e}",
            "p3_check_count": str(registry.passed_count()),
        }
    )
    write_values(OUTPUT_DIRECTORY / "part3_values.json", values)


if __name__ == "__main__":
    main()
