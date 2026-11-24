"""Verify the section at a fixed z and the two orders with z as the outer variable.

The cylinder y^2 + z^2 = 9 and the planes x = -2 and x = 2 treat y and z in the same way.  For a
fixed value of z the two conditions are |x| <= 2 and y^2 <= 9 - z^2, and they involve different
variables.  The section is therefore the rectangle [-2, 2] x [-sqrt(9 - z^2), sqrt(9 - z^2)].
This script checks five claims.

1.  The section at a fixed z is that rectangle, and its area is 8*sqrt(9 - z^2).
2.  At z = 3 and at z = -3 the rectangle collapses to the segment [-2, 2] on the line y = 0.
    The script prints the corner list of every measured section before the page names its shape.
3.  The section area at a fixed z equals the section area at the same value of y, which Part 3
    measures with the roles of y and z exchanged.
4.  The order dy dx dz and the order dx dy dz both give 36*pi and 117*pi.
5.  The integral of z^2 over E is 81*pi, the same number as the integral of y^2.

Run this script with the interpreter of `code/.venv`.  It writes
`code/results/part4_results.json`.
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

SECTION_CELL_COUNT_ACROSS_Y = 12000
"""Number of grid cells along y in a section area measurement."""

GRID_AREA_TOLERANCE = 0.01
"""Largest accepted difference between a grid area and the closed area."""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part4_results.json"
"""Path of the machine-readable record of the checks."""


def rectangle_half_width(fixed_z: float) -> float:
    """Return the half width in y of the section at the fixed value z.

    Args:
        fixed_z: Value of z at which the half width is measured.

    Returns:
        sqrt(9 - z^2), or 0 when |z| >= 3.
    """
    return math.sqrt(max(RADIUS**2 - fixed_z * fixed_z, 0.0))


def corners_of_section(fixed_z: float) -> list[tuple[float, float]]:
    """Return the distinct corners of the section at the fixed value z, in (x, y) coordinates.

    Args:
        fixed_z: Value of z at which the corners are listed.

    Returns:
        The distinct corners of the section.
    """
    half_width = rectangle_half_width(fixed_z)
    corners = [(-HALF_LENGTH, -half_width), (HALF_LENGTH, -half_width),
               (HALF_LENGTH, half_width), (-HALF_LENGTH, half_width)]
    distinct: list[tuple[float, float]] = []
    for corner in corners:
        if not any(abs(corner[0] - other[0]) < 1e-12 and abs(corner[1] - other[1]) < 1e-12
                   for other in distinct):
            distinct.append(corner)
    return distinct


def section_area_by_grid(fixed_z: float) -> float:
    """Return the area of the section at the fixed value z, measured on a midpoint grid.

    The grid covers x in [-2, 2] and y in [-3, 3].  A cell counts when its centre satisfies
    |x| <= 2 and y^2 <= 9 - z^2.

    Args:
        fixed_z: Value of z at which the section is measured.

    Returns:
        The measured area of the section.
    """
    step_across_x = CYLINDER_LENGTH / SECTION_CELL_COUNT_ACROSS_X
    step_across_y = 2.0 * RADIUS / SECTION_CELL_COUNT_ACROSS_Y
    centres_across_x = -HALF_LENGTH + step_across_x * (np.arange(SECTION_CELL_COUNT_ACROSS_X) + 0.5)
    centres_across_y = -RADIUS + step_across_y * (np.arange(SECTION_CELL_COUNT_ACROSS_Y) + 0.5)
    grid_x, grid_y = np.meshgrid(centres_across_x, centres_across_y, indexing="ij")
    inside = grid_y**2 <= RADIUS**2 - fixed_z * fixed_z
    return float(np.count_nonzero(inside)) * step_across_x * step_across_y


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


def order_dy_dx_dz(integrand, follow_cylinder: bool = True) -> float:
    """Return the iterated integral with the order dy dx dz.

    The inner integral runs over y, the middle integral runs over x, and the outer integral
    runs over z.

    Args:
        integrand: Function of (x, y, z).
        follow_cylinder: When True, the inner limits are the two halves of the cylinder at
            the fixed value of z.  When False, the inner limits are the constants -3 and 3.

    Returns:
        The value of the iterated integral.
    """
    def integral_over_y(fixed_z: float, fixed_x: float) -> float:
        if follow_cylinder:
            half_width = rectangle_half_width(fixed_z)
        else:
            half_width = RADIUS
        return integrate_once(lambda y: integrand(fixed_x, y, fixed_z),
                              -half_width, half_width)

    def integral_over_x(fixed_z: float) -> float:
        return integrate_once(lambda x: integral_over_y(fixed_z, x), -HALF_LENGTH, HALF_LENGTH)

    return integrate_once(integral_over_x, -RADIUS, RADIUS)


def order_dx_dy_dz(integrand) -> float:
    """Return the iterated integral with the order dx dy dz.

    The inner integral runs over x, the middle integral runs over y, and the outer integral
    runs over z.

    Args:
        integrand: Function of (x, y, z).

    Returns:
        The value of the iterated integral.
    """
    def integral_over_x(fixed_z: float, fixed_y: float) -> float:
        return integrate_once(lambda x: integrand(x, fixed_y, fixed_z), -HALF_LENGTH, HALF_LENGTH)

    def integral_over_y(fixed_z: float) -> float:
        half_width = rectangle_half_width(fixed_z)
        return integrate_once(lambda y: integral_over_x(fixed_z, y), -half_width, half_width)

    return integrate_once(integral_over_y, -RADIUS, RADIUS)


def integral_of_z_squared() -> float:
    """Return the integral of z^2 over E with a single integral over z.

    The integral is the integral over z of z^2 times the section area 8*sqrt(9 - z^2).
    """
    value, _ = integrate.quad(
        lambda z: z * z * 2.0 * CYLINDER_LENGTH * math.sqrt(max(RADIUS**2 - z * z, 0.0)),
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
    """Run every check of Part 4 and write the record."""
    results: list[dict[str, object]] = []

    for fixed_z in (-3.0, -2.0, 0.0, 1.5, 3.0):
        half_width = rectangle_half_width(fixed_z)
        corners = corners_of_section(fixed_z)
        print(f"z = {fixed_z:+.1f}: half width = {half_width:.12f}, "
              f"corners = {[(round(x, 6), round(y, 6)) for x, y in corners]}")
        measured_area = section_area_by_grid(fixed_z)
        expected_area = 2.0 * CYLINDER_LENGTH * half_width
        record(results, f"section area at z = {fixed_z:+.1f} against 8*sqrt(9 - z^2)",
               measured_area, expected_area, GRID_AREA_TOLERANCE)

    print("shape record: z = -2.0 and z = +1.5 give a rectangle; z = -3.0 and z = +3.0 give "
          "the segment [-2, 2] on the line y = 0")

    for fixed_value in (0.0, 1.5, 2.25):
        area_across_z = section_area_by_grid(fixed_value)
        half_width_as_y = math.sqrt(max(RADIUS**2 - fixed_value * fixed_value, 0.0))
        area_across_y = 2.0 * CYLINDER_LENGTH * half_width_as_y
        record(results, f"section area at z = {fixed_value:+.2f} against the section area at "
                        f"y = {fixed_value:+.2f}",
               area_across_z, area_across_y, GRID_AREA_TOLERANCE)

    exact_quadratic = EXACT_VOLUME + integral_of_z_squared()
    print(f"integral of z^2 over E = {integral_of_z_squared():.12f}")
    record(results, "integral of z^2 over E against 81*pi", integral_of_z_squared(),
           81.0 * math.pi, 1e-6)

    volume_dy_dx_dz = order_dy_dx_dz(lambda x, y, z: 1.0)
    volume_dx_dy_dz = order_dx_dy_dz(lambda x, y, z: 1.0)
    record(results, "order dy dx dz against 36*pi for f = 1", volume_dy_dx_dz, EXACT_VOLUME, 1e-6)
    record(results, "order dx dy dz against 36*pi for f = 1", volume_dx_dy_dz, EXACT_VOLUME, 1e-6)
    record(results, "the two orders with z outer agree for f = 1",
           volume_dy_dx_dz, volume_dx_dy_dz, 1e-8)

    value_dy_dx_dz = order_dy_dx_dz(lambda x, y, z: 1.0 + x + z * z)
    value_dx_dy_dz = order_dx_dy_dz(lambda x, y, z: 1.0 + x + z * z)
    record(results, "order dy dx dz against 117*pi for f = 1 + x + z^2",
           value_dy_dx_dz, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "order dx dy dz against 117*pi for f = 1 + x + z^2",
           value_dx_dy_dz, exact_quadratic, 1e-6 * exact_quadratic)
    record(results, "the two orders with z outer agree for f = 1 + x + z^2",
           value_dy_dx_dz, value_dx_dy_dz, 1e-6 * exact_quadratic)

    wrong_limits_value = order_dy_dx_dz(lambda x, y, z: 1.0, follow_cylinder=False)
    box_volume = CYLINDER_LENGTH * (2.0 * RADIUS) * (2.0 * RADIUS)
    print(f"order dy dx dz with y from -3 to 3 gives {wrong_limits_value:.6f}")
    print(f"distance of that value to 36*pi = {abs(wrong_limits_value - EXACT_VOLUME):.6f}")
    if abs(wrong_limits_value - EXACT_VOLUME) < 20.0:
        raise AssertionError("the negative control does not separate the two limit sets")
    results.append({
        "label": "negative control: y from -3 to 3 is not the rectangle bound",
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
