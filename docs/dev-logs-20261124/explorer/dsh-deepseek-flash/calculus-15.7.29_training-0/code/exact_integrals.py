"""Exact values, as a rational multiple of pi, of the integral of a monomial over the solid.

The solid E is bounded by y = 4 - x**2 - 4*z**2 and y = 0. The script uses the
substitution x = 2*u, z = w, which maps the projection onto the unit disk. Under this
substitution the height is 4*(1 - u**2 - w**2), and every integral of a monomial becomes a
polynomial integral over the unit disk. This module integrates such polynomials with exact
rational arithmetic, so a value that it returns shares no code with a quadrature routine.
"""

from __future__ import annotations

import math
from fractions import Fraction

# Coefficient 4 of z**2 in the upper surface. The substitution z = w keeps this factor.
Z_SQUARED_COEFFICIENT = 4

# Semi-axis of the base ellipse along x. The substitution x = 2*u divides by this factor.
BASE_SEMI_AXIS_X = 2


def multiply_polynomials(
    first: dict[int, Fraction], second: dict[int, Fraction]
) -> dict[int, Fraction]:
    """Return the product of two polynomials that a dictionary keys by the power.

    Args:
        first: Polynomial with keys equal to the powers and values equal to the coefficients.
        second: The second polynomial in the same form.

    Returns:
        The product polynomial in the same form, without a term of coefficient zero.
    """
    product: dict[int, Fraction] = {}
    for first_power, first_coefficient in first.items():
        for second_power, second_coefficient in second.items():
            power = first_power + second_power
            coefficient = product.get(power, Fraction(0)) + first_coefficient * second_coefficient
            product[power] = coefficient
    return {power: coefficient for power, coefficient in product.items() if coefficient != 0}


def power_of_polynomial(base: dict[int, Fraction], exponent: int) -> dict[int, Fraction]:
    """Return a polynomial raised to a non-negative integer power.

    Args:
        base: Polynomial with keys equal to the powers and values equal to the coefficients.
        exponent: Non-negative integer power.

    Returns:
        The power polynomial. The power zero gives the constant polynomial 1.
    """
    result: dict[int, Fraction] = {0: Fraction(1)}
    for _ in range(exponent):
        result = multiply_polynomials(result, base)
    return result


def moment_of_unit_disk(first_exponent: int, second_exponent: int) -> Fraction:
    """Return the factor c with the moment of u**p * w**q over the unit disk equal to c*pi.

    The moment is the Beta integral
    2*B(i + 1/2, j + 1/2)/(2*i + 2*j + 2) with i = p//2 and j = q//2, and it is zero when
    p or q is odd, because the unit disk is symmetric about both axes.

    Args:
        first_exponent: Exponent p of the coordinate u.
        second_exponent: Exponent q of the coordinate w.

    Returns:
        The rational factor c of pi.
    """
    if first_exponent % 2 == 1 or second_exponent % 2 == 1:
        return Fraction(0)
    first_half = first_exponent // 2
    second_half = second_exponent // 2
    numerator = Fraction(
        math.factorial(2 * first_half) * math.factorial(2 * second_half)
    )
    denominator = Fraction(
        4 ** (first_half + second_half)
        * math.factorial(first_half)
        * math.factorial(second_half)
        * math.factorial(first_half + second_half)
        * (first_half + second_half + 1)
    )
    return numerator / denominator


def exact_multiple_of_pi(x_power: int, y_power: int, z_power: int) -> Fraction:
    """Return the factor c of pi, with the integral of x**a * y**b * z**c over E equal to c*pi.

    The inner integral in y gives h**(b + 1)/(b + 1), with h = 4*(1 - r**2). The
    substitution x = 2*u and z = w turns the outer integral into a polynomial integral over
    the unit disk, and each term of that polynomial is a sum of moments of the unit disk.

    Args:
        x_power: Exponent a of the coordinate x.
        y_power: Exponent b of the coordinate y.
        z_power: Exponent c of the coordinate z.

    Returns:
        The rational factor c of pi.
    """
    scale = Fraction(
        BASE_SEMI_AXIS_X ** (x_power + 1) * Z_SQUARED_COEFFICIENT ** (y_power + 1),
        y_power + 1,
    )
    radial_expansion = power_of_polynomial({0: Fraction(1), 1: Fraction(-1)}, y_power + 1)
    total = Fraction(0)
    for radial_power, radial_coefficient in radial_expansion.items():
        for split in range(radial_power + 1):
            binomial_weight = Fraction(math.comb(radial_power, split))
            first_exponent = x_power + 2 * split
            second_exponent = z_power + 2 * (radial_power - split)
            total += (
                radial_coefficient
                * binomial_weight
                * moment_of_unit_disk(first_exponent, second_exponent)
            )
    return scale * total


def exact_value(x_power: int, y_power: int, z_power: int) -> float:
    """Return the integral of x**a * y**b * z**c over E as a float.

    Args:
        x_power: Exponent a of the coordinate x.
        y_power: Exponent b of the coordinate y.
        z_power: Exponent c of the coordinate z.

    Returns:
        The value c*pi as a float, with c from exact_multiple_of_pi.
    """
    return float(exact_multiple_of_pi(x_power, y_power, z_power)) * math.pi
