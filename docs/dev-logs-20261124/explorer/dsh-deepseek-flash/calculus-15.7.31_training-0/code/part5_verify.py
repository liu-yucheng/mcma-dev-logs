"""Verify the two orders of integration with z outermost for Stewart 15.7 Exercise 31.

The section at a fixed z is the parabolic segment of Part 2.  This script computes the same integral
in the two orders that start with z: dy dx dz and dx dy dz.  Each order is one single integral with
variable limits and no split.  The script compares the two orders with each other, compares both
with the exact volume 128/15, and tests each printed limit set against the raw defining
inequalities on random points.

Run this script with the interpreter of ``code/.venv``.  It prints each checked value beside the
value that an independent method gives, and it writes the records to
``code/results/part5_results.json``.
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


def accepts_dy_dx_dz(point: tuple[float, float, float]) -> bool:
    """Return True when one point lies inside the printed limits of the order dy dx dz.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when 0 <= z <= 2, -sqrt(4 - 2z) <= x <= sqrt(4 - 2z), and x^2 <= y <= 4 - 2z.
    """
    x_value, y_value, z_value = point
    if not 0.0 <= z_value <= 2.0:
        return False
    cap = 4.0 - 2.0 * z_value
    return bool(-math.sqrt(cap) <= x_value <= math.sqrt(cap)
                and x_value * x_value <= y_value <= cap)


def accepts_dx_dy_dz(point: tuple[float, float, float]) -> bool:
    """Return True when one point lies inside the printed limits of the order dx dy dz.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when 0 <= z <= 2, 0 <= y <= 4 - 2z, and -sqrt(y) <= x <= sqrt(y).
    """
    x_value, y_value, z_value = point
    if not 0.0 <= z_value <= 2.0:
        return False
    cap = 4.0 - 2.0 * z_value
    return bool(0.0 <= y_value <= cap and -math.sqrt(y_value) <= x_value <= math.sqrt(y_value))


def integral_dy_dx_dz(function: Function) -> float:
    """Return the integral in the order dy dx dz.

    Args:
        function: The integrand f(x, y, z).

    Returns:
        The numeric value of the iterated integral.
    """

    def section(z_value: float) -> float:
        cap = 4.0 - 2.0 * z_value
        half_width = math.sqrt(max(cap, 0.0))

        def middle(x_value: float) -> float:
            value, _ = quad(lambda y_value: function(x_value, y_value, z_value),
                            x_value * x_value, cap, epsabs=1.0e-13, epsrel=1.0e-12)
            return value

        value, _ = quad(middle, -half_width, half_width, epsabs=1.0e-13, epsrel=1.0e-12,
                        limit=200)
        return value

    value, _ = quad(section, 0.0, 2.0, epsabs=1.0e-11, epsrel=1.0e-12, limit=200,
                    points=[0.0, 2.0])
    return value


def integral_dx_dy_dz(function: Function) -> float:
    """Return the integral in the order dx dy dz.

    Args:
        function: The integrand f(x, y, z).

    Returns:
        The numeric value of the iterated integral.
    """

    def section(z_value: float) -> float:
        cap = 4.0 - 2.0 * z_value

        def middle(y_value: float) -> float:
            half_width = math.sqrt(max(y_value, 0.0))
            value, _ = quad(lambda x_value: function(x_value, y_value, z_value), -half_width,
                            half_width, epsabs=1.0e-13, epsrel=1.0e-12, limit=100)
            return value

        value, _ = quad(middle, 0.0, cap, epsabs=1.0e-13, epsrel=1.0e-12, limit=200)
        return value

    value, _ = quad(section, 0.0, 2.0, epsabs=1.0e-11, epsrel=1.0e-12, limit=200,
                    points=[0.0, 2.0])
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
    """Return the smallest inner interval length of the order dy dx dz on interior samples.

    Returns:
        The smallest value of the vertical length 4 - 2z - x^2 over an interior grid.
    """
    shortest = float("inf")
    for z_value in np.linspace(0.0, 1.95, 20):
        cap = 4.0 - 2.0 * z_value
        limit = math.sqrt(cap) * 0.98
        for x_value in np.linspace(-limit, limit, 20):
            shortest = min(shortest, cap - x_value * x_value)
    return shortest


def main() -> None:
    """Run every check of Part 5, print the values, and write the result records."""
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 5000
    samples = np.column_stack((
        generator.uniform(-2.5, 2.5, sample_count),
        generator.uniform(-0.5, 4.5, sample_count),
        generator.uniform(-0.5, 2.5, sample_count),
    ))

    reference = np.array([inside_region(tuple(map(float, row))) for row in samples])
    first_limits = np.array([accepts_dy_dx_dz(tuple(map(float, row))) for row in samples])
    second_limits = np.array([accepts_dx_dy_dz(tuple(map(float, row))) for row in samples])
    first_disagreement = int(np.count_nonzero(first_limits != reference))
    second_disagreement = int(np.count_nonzero(second_limits != reference))
    reference_count = int(np.count_nonzero(reference))

    exact = float(volume_exact())
    values = {}
    for name, function in (("1", function_one), ("x^2+y+z", function_quadratic),
                           ("1+xyz", function_product)):
        values[name] = (integral_dy_dx_dz(function), integral_dx_dy_dz(function))

    print("=== Part 5: z outermost ===")
    print(f"sampled points                       : {sample_count}, inside E {reference_count}")
    print(f"dy dx dz limits against E            : disagreements {first_disagreement}, expected 0")
    print(f"dx dy dz limits against E            : disagreements {second_disagreement}, expected 0")
    print()
    for name, (first, second) in values.items():
        print(f"f = {name:8s}  dy dx dz {first:.12f}  dx dy dz {second:.12f}  "
              f"difference {abs(first - second):.3e}")
    print()
    print(f"volume exact                          : {exact:.12f} = 128/15")
    print(f"order dy dx dz against 128/15         : {abs(values['1'][0] - exact):.3e}")
    print(f"order dx dy dz against 128/15         : {abs(values['1'][1] - exact):.3e}")
    shortest = minimum_inner_length()
    print(f"smallest inner length (height in y)   : {shortest:.6e}, expected above 0")

    records: list[dict[str, float | str]] = [
        {
            "label": "Points that the limits of $dy\\,dx\\,dz$ and $E$ classify differently",
            "computed": float(first_disagreement),
            "expected": 0.0,
            "difference": float(first_disagreement),
            "tolerance": 0.0,
        },
        {
            "label": "Points that the limits of $dx\\,dy\\,dz$ and $E$ classify differently",
            "computed": float(second_disagreement),
            "expected": 0.0,
            "difference": float(second_disagreement),
            "tolerance": 0.0,
        },
    ]
    for name, (first, second) in values.items():
        records.append({
            "label": f"Order $dy\\,dx\\,dz$ against $dx\\,dy\\,dz$ for $f = {name}$",
            "computed": first,
            "expected": second,
            "difference": abs(first - second),
            "tolerance": TOLERANCE,
        })
    records.append({
        "label": "Order $dy\\,dx\\,dz$ against the exact volume $128/15$",
        "computed": values["1"][0],
        "expected": exact,
        "difference": abs(values["1"][0] - exact),
        "tolerance": TOLERANCE,
    })
    records.append({
        "label": "Order $dx\\,dy\\,dz$ against the exact volume $128/15$",
        "computed": values["1"][1],
        "expected": exact,
        "difference": abs(values["1"][1] - exact),
        "tolerance": TOLERANCE,
    })

    for record in records:
        if record["difference"] > record["tolerance"]:
            raise AssertionError(f"check failed: {record['label']}")
    if shortest <= 0.0:
        raise AssertionError("the inner interval of the order dy dx dz closes on the interior")

    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = RESULTS_DIRECTORY / "part5_results.json"
    target.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {target}")


if __name__ == "__main__":
    main()
