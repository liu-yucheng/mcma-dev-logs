"""Verify the two orders of integration with y outermost for Stewart 15.7 Exercise 31.

The section at a fixed y is the rectangle of Part 2.  This script computes the same integral in the
two orders that start with y: dz dx dy and dx dz dy.  Each order is one single integral with
variable limits and no split.  The script compares the two orders with each other, compares both
with the exact volume 128/15, and tests each printed limit set against the raw defining
inequalities on random points.

Run this script with the interpreter of ``code/.venv``.  It prints each checked value beside the
value that an independent method gives, and it writes the records to
``code/results/part4_results.json``.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Callable

import numpy as np
from scipy.integrate import quad

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

RESULTS_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the recorded checks."""

TOLERANCE = 1.0e-7
"""Absolute tolerance of the comparison of two numerical values."""

RANDOM_SEED = 20261122
"""Seed of the random sample of the limit test."""

Function = Callable[[float, float, float], float]
"""Type of an integrand of three variables."""


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


def inside_region(point: tuple[float, float, float]) -> bool:
    """Return True when one point satisfies the three raw defining inequalities.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when y >= x^2, z >= 0, and y + 2z <= 4.
    """
    x_value, y_value, z_value = point
    return bool(y_value >= x_value * x_value and z_value >= 0.0 and y_value + 2.0 * z_value <= 4.0)


def accepts_dz_dx_dy(point: tuple[float, float, float]) -> bool:
    """Return True when one point lies inside the printed limits of the order dz dx dy.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when 0 <= y <= 4, -sqrt(y) <= x <= sqrt(y), and 0 <= z <= (4 - y)/2.
    """
    x_value, y_value, z_value = point
    if not 0.0 <= y_value <= 4.0:
        return False
    half_width = math.sqrt(y_value)
    return bool(-half_width <= x_value <= half_width and 0.0 <= z_value <= (4.0 - y_value) / 2.0)


def accepts_dx_dz_dy(point: tuple[float, float, float]) -> bool:
    """Return True when one point lies inside the printed limits of the order dx dz dy.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when 0 <= y <= 4, 0 <= z <= (4 - y)/2, and -sqrt(y) <= x <= sqrt(y).
    """
    x_value, y_value, z_value = point
    if not 0.0 <= y_value <= 4.0:
        return False
    half_width = math.sqrt(y_value)
    return bool(0.0 <= z_value <= (4.0 - y_value) / 2.0 and -half_width <= x_value <= half_width)


def integral_dz_dx_dy(function: Function) -> float:
    """Return the integral in the order dz dx dy.

    Args:
        function: The integrand f(x, y, z).

    Returns:
        The numeric value of the iterated integral.
    """

    def section(y_value: float) -> float:
        half_width = math.sqrt(y_value)
        height = (4.0 - y_value) / 2.0

        def middle(x_value: float) -> float:
            value, _ = quad(lambda z_value: function(x_value, y_value, z_value), 0.0, height,
                            epsabs=1.0e-13, epsrel=1.0e-12)
            return value

        value, _ = quad(middle, -half_width, half_width, epsabs=1.0e-13, epsrel=1.0e-12,
                        limit=200)
        return value

    value, _ = quad(section, 0.0, 4.0, epsabs=1.0e-12, epsrel=1.0e-12, limit=200,
                    points=[0.0, 4.0])
    return value


def integral_dx_dz_dy(function: Function) -> float:
    """Return the integral in the order dx dz dy.

    Args:
        function: The integrand f(x, y, z).

    Returns:
        The numeric value of the iterated integral.
    """

    def section(y_value: float) -> float:
        half_width = math.sqrt(y_value)
        height = (4.0 - y_value) / 2.0

        def middle(z_value: float) -> float:
            value, _ = quad(lambda x_value: function(x_value, y_value, z_value), -half_width,
                            half_width, epsabs=1.0e-13, epsrel=1.0e-12)
            return value

        value, _ = quad(middle, 0.0, height, epsabs=1.0e-13, epsrel=1.0e-12, limit=200)
        return value

    value, _ = quad(section, 0.0, 4.0, epsabs=1.0e-12, epsrel=1.0e-12, limit=200,
                    points=[0.0, 4.0])
    return value


def volume_exact() -> Fraction:
    """Return the exact volume from the expanded polynomial (4 - x^2)^2 / 4.

    Returns:
        The exact volume as a fraction.
    """
    coefficients = [Fraction(4), Fraction(0), Fraction(-2), Fraction(0), Fraction(1, 4)]
    total = Fraction(0)
    for power, coefficient in enumerate(coefficients):
        total += coefficient * (Fraction(2) ** (power + 1) - Fraction(-2) ** (power + 1)) / (
            power + 1)
    return total


def minimum_inner_length() -> float:
    """Return the smallest inner interval length of the order dz dx dy on interior samples.

    Returns:
        The smallest height (4 - y)/2 over a grid that stays 0.05 away from each end.
    """
    shortest = float("inf")
    for y_value in np.linspace(0.05, 3.95, 40):
        shortest = min(shortest, (4.0 - y_value) / 2.0)
    return shortest


def main() -> None:
    """Run every check of Part 4, print the values, and write the result records."""
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 5000
    samples = np.column_stack((
        generator.uniform(-2.5, 2.5, sample_count),
        generator.uniform(-0.5, 4.5, sample_count),
        generator.uniform(-0.5, 2.5, sample_count),
    ))

    reference = np.array([inside_region(tuple(map(float, row))) for row in samples])
    first_limits = np.array([accepts_dz_dx_dy(tuple(map(float, row))) for row in samples])
    second_limits = np.array([accepts_dx_dz_dy(tuple(map(float, row))) for row in samples])
    first_disagreement = int(np.count_nonzero(first_limits != reference))
    second_disagreement = int(np.count_nonzero(second_limits != reference))
    reference_count = int(np.count_nonzero(reference))

    exact = float(volume_exact())
    values = {}
    for name, function in (("1", function_one), ("x^2+y+z", function_quadratic),
                           ("1+xyz", function_product)):
        values[name] = (integral_dz_dx_dy(function), integral_dx_dz_dy(function))

    print("=== Part 4: y outermost ===")
    print(f"sampled points                       : {sample_count}, inside E {reference_count}")
    print(f"dz dx dy limits against E            : disagreements {first_disagreement}, expected 0")
    print(f"dx dz dy limits against E            : disagreements {second_disagreement}, expected 0")
    print()
    for name, (first, second) in values.items():
        print(f"f = {name:8s}  dz dx dy {first:.12f}  dx dz dy {second:.12f}  "
              f"difference {abs(first - second):.3e}")
    print()
    print(f"volume exact                          : {exact:.12f} = 128/15")
    print(f"order dz dx dy against 128/15         : {abs(values['1'][0] - exact):.3e}")
    print(f"order dx dz dy against 128/15         : {abs(values['1'][1] - exact):.3e}")
    shortest = minimum_inner_length()
    print(f"smallest inner length (height in z)   : {shortest:.6e}, expected above 0")

    records: list[dict[str, float | str]] = [
        {
            "label": "Points that the limits of $dz\\,dx\\,dy$ and $E$ classify differently",
            "computed": float(first_disagreement),
            "expected": 0.0,
            "difference": float(first_disagreement),
            "tolerance": 0.0,
        },
        {
            "label": "Points that the limits of $dx\\,dz\\,dy$ and $E$ classify differently",
            "computed": float(second_disagreement),
            "expected": 0.0,
            "difference": float(second_disagreement),
            "tolerance": 0.0,
        },
    ]
    for name, (first, second) in values.items():
        records.append({
            "label": f"Order $dz\\,dx\\,dy$ against $dx\\,dz\\,dy$ for $f = {name}$",
            "computed": first,
            "expected": second,
            "difference": abs(first - second),
            "tolerance": TOLERANCE,
        })
    records.append({
        "label": "Order $dz\\,dx\\,dy$ against the exact volume $128/15$",
        "computed": values["1"][0],
        "expected": exact,
        "difference": abs(values["1"][0] - exact),
        "tolerance": TOLERANCE,
    })
    records.append({
        "label": "Order $dx\\,dz\\,dy$ against the exact volume $128/15$",
        "computed": values["1"][1],
        "expected": exact,
        "difference": abs(values["1"][1] - exact),
        "tolerance": TOLERANCE,
    })

    for record in records:
        if record["difference"] > record["tolerance"]:
            raise AssertionError(f"check failed: {record['label']}")
    if shortest <= 0.0:
        raise AssertionError("the inner interval of the order dz dx dy closes on the interior")

    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = RESULTS_DIRECTORY / "part4_results.json"
    target.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {target}")


if __name__ == "__main__":
    main()
