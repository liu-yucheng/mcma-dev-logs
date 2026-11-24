"""Verify the region, its three projections, and its volume for Stewart 15.7 Exercise 31.

The solid E is bounded by y = x^2, z = 0, and y + 2z = 4.  This script reduces the three raw
inequalities to one bound chain, checks the reduction on random points, and computes the volume by
two different orders of integration and by exact rational arithmetic.

Run this script with the interpreter of ``code/.venv``.  It prints each checked value beside the
value that an independent method gives, and it writes the records to
``code/results/part1_results.json``.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import quad

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

RESULTS_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the recorded checks."""

RANDOM_SEED = 20261122
"""Seed of every random sample of this script."""

TOLERANCE = 1.0e-9
"""Absolute tolerance of a numeric comparison against an exact value."""


def inside_region_raw(point: tuple[float, float, float]) -> bool:
    """Return True when one point satisfies the three raw defining inequalities.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when y >= x^2, z >= 0, and y + 2z <= 4.
    """
    x_value, y_value, z_value = point
    return bool(y_value >= x_value * x_value and z_value >= 0.0 and y_value + 2.0 * z_value <= 4.0)


def inside_region_chain(point: tuple[float, float, float]) -> bool:
    """Return True when one point satisfies the reduced bound chain of this script.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when x^2 <= y <= 4 and 0 <= z <= (4 - y) / 2.
    """
    x_value, y_value, z_value = point
    return bool(x_value * x_value <= y_value <= 4.0 and 0.0 <= z_value <= (4.0 - y_value) / 2.0)


def inside_alternative(point: tuple[float, float, float]) -> bool:
    """Return True when one point satisfies the rejected orientation of the cylinder.

    Args:
        point: The coordinates (x, y, z) of the point.

    Returns:
        True when y <= x^2, z >= 0, and y + 2z <= 4.
    """
    x_value, y_value, z_value = point
    return bool(y_value <= x_value * x_value and z_value >= 0.0 and y_value + 2.0 * z_value <= 4.0)


def volume_order_dz_dy_dx() -> float:
    """Return the volume from the order dz dy dx, with two nested calls of ``quad``.

    Returns:
        The numeric volume of the solid.
    """

    def height(y_value: float) -> float:
        return (4.0 - y_value) / 2.0

    def section(x_value: float) -> float:
        value, _ = quad(height, x_value * x_value, 4.0, epsabs=1.0e-13, epsrel=1.0e-13, limit=200)
        return value

    value, _ = quad(section, -2.0, 2.0, epsabs=1.0e-12, epsrel=1.0e-12, limit=200, points=[0.0])
    return value


def volume_order_dy_dx_dz() -> float:
    """Return the volume from the order dy dx dz, with two nested calls of ``quad``.

    Returns:
        The numeric volume of the solid.
    """

    def section(z_value: float) -> float:
        half_width = math.sqrt(max(4.0 - 2.0 * z_value, 0.0))
        cap = 4.0 - 2.0 * z_value
        value, _ = quad(lambda x_value: cap - x_value * x_value, -half_width, half_width,
                        epsabs=1.0e-14, epsrel=1.0e-13, limit=100)
        return value

    value, _ = quad(section, 0.0, 2.0, epsabs=1.0e-11, epsrel=1.0e-12, limit=200,
                    points=[0.0, 2.0])
    return value


def integrate_polynomial(coefficients: list[Fraction], low: Fraction, high: Fraction) -> Fraction:
    """Return the exact integral of one polynomial over one interval.

    Args:
        coefficients: The coefficient of x^0, x^1, ... in ascending order.
        low: The lower limit of the interval.
        high: The upper limit of the interval.

    Returns:
        The exact value of the integral.
    """
    total = Fraction(0)
    for power, coefficient in enumerate(coefficients):
        total += coefficient * (high ** (power + 1) - low ** (power + 1)) / (power + 1)
    return total


def volume_exact() -> Fraction:
    """Return the exact volume from the expanded polynomial (4 - x^2)^2 / 4.

    Returns:
        The exact volume as a fraction.
    """
    coefficients = [Fraction(4), Fraction(0), Fraction(-2), Fraction(0), Fraction(1, 4)]
    return integrate_polynomial(coefficients, Fraction(-2), Fraction(2))


def projection_areas() -> tuple[float, float, float]:
    """Return the numeric areas of the three projections.

    Returns:
        The area on the plane z = 0, the area on the plane x = 0, and the area on the plane y = 0.
    """
    area_on_plane_z_zero, _ = quad(lambda x_value: 4.0 - x_value * x_value, -2.0, 2.0,
                                   epsabs=1.0e-13, epsrel=1.0e-13)
    area_on_plane_x_zero, _ = quad(lambda y_value: (4.0 - y_value) / 2.0, 0.0, 4.0,
                                   epsabs=1.0e-13, epsrel=1.0e-13)
    area_on_plane_y_zero, _ = quad(lambda z_value: 2.0 * math.sqrt(max(4.0 - 2.0 * z_value, 0.0)),
                                   0.0, 2.0, epsabs=1.0e-12, epsrel=1.0e-12, points=[2.0])
    return area_on_plane_z_zero, area_on_plane_x_zero, area_on_plane_y_zero


def main() -> None:
    """Run every check of Part 1, print the values, and write the result records."""
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 20000
    samples = np.column_stack((
        generator.uniform(-3.0, 3.0, sample_count),
        generator.uniform(-0.5, 4.5, sample_count),
        generator.uniform(-0.5, 2.5, sample_count),
    ))

    raw_flags = np.array([inside_region_raw(tuple(map(float, row))) for row in samples])
    chain_flags = np.array([inside_region_chain(tuple(map(float, row))) for row in samples])
    disagreement_count = int(np.count_nonzero(raw_flags != chain_flags))
    inside_count = int(np.count_nonzero(raw_flags))

    exact_volume = volume_exact()
    numeric_volume_first = volume_order_dz_dy_dx()
    numeric_volume_fourth = volume_order_dy_dx_dz()

    area_z, area_x, area_y = projection_areas()

    alternative_points = [(1000.0, 0.0, 0.0), (1000.0, 4.0, 0.0), (5.0, 0.0, 2.0)]
    alternative_flags = [inside_alternative(point) and not inside_region_raw(point)
                         for point in alternative_points]
    alternative_gap = max(abs(point[0]) for point in alternative_points)
    region_x_limit = 2.0

    maximum_x_member = inside_region_raw((2.0, 4.0, 0.0))
    outside_x_member = inside_region_raw((2.0 + 1.0e-9, 4.0, 0.0))

    print("=== Part 1: the region and its volume ===")
    print(f"sampled points                 : {sample_count}")
    print(f"sampled points inside E        : {inside_count}")
    print(f"raw inequalities against chain : disagreements {disagreement_count}, expected 0")
    print(f"corner (2, 4, 0) inside E      : {maximum_x_member}, expected True")
    print(f"corner (2 + 1e-9, 4, 0) inside : {outside_x_member}, expected False")
    print(f"rejected orientation admits |x|: {alternative_gap}, E allows |x| <= {region_x_limit}")
    print(f"rejected orientation probes    : {alternative_flags}, expected [True, True, True]")
    print()
    print(f"volume, exact (4 - x^2)^2 / 4  : {exact_volume} = {float(exact_volume):.15f}")
    print(f"volume, order dz dy dx         : {numeric_volume_first:.15f}")
    print(f"volume, order dy dx dz         : {numeric_volume_fourth:.15f}")
    print(f"difference, first against exact : {abs(numeric_volume_first - float(exact_volume)):.3e}")
    print(f"difference, second against exact: {abs(numeric_volume_fourth - float(exact_volume)):.3e}")
    print()
    print(f"projection area on plane z = 0 : {area_z:.15f}, closed form 32/3 = {32.0 / 3.0:.15f}")
    print(f"projection area on plane x = 0 : {area_x:.15f}, closed form 4 = 4")
    print(f"projection area on plane y = 0 : {area_y:.15f}, closed form 16/3 = {16.0 / 3.0:.15f}")
    print(f"sum of the three projection areas: {area_z + area_x + area_y:.15f}, closed form 20")

    records = [
        {
            "label": "Points that the raw inequalities and the bound chain classify differently",
            "computed": float(disagreement_count),
            "expected": 0.0,
            "difference": float(disagreement_count),
            "tolerance": 0.0,
        },
        {
            "label": "Volume from the order $dz\\,dy\\,dx$ against the exact value $128/15$",
            "computed": numeric_volume_first,
            "expected": float(exact_volume),
            "difference": abs(numeric_volume_first - float(exact_volume)),
            "tolerance": TOLERANCE,
        },
        {
            "label": "Volume from the order $dy\\,dx\\,dz$ against the exact value $128/15$",
            "computed": numeric_volume_fourth,
            "expected": float(exact_volume),
            "difference": abs(numeric_volume_fourth - float(exact_volume)),
            "tolerance": TOLERANCE,
        },
        {
            "label": "Area of the projection on the plane $z = 0$ against $32/3$",
            "computed": area_z,
            "expected": 32.0 / 3.0,
            "difference": abs(area_z - 32.0 / 3.0),
            "tolerance": TOLERANCE,
        },
        {
            "label": "Area of the projection on the plane $x = 0$ against $4$",
            "computed": area_x,
            "expected": 4.0,
            "difference": abs(area_x - 4.0),
            "tolerance": TOLERANCE,
        },
        {
            "label": "Area of the projection on the plane $y = 0$ against $16/3$",
            "computed": area_y,
            "expected": 16.0 / 3.0,
            "difference": abs(area_y - 16.0 / 3.0),
            "tolerance": TOLERANCE,
        },
    ]

    for record in records:
        if record["difference"] > record["tolerance"]:
            raise AssertionError(f"check failed: {record['label']}")
    if alternative_flags != [True, True, True]:
        raise AssertionError("the rejected orientation must admit the probe points")
    if not (maximum_x_member and not outside_x_member):
        raise AssertionError("the bound |x| <= 2 must be attained and must not be exceeded")

    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = RESULTS_DIRECTORY / "part1_results.json"
    target.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {target}")


if __name__ == "__main__":
    main()
