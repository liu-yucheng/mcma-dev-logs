"""Verify the section at a fixed y and the two orders with y as the outer variable.

For a fixed value of y the two conditions |x| <= 2 and z^2 <= 9 - y^2 involve different
variables and no other condition couples them.  The section is therefore the rectangle
[-2, 2] x [-sqrt(9 - y^2), sqrt(9 - y^2)].  This script checks four claims.

1.  The section at a fixed y is that rectangle, and its area is 8*sqrt(9 - y^2).
2.  At y = 3 and at y = -3 the rectangle collapses to the segment [-2, 2] on the line z = 0.
    The script prints the corner list of every measured section before the page names its shape.
3.  The order dz dx dy and the order dx dz dy both give 36*pi and 117*pi.
4.  The limis from the rectangle give a different number when the z bound is replaced by the
    constant 3, so the check of Item 3 can fail.

Run this script with the interpreter of `code/.venv`.  It writes
`code/results/part3_results.json`.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import integrate

RADIUS = 3.0
"""Radius of the circular cylinder y^2 + z^2 = 9."""

HALF_LENGTH = 2.0
"""Half of the distance between the planes x = -2 and x = 2."""

CYLINDER_LENGTH = 2.0 * HALF_LENGTH
"""Distance between the two planes x = -2 and x = 2."""

EXACT_VOLUME = math.pi * RADIUS**2 * CYLINDER_LENGTH
"""Volume of E, thus 36*pi."""

SECTION_CELL_COUNT_ACROSS_X = 200
"""Number of grid cells along x in a section area measurement."""

SECTION_CELL_COUNT_ACROSS_Z = 12000
"""Number of grid cells along z in a section area measurement."""

GRID_AREA_TOLERANCE = 0.01
"""Largest accepted difference between a grid area and the closed area.

The grid rounds the z extent of a section to a whole number of cells.  The largest error of one
section is four times the cell size along z, which is 0.002 at the grid of this script.
"""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part3_results.json"
"""Path of the machine-readable record of the checks."""


def rectangle_half_width(fixed_y: float) -> float:
    """Return the half width in z of the section at the fixed value y.

    Args:
        fixed_y: Value of y at which the half width is measured.

    Returns:
        sqrt(9 - y^2), or 0 when |y| >= 3.
    """
    return math.sqrt(max(RADIUS**2 - fixed_y * fixed_y, 0.0))


def corners_of_section(fixed_y: float) -> list[tuple[float, float]]:
    """Return the corner list of the section at the fixed value y, in (x, z) coordinates.

    A degenerate section returns its two distinct corners only, so that the caller can see
    whether the section is a rectangle or a segment.

    Args:
        fixed_y: Value of y at which the corners are listed.

    Returns:
        The distinct corners of the section.
    """
    half_width = rectangle_half_width(fixed_y)
    corners = [(-HALF_LENGTH, -half_width), (HALF_LENGTH, -half_width),
               (HALF_LENGTH, half_width), (-HALF_LENGTH, half_width)]
    distinct: list[tuple[float, float]] = []
    for corner in corners:
        if not any(abs(corner[0] - other[0]) < 1e-12 and abs(corner[1] - other[1]) < 1e-12
                   for other in distinct):
            distinct.append(corner)
    return distinct


def section_area_by_grid(fixed_y: float) -> float:
    """Return the area of the section at the fixed value y, measured on a midpoint grid.

    The grid covers x in [-2, 2] and z in [-3, 3].  A cell counts when its centre satisfies
    |x| <= 2 and z^2 <= 9 - y^2.

    Args:
        fixed_y: Value of y at which the section is measured.

    Returns:
        The measured area of the section.
    """
    step_across_x = CYLINDER_LENGTH / SECTION_CELL_COUNT_ACROSS_X
    step_across_z = 2.0 * RADIUS / SECTION_CELL_COUNT_ACROSS_Z
    centres_across_x = -HALF_LENGTH + step_across_x * (np.arange(SECTION_CELL_COUNT_ACROSS_X) + 0.5)
    centres_across_z = -RADIUS + step_across_z * (np.arange(SECTION_CELL_COUNT_ACROSS_Z) + 0.5)
    grid_x, grid_z = np.meshgrid(centres_across_x, centres_across_z, indexing="ij")
    inside = grid_z**2 <= RADIUS**2 - fixed_y * fixed_y
    return float(np.count_nonzero(inside)) * step_across_x * step_across_z


def integrate_once(integrand, low: float, high: float) -> float:
    """Return the one-dimensional integral of `integrand` between two limits.

    Args:
        integrand: Function of one variable.
        low: Lower limit.
        high: Upper limit.

    Returns:
        The value of the integral.
    """
    value, _ = integrate.quad(integrand, low, high, epsabs=1e-12, epsrel=1e-12, limit=200)
    return float(value)


def order_dz_dx_dy(integrand, follow_cylinder: bool = True) -> float:
    """Return the iterated integral with the order dz dx dy.

    The inner integral runs over z, the middle integral runs over x, and the outer integral
    runs over y.  The nested `quad` calls follow that order from the inside out.

    Args:
        integrand: Function of (x, y, z).
        follow_cylinder: When True, the inner limits are the two halves of the cylinder at
            the fixed value of y.  When False, the inner limits are the constants -3 and 3.

    Returns:
        The value of the iterated integral.
    """
    def integral_over_z(fixed_y: float, fixed_x: float) -> float:
        if follow_cylinder:
            half_width = rectangle_half_width(fixed_y)
        else:
            half_width = RADIUS
        return integrate_once(lambda z: integrand(fixed_x, fixed_y, z),
                              -half_width, half_width)

    def integral_over_x(fixed_y: float) -> float:
        return integrate_once(lambda x: integral_over_z(fixed_y, x), -HALF_LENGTH, HALF_LENGTH)

    return integrate_once(integral_over_x, -RADIUS, RADIUS)


def order_dx_dz_dy(integrand) -> float:
    """Return the iterated integral with the order dx dz dy.

    The inner integral runs over x, the middle integral runs over z, and the outer integral
    runs over y.

    Args:
        integrand: Function of (x, y, z).

    Returns:
        The value of the iterated integral.
    """
    def integral_over_x(fixed_y: float, fixed_z: float) -> float:
        return integrate_once(lambda x: integrand(x, fixed_y, fixed_z), -HALF_LENGTH, HALF_LENGTH)

    def integral_over_z(fixed_y: float) -> float:
        half_width = rectangle_half_width(fixed_y)
        return integrate_once(lambda z: integral_over_x(fixed_y, z), -half_width, half_width)

    return integrate_once(integral_over_z, -RADIUS, RADIUS)


def exact_integral_of_y_squared() -> float:
    """Return the integral of y^2 over E by a single integral over y.

    The integral is the integral over y of y^2 times the section area 8*sqrt(9 - y^2).
    """
    value, _ = integrate.quad(
        lambda y: y * y * 2.0 * CYLINDER_LENGTH * math.sqrt(max(RADIUS**2 - y * y, 0.0)),
        -RADIUS, RADIUS, limit=400)
    return float(value)


def record(results: list[dict[str, object]], label: str, computed: float, expected: float,
           tolerance: float) -> None:
    """Append one comparison to the record, print it, and raise when it fails."""
    difference = abs(computed - expected)
    passed = difference <= tolerance
    results.append({
        "label": label,
        "computed": computed,
        "expected": expected,
        "difference": difference,
        "tolerance": tolerance,
        "passed": passed,
    })
    print(f"{label}: computed={computed:.12f} expected={expected:.12f} "
          f"difference={difference:.3e} tolerance={tolerance:.3e}")
    if not passed:
        raise AssertionError(f"{label}: difference {difference:.6e} exceeds {tolerance:.6e}")


def main() -> None:
    """Run every check of Part 3 and write the record."""
    results: list[dict[str, object]] = []

    for fixed_y in (-3.0, -2.0, 0.0, 1.5, 3.0):
        half_width = rectangle_half_width(fixed_y)
        corners = corners_of_section(fixed_y)
        print(f"y = {fixed_y:+.1f}: half width = {half_width:.12f}, "
              f"corners = {[(round(x, 6), round(z, 6)) for x, z in corners]}")
        measured_area = section_area_by_grid(fixed_y)
        expected_area = 2.0 * CYLINDER_LENGTH * half_width
        record(results, f"section area at y = {fixed_y:+.1f} against 8*sqrt(9 - y^2)",
               measured_area, expected_area, GRID_AREA_TOLERANCE)

    print("shape record: y = -2.0 and y = +1.5 give a rectangle; y = -3.0 and y = +3.0 give "
          "the segment [-2, 2] on the line z = 0")

    lift_points = [(-2.0, 1.5, 2.5), (0.0, 1.5, -2.5), (2.0, 1.5, 0.0)]
    for point in lift_points:
        inside = abs(point[0]) <= HALF_LENGTH and point[2] ** 2 <= RADIUS**2 - point[1] ** 2
        print(f"lift of the corner point {point} lies in the section: {inside}")
        if not inside:
            raise AssertionError(f"the point {point} should lie in the section at y = 1.5")
        results.append({
            "label": f"membership of the section point {point}",
            "computed": 1.0,
            "expected": 1.0,
            "difference": 0.0,
            "tolerance": 0.0,
            "passed": True,
        })

    exact_quadratic = EXACT_VOLUME + exact_integral_of_y_squared()

    volume_dz_dx_dy = order_dz_dx_dy(lambda x, y, z: 1.0)
    volume_dx_dz_dy = order_dx_dz_dy(lambda x, y, z: 1.0)
    record(results, "order dz dx dy against 36*pi for f = 1", volume_dz_dx_dy, EXACT_VOLUME, 1e-6)
    record(results, "order dx dz dy against 36*pi for f = 1", volume_dx_dz_dy, EXACT_VOLUME, 1e-6)
    record(results, "the two orders with y outer agree for f = 1",
           volume_dz_dx_dy, volume_dx_dz_dy, 1e-8)

    value_dz_dx_dy = order_dz_dx_dy(lambda x, y, z: 1.0 + x + y * y)
    value_dx_dz_dy = order_dx_dz_dy(lambda x, y, z: 1.0 + x + y * y)
    record(results, "order dz dx dy against 117*pi for f = 1 + x + y^2",
           value_dz_dx_dy, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "order dx dz dy against 117*pi for f = 1 + x + y^2",
           value_dx_dz_dy, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "the two orders with y outer agree for f = 1 + x + y^2",
           value_dz_dx_dy, value_dx_dz_dy, 1e-6 * exact_quadratic)

    wrong_limits_value = order_dz_dx_dy(lambda x, y, z: 1.0, follow_cylinder=False)
    box_volume = CYLINDER_LENGTH * (2.0 * RADIUS) * (2.0 * RADIUS)
    print(f"order dz dx dy with z from -3 to 3 gives {wrong_limits_value:.6f}")
    print(f"distance of that value to 36*pi = {abs(wrong_limits_value - EXACT_VOLUME):.6f}")
    if abs(wrong_limits_value - EXACT_VOLUME) < 20.0:
        raise AssertionError("the negative control does not separate the two limit sets")
    results.append({
        "label": "negative control: z from -3 to 3 is not the rectangle bound",
        "computed": wrong_limits_value,
        "expected": box_volume,
        "difference": abs(wrong_limits_value - box_volume),
        "tolerance": 1e-6,
        "passed": abs(wrong_limits_value - box_volume) <= 1e-6,
    })

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
