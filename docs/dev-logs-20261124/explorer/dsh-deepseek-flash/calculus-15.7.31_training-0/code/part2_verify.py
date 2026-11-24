"""Verify the three families of cross sections of the solid E of Stewart 15.7 Exercise 31.

Each cross section is derived from the defining inequalities, not from a drawing.  The area of each
section is computed in two ways: from the corner list by the shoelace formula, and from the
inequality bounds by one-dimensional quadrature.  Each family is sampled at three heights, and the
three slab integrals must reproduce the volume 128/15.

Run this script with the interpreter of ``code/.venv``.  It prints each checked value beside the
value that an independent method gives, and it writes the records to
``code/results/part2_results.json``.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

from scipy.integrate import quad

WORKSPACE = Path(__file__).resolve().parent.parent
"""Root of the problem workspace."""

RESULTS_DIRECTORY = WORKSPACE / "code" / "results"
"""Directory of the recorded checks."""

TOLERANCE = 1.0e-9
"""Absolute tolerance of a numeric comparison."""

EXACT_VOLUME = Fraction(128, 15)
"""Volume of the solid, computed in Part 1."""

PROBE_HEIGHTS_X = (0.0, 1.0, 1.9)
"""Three heights of the section at a fixed x."""

PROBE_HEIGHTS_Y = (0.5, 2.0, 3.5)
"""Three heights of the section at a fixed y."""

PROBE_HEIGHTS_Z = (0.0, 1.0, 1.5)
"""Three heights of the section at a fixed z."""


def polygon_area(corners: list[tuple[float, float]]) -> float:
    """Return the area of one polygon from its corner list by the shoelace formula.

    Args:
        corners: The corners in order along the boundary.

    Returns:
        The absolute area of the polygon.
    """
    total = 0.0
    for index, corner in enumerate(corners):
        next_corner = corners[(index + 1) % len(corners)]
        total += corner[0] * next_corner[1] - next_corner[0] * corner[1]
    return abs(total) / 2.0


def distinct_corner_count(corners: list[tuple[float, float]]) -> int:
    """Return the number of distinct corners of one polygon.

    Args:
        corners: The corners of the polygon.

    Returns:
        The number of distinct corners, with a tolerance of 1.0e-12 on each coordinate.
    """
    distinct: list[tuple[float, float]] = []
    for corner in corners:
        if not any(abs(corner[0] - other[0]) < 1.0e-12 and abs(corner[1] - other[1]) < 1.0e-12
                   for other in distinct):
            distinct.append(corner)
    return len(distinct)


def triangle_corners(x_value: float) -> list[tuple[float, float]]:
    """Return the corners of the section at a fixed x in the coordinates (y, z).

    Args:
        x_value: The fixed value of x.

    Returns:
        The three corners of the triangle, or three equal corners at a boundary value.
    """
    low = x_value * x_value
    return [(low, 0.0), (4.0, 0.0), (low, (4.0 - low) / 2.0)]


def triangle_area_by_integral(x_value: float) -> float:
    """Return the area of the section at a fixed x from the inequality bounds.

    Args:
        x_value: The fixed value of x.

    Returns:
        The area of the section.
    """
    value, _ = quad(lambda y_value: (4.0 - y_value) / 2.0, x_value * x_value, 4.0,
                    epsabs=1.0e-14, epsrel=1.0e-13)
    return value


def rectangle_corners(y_value: float) -> list[tuple[float, float]]:
    """Return the corners of the section at a fixed y in the coordinates (x, z).

    Args:
        y_value: The fixed value of y.

    Returns:
        The four corners of the rectangle, or a degenerate list at a boundary value.
    """
    half_width = math.sqrt(y_value)
    height = (4.0 - y_value) / 2.0
    return [(-half_width, 0.0), (half_width, 0.0), (half_width, height), (-half_width, height)]


def rectangle_area_by_bounds(y_value: float) -> float:
    """Return the area of the section at a fixed y from the inequality bounds.

    Args:
        y_value: The fixed value of y.

    Returns:
        The area of the section.
    """
    width, _ = quad(lambda x_value: 1.0, -math.sqrt(y_value), math.sqrt(y_value),
                    epsabs=1.0e-14, epsrel=1.0e-13)
    height, _ = quad(lambda z_value: 1.0, 0.0, (4.0 - y_value) / 2.0,
                     epsabs=1.0e-14, epsrel=1.0e-13)
    return width * height


def cap_corners(z_value: float) -> list[tuple[float, float]]:
    """Return the corners of the section at a fixed z in the coordinates (x, y).

    The section is a parabolic segment.  Its apex is (0, 0) and its two upper corners are
    (minus the half width, cap) and (the half width, cap).

    Args:
        z_value: The fixed value of z.

    Returns:
        The three named corners of the segment.
    """
    cap = 4.0 - 2.0 * z_value
    half_width = math.sqrt(max(cap, 0.0))
    return [(-half_width, cap), (0.0, 0.0), (half_width, cap)]


def cap_area_by_integral(z_value: float) -> float:
    """Return the area of the parabolic segment at a fixed z from the inequality bounds.

    Args:
        z_value: The fixed value of z.

    Returns:
        The area of the section.
    """
    cap = 4.0 - 2.0 * z_value
    half_width = math.sqrt(max(cap, 0.0))
    value, _ = quad(lambda x_value: cap - x_value * x_value, -half_width, half_width,
                    epsabs=1.0e-14, epsrel=1.0e-13)
    return value


def cap_area_closed_form(z_value: float) -> float:
    """Return the area of the parabolic segment from the closed form four thirds of a cubed.

    Args:
        z_value: The fixed value of z.

    Returns:
        The area of the section.
    """
    half_width = math.sqrt(max(4.0 - 2.0 * z_value, 0.0))
    return 4.0 / 3.0 * half_width ** 3


def main() -> None:
    """Run every check of Part 2, print the values, and write the result records."""
    records: list[dict[str, float | str]] = []

    print("=== Part 2: the three families of cross sections ===")
    print()
    print("section at a fixed x, coordinates (y, z)")
    for x_value in PROBE_HEIGHTS_X:
        corners = triangle_corners(x_value)
        shoelace = polygon_area(corners)
        integral = triangle_area_by_integral(x_value)
        print(f"  x = {x_value:4.2f}  corners {[(round(a, 6), round(b, 6)) for a, b in corners]}")
        print(f"           shoelace {shoelace:.12f}  integral {integral:.12f}  "
              f"difference {abs(shoelace - integral):.3e}  distinct {distinct_corner_count(corners)}")
        records.append({
            "label": f"Area at fixed $x = {x_value:g}$: shoelace against the bound integral",
            "computed": shoelace,
            "expected": integral,
            "difference": abs(shoelace - integral),
            "tolerance": TOLERANCE,
        })
    print()

    print("section at a fixed y, coordinates (x, z)")
    for y_value in PROBE_HEIGHTS_Y:
        corners = rectangle_corners(y_value)
        shoelace = polygon_area(corners)
        from_bounds = rectangle_area_by_bounds(y_value)
        print(f"  y = {y_value:4.2f}  corners {[(round(a, 6), round(b, 6)) for a, b in corners]}")
        print(f"           shoelace {shoelace:.12f}  bounds {from_bounds:.12f}  "
              f"difference {abs(shoelace - from_bounds):.3e}  distinct {distinct_corner_count(corners)}")
        records.append({
            "label": f"Area at fixed $y = {y_value:g}$: shoelace against the bound integral",
            "computed": shoelace,
            "expected": from_bounds,
            "difference": abs(shoelace - from_bounds),
            "tolerance": TOLERANCE,
        })
    print()

    print("section at a fixed z, coordinates (x, y)")
    for z_value in PROBE_HEIGHTS_Z:
        corners = cap_corners(z_value)
        integral = cap_area_by_integral(z_value)
        closed = cap_area_closed_form(z_value)
        print(f"  z = {z_value:4.2f}  corners {[(round(a, 6), round(b, 6)) for a, b in corners]}")
        print(f"           integral {integral:.12f}  closed form {closed:.12f}  "
              f"difference {abs(integral - closed):.3e}  distinct {distinct_corner_count(corners)}")
        records.append({
            "label": f"Area at fixed $z = {z_value:g}$: bound integral against $\\frac{{4}}{{3}}a^3$",
            "computed": integral,
            "expected": closed,
            "difference": abs(integral - closed),
            "tolerance": TOLERANCE,
        })
    print()

    slab_x, _ = quad(lambda x_value: triangle_area_by_integral(x_value), -2.0, 2.0,
                     epsabs=1.0e-11, epsrel=1.0e-12, limit=200)
    slab_y, _ = quad(lambda y_value: rectangle_area_by_bounds(y_value), 0.0, 4.0,
                     epsabs=1.0e-11, epsrel=1.0e-12, limit=200)
    slab_z, _ = quad(lambda z_value: cap_area_by_integral(z_value), 0.0, 2.0,
                     epsabs=1.0e-11, epsrel=1.0e-12, limit=200, points=[2.0])

    exact = float(EXACT_VOLUME)
    print("slab integrals of the three section areas")
    print(f"  integral over x of the triangle area : {slab_x:.12f}")
    print(f"  integral over y of the rectangle area: {slab_y:.12f}")
    print(f"  integral over z of the segment area  : {slab_z:.12f}")
    print(f"  exact volume                         : {exact:.12f}")
    for name, value in (("x", slab_x), ("y", slab_y), ("z", slab_z)):
        records.append({
            "label": f"Slab integral over {name} of the section area against $128/15$",
            "computed": value,
            "expected": exact,
            "difference": abs(value - exact),
            "tolerance": TOLERANCE,
        })

    boundary_x = distinct_corner_count(triangle_corners(2.0))
    boundary_y_zero = distinct_corner_count(rectangle_corners(0.0))
    boundary_y_four = distinct_corner_count(rectangle_corners(4.0))
    boundary_z = distinct_corner_count(cap_corners(2.0))
    print()
    print("degenerate sections at the boundary values")
    print(f"  x = 2   distinct corners {boundary_x}, expected 1 (one point)")
    print(f"  y = 0   distinct corners {boundary_y_zero}, expected 2 (one segment along z)")
    print(f"  y = 4   distinct corners {boundary_y_four}, expected 2 (one segment along x)")
    print(f"  z = 2   distinct corners {boundary_z}, expected 1 (one point)")

    if boundary_x != 1 or boundary_y_zero != 2 or boundary_y_four != 2 or boundary_z != 1:
        raise AssertionError("the degenerate sections do not have the printed corner count")
    for record in records:
        if record["difference"] > record["tolerance"]:
            raise AssertionError(f"check failed: {record['label']}")

    RESULTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
    target = RESULTS_DIRECTORY / "part2_results.json"
    target.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {target}")


if __name__ == "__main__":
    main()
