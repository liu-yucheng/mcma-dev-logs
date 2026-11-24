"""Verify that the six orders of integration agree for Stewart 15.7 Exercise 31.

This script gathers the six limit sets, computes the integral for three polynomial functions in all
six orders, and compares each value with an exact value from a different method: an exact rational
integral over the parametrisation (x, s, t) of the solid.  It also compares all six orders for one
non-polynomial function, tests the six limit sets against the raw inequalities on a larger sample,
and counts the orders.

Run this script with the interpreter of ``code/.venv``.  It prints each checked value beside the
value that an independent method gives, and it writes the records to
``code/results/part6_results.json``.
"""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable

import numpy as np

from part3_verify import (
    accepts_dy_dz_dx,
    accepts_dz_dy_dx,
    integral_dy_dz_dx,
    integral_dz_dy_dx,
    minimum_inner_length as minimum_inner_length_x,
)
from part4_verify import (
    accepts_dx_dz_dy,
    accepts_dz_dx_dy,
    integral_dx_dz_dy,
    integral_dz_dx_dy,
    minimum_inner_length as minimum_inner_length_y,
)
from part5_verify import (
    accepts_dx_dy_dz,
    accepts_dy_dx_dz,
    integral_dx_dy_dz,
    integral_dy_dx_dz,
    minimum_inner_length as minimum_inner_length_z,
)

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

RESULTS_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the recorded checks."""

TOLERANCE = 1.0e-6
"""Absolute tolerance of the comparison of two numerical values."""

RANDOM_SEED = 20261122
"""Seed of the random sample of the limit test."""

Function = Callable[[float, float, float], float]
"""Type of an integrand of three variables."""

Monomial = tuple[int, int, int]
"""Exponents of (x, s, t) of one term of a polynomial."""

Polynomial = dict[Monomial, Fraction]
"""Sparse polynomial in the variables x, s, and t."""

EMPTY: Polynomial = {}
"""The zero polynomial."""


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Return the sum of two sparse polynomials.

    Args:
        left: The first polynomial.
        right: The second polynomial.

    Returns:
        The sum, with zero coefficients removed.
    """
    total = dict(left)
    for monomial, coefficient in right.items():
        total[monomial] = total.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in total.items() if coefficient != 0}


def polynomial_scale(polynomial: Polynomial, factor: Fraction) -> Polynomial:
    """Return one sparse polynomial multiplied by a constant.

    Args:
        polynomial: The polynomial.
        factor: The constant factor.

    Returns:
        The scaled polynomial, with zero coefficients removed.
    """
    scaled = {monomial: coefficient * factor for monomial, coefficient in polynomial.items()}
    return {monomial: coefficient for monomial, coefficient in scaled.items() if coefficient != 0}


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Return the product of two sparse polynomials.

    Args:
        left: The first polynomial.
        right: The second polynomial.

    Returns:
        The product.
    """
    product: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = (
                left_monomial[0] + right_monomial[0],
                left_monomial[1] + right_monomial[1],
                left_monomial[2] + right_monomial[2],
            )
            product[monomial] = product.get(monomial, Fraction(0)) + (
                left_coefficient * right_coefficient)
    return {monomial: coefficient for monomial, coefficient in product.items() if coefficient != 0}


def polynomial_power(base: Polynomial, exponent: int) -> Polynomial:
    """Return one sparse polynomial raised to a non-negative power.

    Args:
        base: The polynomial.
        exponent: The exponent.

    Returns:
        The power of the polynomial.
    """
    result: Polynomial = {(0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        result = polynomial_multiply(result, base)
    return result


def polynomial_integral(polynomial: Polynomial) -> Fraction:
    """Return the exact integral of one polynomial over the parameter box.

    The box is x in [-2, 2], s in [0, 1], and t in [0, 1].

    Args:
        polynomial: The polynomial in x, s, and t.

    Returns:
        The exact value of the integral.
    """
    total = Fraction(0)
    for (x_power, s_power, t_power), coefficient in polynomial.items():
        total += coefficient * (Fraction(2) ** (x_power + 1) - Fraction(-2) ** (x_power + 1)) / (
            x_power + 1) / (s_power + 1) / (t_power + 1)
    return total


def exact_numeric_totals() -> dict[str, Fraction]:
    """Return the exact value of the integral of three polynomial functions over E.

    The method is a change of variables to (x, s, t) with y = x^2 + s (4 - x^2) and
    z = t (4 - y) / 2.  The Jacobian is (4 - x^2) (4 - y) / 2.

    Returns:
        The exact value for the constant 1, for x^2 + y + z, and for 1 + x y z.
    """
    x_polynomial: Polynomial = {(1, 0, 0): Fraction(1)}
    y_polynomial: Polynomial = {(2, 0, 0): Fraction(1), (2, 1, 0): Fraction(-1),
                                (0, 1, 0): Fraction(4)}
    z_polynomial: Polynomial = {(0, 0, 1): Fraction(2), (2, 0, 1): Fraction(-1, 2),
                                (0, 1, 1): Fraction(-2), (2, 1, 1): Fraction(1, 2)}
    one: Polynomial = {(0, 0, 0): Fraction(1)}
    four: Polynomial = {(0, 0, 0): Fraction(4)}
    four_minus_x_squared = polynomial_add(
        four, polynomial_scale(polynomial_power(x_polynomial, 2), Fraction(-1)))
    four_minus_y = polynomial_add(four, polynomial_scale(y_polynomial, Fraction(-1)))
    jacobian = polynomial_scale(polynomial_multiply(four_minus_x_squared, four_minus_y),
                                Fraction(1, 2))
    return {
        "1": polynomial_integral(jacobian),
        "x^2+y+z": polynomial_integral(
            polynomial_multiply(
                polynomial_add(polynomial_add(polynomial_power(x_polynomial, 2), y_polynomial),
                               z_polynomial),
                jacobian)),
        "1+xyz": polynomial_integral(
            polynomial_multiply(
                polynomial_add(
                    one,
                    polynomial_multiply(
                        polynomial_multiply(polynomial_power(x_polynomial, 1), y_polynomial),
                        z_polynomial)),
                jacobian)),
    }


def function_one(x_value: float, y_value: float, z_value: float) -> float:
    """Return the constant integrand 1.

    Args:
        x_value: The coordinate x.
        y_value: The coordinate y.
        z_value: The coordinate z.

    Returns:
        The value 1.
    """
    return 1.0


def function_quadratic(x_value: float, y_value: float, z_value: float) -> float:
    """Return the integrand x^2 + y + z.

    Args:
        x_value: The coordinate x.
        y_value: The coordinate y.
        z_value: The coordinate z.

    Returns:
        The value of x^2 + y + z.
    """
    return x_value * x_value + y_value + z_value


def function_product(x_value: float, y_value: float, z_value: float) -> float:
    """Return the integrand 1 + x y z.

    Args:
        x_value: The coordinate x.
        y_value: The coordinate y.
        z_value: The coordinate z.

    Returns:
        The value of 1 + x y z.
    """
    return 1.0 + x_value * y_value * z_value


def function_non_polynomial(x_value: float, y_value: float, z_value: float) -> float:
    """Return the integrand exp(-x^2) (1 + z), which no polynomial method handles.

    Args:
        x_value: The coordinate x.
        y_value: The coordinate y.
        z_value: The coordinate z.

    Returns:
        The value of exp(-x^2) (1 + z).
    """
    return math.exp(-x_value * x_value) * (1.0 + z_value)


def inside_region(point: tuple[float, float, float]) -> bool:
    """Return True when one point satisfies the three raw defining inequalities.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when y >= x^2, z >= 0, and y + 2z <= 4.
    """
    x_value, y_value, z_value = point
    return bool(y_value >= x_value * x_value and z_value >= 0.0 and y_value + 2.0 * z_value <= 4.0)


def order_functions() -> dict[str, tuple[Function, Callable[[tuple[float, float, float]], bool]]]:
    """Return the integral function and the limit test of each of the six orders.

    Returns:
        A dictionary keyed by the order name, in the order of the exercise.
    """
    return {
        "dz dy dx": (integral_dz_dy_dx, accepts_dz_dy_dx),
        "dz dx dy": (integral_dz_dx_dy, accepts_dz_dx_dy),
        "dy dz dx": (integral_dy_dz_dx, accepts_dy_dz_dx),
        "dy dx dz": (integral_dy_dx_dz, accepts_dy_dx_dz),
        "dx dz dy": (integral_dx_dz_dy, accepts_dx_dz_dy),
        "dx dy dz": (integral_dx_dy_dz, accepts_dx_dy_dz),
    }


def main() -> None:
    """Run every check of Part 6, print the values, and write the result records."""
    exact_totals = exact_numeric_totals()
    orders = order_functions()

    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 20000
    samples = np.column_stack((
        generator.uniform(-2.5, 2.5, sample_count),
        generator.uniform(-0.5, 4.5, sample_count),
        generator.uniform(-0.5, 2.5, sample_count),
    ))
    reference = np.array([inside_region(tuple(map(float, row))) for row in samples])

    print("=== Part 6: the six orders and their agreement ===")
    print(f"exact value of f = 1        : {exact_totals['1']} = {float(exact_totals['1']):.12f}")
    print(f"exact value of f = x^2+y+z  : {exact_totals['x^2+y+z']} = "
          f"{float(exact_totals['x^2+y+z']):.12f}")
    print(f"exact value of f = 1+xyz    : {exact_totals['1+xyz']} = {float(exact_totals['1+xyz']):.12f}")
    print(f"closed forms                : 128/15 = {128.0 / 15.0:.12f}, "
          f"512/21 = {512.0 / 21.0:.12f}, 128/15 = {128.0 / 15.0:.12f}")
    print()

    disagreement_counts = {}
    for name, (_, limit_test) in orders.items():
        flags = np.array([limit_test(tuple(map(float, row))) for row in samples])
        disagreement_counts[name] = int(np.count_nonzero(flags != reference))
    print("limit sets against the raw inequalities on "
          f"{sample_count} random points")
    for name, count in disagreement_counts.items():
        print(f"  {name}  disagreements {count}, expected 0")
    print()

    comparison: dict[str, list[float]] = {}
    for name, (integral, _) in orders.items():
        comparison[name] = [integral(function) for function in
                            (function_one, function_quadratic, function_product)]

    largest_deviation = 0.0
    for index, key in enumerate(("1", "x^2+y+z", "1+xyz")):
        exact = float(exact_totals[key])
        print(f"f = {key}")
        for name, values in comparison.items():
            deviation = abs(values[index] - exact)
            largest_deviation = max(largest_deviation, deviation)
            print(f"  {name}  {values[index]:.12f}  exact {exact:.12f}  deviation {deviation:.3e}")
    print()

    non_polynomial = [integral(function_non_polynomial) for integral, _ in orders.values()]
    largest_spread = max(non_polynomial) - min(non_polynomial)
    print("f = exp(-x^2) (1 + z)")
    for name, value in zip(orders, non_polynomial):
        print(f"  {name}  {value:.12f}")
    print(f"largest difference between two orders: {largest_spread:.3e}")
    print()

    permutation_count = len(list(itertools.permutations(("x", "y", "z"))))
    print(f"orders of integration: {permutation_count}, 3! = {math.factorial(3)}")
    print(f"smallest inner lengths: x outermost {minimum_inner_length_x():.6e}, "
          f"y outermost {minimum_inner_length_y():.6e}, z outermost {minimum_inner_length_z():.6e}")

    records: list[dict[str, float | str]] = [
        {
            "label": "Exact value of $f = 1$ from the parametrisation against $128/15$",
            "computed": float(exact_totals["1"]),
            "expected": 128.0 / 15.0,
            "difference": abs(float(exact_totals["1"]) - 128.0 / 15.0),
            "tolerance": 1.0e-12,
        },
        {
            "label": "Exact value of $f = x^2+y+z$ from the parametrisation against $512/21$",
            "computed": float(exact_totals["x^2+y+z"]),
            "expected": 512.0 / 21.0,
            "difference": abs(float(exact_totals["x^2+y+z"]) - 512.0 / 21.0),
            "tolerance": 1.0e-12,
        },
        {
            "label": "Exact value of $f = 1+xyz$ from the parametrisation against $128/15$",
            "computed": float(exact_totals["1+xyz"]),
            "expected": 128.0 / 15.0,
            "difference": abs(float(exact_totals["1+xyz"]) - 128.0 / 15.0),
            "tolerance": 1.0e-12,
        },
        {
            "label": "Largest deviation of the eighteen order values from the exact values",
            "computed": largest_deviation,
            "expected": 0.0,
            "difference": largest_deviation,
            "tolerance": TOLERANCE,
        },
        {
            "label": "Largest difference between two orders for $f = e^{-x^2}(1+z)$",
            "computed": largest_spread,
            "expected": 0.0,
            "difference": largest_spread,
            "tolerance": TOLERANCE,
        },
        {
            "label": "Number of orders of integration against $3!$",
            "computed": float(permutation_count),
            "expected": float(math.factorial(3)),
            "difference": abs(float(permutation_count - math.factorial(3))),
            "tolerance": 0.0,
        },
    ]
    for name, count in disagreement_counts.items():
        pretty_name = name.replace(" ", chr(92) + ",")
        records.append({
            "label": f"Points that the limits of ${pretty_name}$ and $E$ classify differently",
            "computed": float(count),
            "expected": 0.0,
            "difference": float(count),
            "tolerance": 0.0,
        })

    for record in records:
        if record["difference"] > record["tolerance"]:
            raise AssertionError(f"check failed: {record['label']}")

    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = RESULTS_DIRECTORY / "part6_results.json"
    target.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {target}")


if __name__ == "__main__":
    main()
