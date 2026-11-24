"""Check the reading of the three pairs of limits of the iterated integral.

The problem gives the iterated integral of Exercise 15.7.28 of Calculus: Early
Transcendentals.  The integral reads the outer limit of y as 0 to 2, the middle limit of z as
0 to 2 - y, and the inner limit of x as 0 to 4 - y^2.  This module writes the solid region in
three independent forms, compares the three forms on random points, measures the extent of the
region, and integrates the region in three orders.  Every assertion compares a value from one
form with a value from a different form.
"""

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.integrate import tplquad

RANDOM_SEED = 20261122
"""Seed of every pseudo-random sample of this module."""

SAMPLE_COUNT = 40000
"""Count of the random points that the comparison of the three forms uses."""

RANDOM_LOW = (-0.5, -0.5, -0.5)
"""Lower corner of the box that holds the sampled points, as (x, y, z)."""

RANDOM_HIGH = (4.5, 2.5, 2.5)
"""Upper corner of the box that holds the sampled points, as (x, y, z)."""

RESULT_PATH = Path(__file__).with_name("results") / "part1_results.json"
"""Path of the record that the product page reads."""


def region_from_nested_limits(x, y, z):
    """Return the membership of points, read directly from the three pairs of limits.

    Args:
        x: Array of the x coordinates.
        y: Array of the y coordinates.
        z: Array of the z coordinates.

    Returns:
        A boolean array.  An entry is True when the point obeys the three pairs of limits in
        the order of the differentials.
    """
    inside = (
        (y >= 0.0)
        & (y <= 2.0)
        & (z >= 0.0)
        & (z <= 2.0 - y)
        & (x >= 0.0)
        & (x <= 4.0 - y * y)
    )
    return inside


def region_from_flat_inequalities(x, y, z):
    """Return the membership of points, read from five inequalities in sum form.

    Args:
        x: Array of the x coordinates.
        y: Array of the y coordinates.
        z: Array of the z coordinates.

    Returns:
        A boolean array.  An entry is True when the point obeys the five inequalities
        y >= 0, y <= 2, z >= 0, y + z <= 2, x >= 0 and x + y^2 <= 4.
    """
    inside = (
        (0.0 <= y)
        & (y <= 2.0)
        & (0.0 <= z)
        & (y + z <= 2.0)
        & (0.0 <= x)
        & (x + y * y <= 4.0)
    )
    return inside


def region_from_solved_height(x, y, z):
    """Return the membership of points, with the height y solved out of the region.

    For one pair (x, z), the region holds the heights from zero to the smallest of the three
    numbers 2, 2 - z, and the square root of 4 - x.

    Args:
        x: Array of the x coordinates.
        y: Array of the y coordinates.
        z: Array of the z coordinates.

    Returns:
        A boolean array.  An entry is True when the point obeys the solved form.
    """
    reachable = np.sqrt(np.maximum(4.0 - x, 0.0))
    height_maximum = np.minimum(np.minimum(2.0, 2.0 - z), reachable)
    inside = (
        (0.0 <= x)
        & (x <= 4.0)
        & (0.0 <= z)
        & (0.0 <= y)
        & (y <= height_maximum)
    )
    return inside


def region_with_inner_limit_held_by_z(x, y, z):
    """Return the membership of points for the misreading x <= 4 - z^2.

    The inner limit of the integral holds y, not z.  This function records what the region
    becomes when a reader replaces y by z in that limit.

    Args:
        x: Array of the x coordinates.
        y: Array of the y coordinates.
        z: Array of the z coordinates.

    Returns:
        A boolean array.  An entry is True when the point obeys the misread limits.
    """
    inside = (
        (y >= 0.0)
        & (y <= 2.0)
        & (z >= 0.0)
        & (z <= 2.0 - y)
        & (x >= 0.0)
        & (x <= 4.0 - z * z)
    )
    return inside


def volume_in_given_order():
    """Return the value of the iterated integral in the order dx dz dy of the page.

    Returns:
        The value of the integral as a float.
    """
    value, _ = tplquad(
        lambda y, z, x: 1.0,
        0.0,
        2.0,
        lambda y: 0.0,
        lambda y: 2.0 - y,
        lambda y, z: 0.0,
        lambda y, z: 4.0 - y * y,
    )
    return value


def volume_with_other_inner_order():
    """Return the value of the integral with the two inner limits interchanged.

    The limits of x and z both hold y only.  The value must not change when the two inner
    limits trade places.

    Returns:
        The value of the integral as a float.
    """
    value, _ = tplquad(
        lambda y, x, z: 1.0,
        0.0,
        2.0,
        lambda y: 0.0,
        lambda y: 4.0 - y * y,
        lambda y, x: 0.0,
        lambda y, x: 2.0 - y,
    )
    return value


def volume_in_order_dx_dy_dz():
    """Return the value of the integral with z as the outer variable.

    The outer limit of z is 0 to 2.  At a fixed z, the height y runs from 0 to 2 - z, and x
    runs from 0 to 4 - y^2.  This nesting follows from the same region, read from z outward.

    Returns:
        The value of the integral as a float.
    """
    value, _ = tplquad(
        lambda z, y, x: 1.0,
        0.0,
        2.0,
        lambda z: 0.0,
        lambda z: 2.0 - z,
        lambda z, y: 0.0,
        lambda z, y: 4.0 - y * y,
    )
    return value


def exact_volume_from_polynomial():
    """Integrate the area of the cut exactly, with rational arithmetic.

    The area of the cut at the height y is the product of the two sides 4 - y^2 and 2 - y.
    The function multiplies the two polynomials with exact rational coefficients and then
    evaluates the antiderivative at the two ends of the interval.  No floating point number
    enters the computation, so the result is independent of the three numeric integrations.

    Returns:
        The volume of the solid as a Fraction.
    """
    first = [Fraction(4), Fraction(0), Fraction(-1)]
    second = [Fraction(2), Fraction(-1)]
    product = [Fraction(0)] * (len(first) + len(second) - 1)
    for index, left in enumerate(first):
        for offset, right in enumerate(second):
            product[index + offset] += left * right
    upper = 2
    total = Fraction(0)
    for power, coefficient in enumerate(product):
        total += coefficient * Fraction(upper ** (power + 1), power + 1)
    return total


def measure_extent():
    """Return the largest x, y and z of the region, from an analytic rule and from a grid.

    Returns:
        A dictionary with the analytic extent and the grid extent.
    """
    analytic = {"x": 4.0, "y": 2.0, "z": 2.0}
    heights = np.linspace(0.0, 2.0, 20001)
    length_x = 4.0 - heights * heights
    length_z = 2.0 - heights
    grid = {
        "x": float(np.max(length_x)),
        "y": float(np.max(heights)),
        "z": float(np.max(length_z)),
    }
    return {"analytic": analytic, "grid": grid}


def compare_forms():
    """Compare the three forms of the region on one random sample.

    Returns:
        A dictionary with the sample count and the disagreement counts.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    low = np.array(RANDOM_LOW)
    high = np.array(RANDOM_HIGH)
    points = low + (high - low) * generator.random((SAMPLE_COUNT, 3))
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    nested = region_from_nested_limits(x, y, z)
    flat = region_from_flat_inequalities(x, y, z)
    solved = region_from_solved_height(x, y, z)
    misread = region_with_inner_limit_held_by_z(x, y, z)
    return {
        "sample_count": SAMPLE_COUNT,
        "inside_count": int(np.count_nonzero(nested)),
        "nested_against_flat": int(np.count_nonzero(nested != flat)),
        "nested_against_solved": int(np.count_nonzero(nested != solved)),
        "nested_against_misread": int(np.count_nonzero(nested != misread)),
    }


def probe_misreading():
    """Compare the correct region with the misread region at two named points.

    Returns:
        A dictionary with the membership of each point in each region.
    """
    probes = {
        "x_above_the_wall": (3.5, 1.0, 0.5),
        "x_below_the_wall": (1.0, 1.0, 0.5),
    }
    record = {}
    for name, (x, y, z) in probes.items():
        arguments = (np.array([x]), np.array([y]), np.array([z]))
        record[name] = {
            "point": [x, y, z],
            "inside_by_limits": bool(region_from_nested_limits(*arguments)[0]),
            "inside_by_misreading": bool(region_with_inner_limit_held_by_z(*arguments)[0]),
        }
    return record


def main():
    """Run every check of part 1 and write the record of the checked values."""
    comparison = compare_forms()
    extent = measure_extent()
    given = volume_in_given_order()
    swapped = volume_with_other_inner_order()
    reordered = volume_in_order_dx_dy_dz()
    spread = max(abs(given - swapped), abs(given - reordered), abs(swapped - reordered))
    probes = probe_misreading()
    exact = exact_volume_from_polynomial()

    print("part 1 checks")
    print(f"sample count                     : {comparison['sample_count']}")
    print(f"points inside the region         : {comparison['inside_count']}")
    print(f"nested against flat disagreements: {comparison['nested_against_flat']}")
    print(f"nested against solved disagreements: {comparison['nested_against_solved']}")
    print(f"nested against misread disagreements: {comparison['nested_against_misread']}")
    for axis in ("x", "y", "z"):
        print(
            f"largest {axis} of the region        : "
            f"{extent['analytic'][axis]:.12f} analytic, {extent['grid'][axis]:.12f} grid"
        )
    print(f"volume in the order dx dz dy     : {given:.12f}")
    print(f"volume with the inner limits swapped: {swapped:.12f}")
    print(f"volume in the order dx dy dz     : {reordered:.12f}")
    print(f"largest gap between the three    : {spread:.3e}")
    print(f"volume from the exact polynomial : {exact} = {float(exact):.12f}")
    for name, record in probes.items():
        print(
            f"probe {name:22s}: inside by limits {record['inside_by_limits']}, "
            f"inside by misreading {record['inside_by_misreading']}"
        )

    assert comparison["nested_against_flat"] == 0, "the flat inequalities disagree with the limits"
    assert comparison["nested_against_solved"] == 0, "the solved form disagrees with the limits"
    assert comparison["inside_count"] > 1000, "too few sampled points fall inside the region"
    assert comparison["nested_against_misread"] > 1000, "the misreading is not distinguishable"
    for axis in ("x", "y", "z"):
        assert abs(extent["analytic"][axis] - extent["grid"][axis]) < 1.0e-9, (
            f"the extent of {axis} disagrees with the grid"
        )
    assert spread < 1.0e-9, "the three orders give different values"
    assert abs(float(exact) - given) < 1.0e-9, (
        f"the exact value {exact} disagrees with the numeric value {given}"
    )
    assert probes["x_above_the_wall"]["inside_by_limits"] is False, "the probe is not outside"
    assert probes["x_above_the_wall"]["inside_by_misreading"] is True, (
        "the misreading does not admit the probe"
    )

    record = {
        "sample_count": comparison["sample_count"],
        "inside_count": comparison["inside_count"],
        "nested_against_flat": comparison["nested_against_flat"],
        "nested_against_solved": comparison["nested_against_solved"],
        "nested_against_misread": comparison["nested_against_misread"],
        "extent": extent,
        "volume": {
            "given_order": given,
            "swapped_inner_order": swapped,
            "order_x_y_z": reordered,
            "largest_gap": spread,
            "exact_numerator": exact.numerator,
            "exact_denominator": exact.denominator,
            "exact_text": f"{exact.numerator}/{exact.denominator}",
            "exact_value": float(exact),
        },
        "probes": probes,
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"record written to {RESULT_PATH}")
    print("part 1: all checks passed")


if __name__ == "__main__":
    main()
