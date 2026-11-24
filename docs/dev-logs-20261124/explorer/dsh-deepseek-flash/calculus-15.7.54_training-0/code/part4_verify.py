"""Verify the average value f_ave of f(x, y, z) = x^2 z + y^2 z over the region E.

The script forms the ratio of the triple integral to the volume by exact
rational arithmetic and then checks the same ratio with two numerical routes
that do not use the rational result. It also computes the largest value of f on
E, so that the tutorial can state a bound on the answer that is not the ratio
itself.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Sequence

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize

POLYNOMIAL_PAIRS = Sequence[tuple[Fraction, int]]
DECIMAL_PLACES = 7


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


def value_of_f(radius_squared: float, height: float) -> float:
    """Return f at a point whose distance from the axis has the given square."""
    return radius_squared * height


def main() -> None:
    """Run every check of Part 4 and print each computed value beside its reference."""
    # BEGIN CHECK exact_ratio
    numerator_terms = [(Fraction(1, 2), 3), (Fraction(-1, 1), 5), (Fraction(1, 2), 7)]
    numerator_coefficient = 2 * integrate_monomials(numerator_terms, Fraction(0, 1), Fraction(1, 1))
    denominator_terms = [(Fraction(1, 1), 1), (Fraction(-1, 1), 3)]
    denominator_coefficient = 2 * integrate_monomials(denominator_terms, Fraction(0, 1), Fraction(1, 1))
    ratio = numerator_coefficient / denominator_coefficient
    print("numerator, coefficient of pi                 :", numerator_coefficient)
    print("denominator, coefficient of pi               :", denominator_coefficient)
    print("ratio of the coefficients                    :", ratio)
    print("expected average value                       :", Fraction(1, 12))
    assert ratio == Fraction(1, 12)
    # END CHECK exact_ratio

    # BEGIN CHECK ratio_by_numeric_integrals
    numerator_numeric, numerator_error = quad(lambda z: 0.5 * math.pi * z * (1.0 - z) ** 2, 0.0, 1.0)
    denominator_numeric, denominator_error = quad(lambda z: math.pi * (1.0 - z), 0.0, 1.0)
    ratio_numeric = numerator_numeric / denominator_numeric
    ratio_exact = float(Fraction(1, 12))
    print("numerator by adaptive quadrature in z        :", numerator_numeric, "error", numerator_error)
    print("denominator by adaptive quadrature in z      :", denominator_numeric, "error", denominator_error)
    print("ratio by adaptive quadrature                 :", ratio_numeric)
    print("ratio from exact fractions                   :", ratio_exact)
    assert abs(ratio_numeric - ratio_exact) < 1.0e-10
    # END CHECK ratio_by_numeric_integrals

    # BEGIN CHECK largest_value_on_region
    def negative_value(parameters: np.ndarray) -> float:
        """Return minus f for a radius and a fraction of the free height.

        A point of E has the height z = (1 - r^2) u with u in [0, 1], so the
        search stays on E without a constraint term.
        """
        radius = parameters[0]
        fraction = parameters[1]
        return -value_of_f(radius * radius, (1.0 - radius * radius) * fraction)

    bounded_search = minimize(
        negative_value,
        x0=np.array([0.4, 0.8]),
        method="L-BFGS-B",
        bounds=((0.0, 1.0), (0.0, 1.0)),
    )
    largest_by_search = float(-bounded_search.fun)
    radius_best = float(bounded_search.x[0])
    radius_squared_best = radius_best * radius_best
    height_best = (1.0 - radius_squared_best) * float(bounded_search.x[1])
    largest_by_hand = 0.25
    print("largest value of f on E by search            :", largest_by_search)
    print("point of the largest value, r squared and z  :", radius_squared_best, height_best)
    print("largest value of f on E by hand, 1 / 4       :", largest_by_hand)
    print("f at r squared 1/2 and z 1/2                 :", value_of_f(0.5, 0.5))
    assert abs(largest_by_search - largest_by_hand) < 1.0e-6
    assert abs(radius_squared_best - 0.5) < 1.0e-5
    assert abs(height_best - 0.5) < 1.0e-5
    # END CHECK largest_value_on_region

    # BEGIN CHECK ratio_inside_bounds
    average_value = ratio_exact
    largest_value = largest_by_hand
    print("average value                                :", average_value)
    print("lower bound 0 and upper bound 1 / 4          :", 0.0, largest_value)
    print("ratio of the average value to the largest    :", average_value / largest_value)
    assert 0.0 < average_value < largest_value
    assert average_value == largest_value / 3.0
    # END CHECK ratio_inside_bounds

    # BEGIN CHECK two_wrong_answers
    integral_alone = float(numerator_coefficient) * math.pi
    divided_by_base_area = integral_alone / math.pi
    correct_value = float(Fraction(1, 12))
    print("value when the division by V(E) is dropped   :", integral_alone)
    print("value when the base area pi replaces V(E)     :", divided_by_base_area)
    print("correct average value                         :", correct_value)
    assert abs(integral_alone - correct_value) > 1.0e-2
    assert abs(divided_by_base_area - correct_value) > 1.0e-2
    # END CHECK two_wrong_answers

    # BEGIN CHECK decimal_form
    decimal_by_format = f"{correct_value:.{DECIMAL_PLACES}f}"
    decimal_by_rounding = float(round(correct_value, DECIMAL_PLACES))
    print("decimal form with", DECIMAL_PLACES, "places        :", decimal_by_format)
    print("decimal form by rounding                     :", decimal_by_rounding)
    print("exact one twelfth                            :", correct_value)
    assert decimal_by_format == "0.0833333"
    assert abs(decimal_by_rounding - correct_value) < 5.0e-8
    # END CHECK decimal_form

    print("part4_verify: all checks passed")


if __name__ == "__main__":
    main()
