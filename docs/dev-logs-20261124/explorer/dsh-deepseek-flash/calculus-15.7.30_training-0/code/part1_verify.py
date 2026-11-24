"""Verify the inequality description, the volume, and the projections of the solid E.

Exercise 30 of Section 15.7 gives three surfaces: the cylinder y^2 + z^2 = 9 and the planes
x = -2 and x = 2.  The solid E is the part of the cylinder that the two planes bound.  This
script checks four claims.

1.  The solid is the set {|x| <= 2 and y^2 + z^2 <= 9}, and each of the three surfaces is part
    of the boundary of that set.
2.  The volume of E is 36*pi.  Four independent methods compute the volume.
3.  The section of E at a fixed x is the full disk of radius 3 when |x| <= 2, and it is empty
    when |x| > 2.
4.  The three coordinate projections of E are the disk y^2 + z^2 <= 9 and the two rectangles
    [-2, 2] x [-3, 3].

Run this script with the interpreter of `code/.venv`.  Every comparison prints the computed
value, the expected value, the difference, and the tolerance.  The script raises
`AssertionError` when a comparison fails, and it writes `code/results/part1_results.json`.
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
"""Volume of E by the closed form: disk area times cylinder length, thus 36*pi."""

BOUNDING_BOX_VOLUME = CYLINDER_LENGTH * (2.0 * RADIUS) * (2.0 * RADIUS)
"""Volume of the box [-2, 2] x [-3, 3] x [-3, 3], used by the Monte Carlo method."""

RANDOM_SEED = 20261122
"""Seed of every random sample of this script."""

GRID_CELL_COUNT = 1200
"""Number of cells on one side of the midpoint grid of a section."""

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "part1_results.json"
"""Path of the machine-readable record of the checks."""


def is_inside_solid(x: float, y: float, z: float) -> bool:
    """Return True when the point (x, y, z) lies in the solid E.

    Args:
        x: Coordinate along the axis of the cylinder.
        y: First coordinate across the cylinder.
        z: Second coordinate across the cylinder.

    Returns:
        True when |x| <= 2 and y^2 + z^2 <= 9.
    """
    return abs(x) <= HALF_LENGTH and y * y + z * z <= RADIUS * RADIUS


def volume_by_closed_form() -> float:
    """Return the volume as the area of the disk times the distance between the planes."""
    return math.pi * RADIUS**2 * CYLINDER_LENGTH


def volume_by_slice_quadrature() -> float:
    """Return the volume as the integral over y of the section area 8*sqrt(9 - y^2).

    The section area used here comes from Part 3, which derives the rectangle at a fixed
    value of y.  The route is independent of the triple quadrature below.
    """
    integrand = lambda y: 2.0 * CYLINDER_LENGTH * math.sqrt(max(RADIUS**2 - y * y, 0.0))
    value, _ = integrate.quad(integrand, -RADIUS, RADIUS, limit=400)
    return float(value)


def volume_by_triple_quadrature() -> float:
    """Return the volume with the order dz dy dx that Part 2 derives."""
    value, _ = integrate.tplquad(
        lambda z, y, x: 1.0,
        -HALF_LENGTH,
        HALF_LENGTH,
        lambda x: -RADIUS,
        lambda x: RADIUS,
        lambda x, y: -math.sqrt(max(RADIUS**2 - y * y, 0.0)),
        lambda x, y: math.sqrt(max(RADIUS**2 - y * y, 0.0)),
        epsabs=1e-11,
        epsrel=1e-11,
    )
    return float(value)


def volume_by_monte_carlo(sample_count: int) -> tuple[float, float]:
    """Return a Monte Carlo estimate of the volume and its standard error.

    Args:
        sample_count: Number of independent uniform points in the bounding box.

    Returns:
        The estimate and one standard error of the estimate.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    unit_points = generator.uniform(-1.0, 1.0, size=(sample_count, 3))
    points = unit_points * np.array([HALF_LENGTH, RADIUS, RADIUS])
    inside = points[:, 1] ** 2 + points[:, 2] ** 2 <= RADIUS * RADIUS
    fraction = float(np.count_nonzero(inside)) / float(sample_count)
    estimate = fraction * BOUNDING_BOX_VOLUME
    standard_error = BOUNDING_BOX_VOLUME * math.sqrt(fraction * (1.0 - fraction) / sample_count)
    return estimate, standard_error


def section_area_by_grid(abscissa: float) -> float:
    """Return the area of the section at x = abscissa, measured on a midpoint grid.

    The grid covers the square [-3, 3] x [-3, 3] in the plane x = abscissa.  The area is the
    number of cells whose centre lies in E times the cell area.  The error is proportional to
    the cell size times the perimeter of the disk, thus below 0.1 square units.

    Args:
        abscissa: Value of x at which the section is measured.

    Returns:
        The measured area of the section.
    """
    cell_size = 2.0 * RADIUS / GRID_CELL_COUNT
    centres = -RADIUS + cell_size * (np.arange(GRID_CELL_COUNT) + 0.5)
    first_axis, second_axis = np.meshgrid(centres, centres, indexing="ij")
    inside = (first_axis**2 + second_axis**2 <= RADIUS * RADIUS) & (abs(abscissa) <= HALF_LENGTH)
    return float(np.count_nonzero(inside)) * cell_size * cell_size


def lift_exists(dropped_axis: str, first: float, second: float) -> bool:
    """Return True when some point of E projects to the pair (first, second).

    The search samples the kept coordinate on a grid of 161 values between -3 and 3, and it
    returns True as soon as one sample lies in E.

    Args:
        dropped_axis: Name of the coordinate that the projection drops: "x", "y", or "z".
        first: First kept coordinate of the projected pair.
        second: Second kept coordinate of the projected pair.

    Returns:
        True when the pair has a lift in E.
    """
    candidates = np.linspace(-RADIUS, RADIUS, 161)
    for candidate in candidates:
        if dropped_axis == "x":
            point = (float(candidate), first, second)
        elif dropped_axis == "y":
            point = (first, float(candidate), second)
        else:
            point = (first, second, float(candidate))
        if is_inside_solid(*point):
            return True
    return False


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
    """Run every check of Part 1 and write the record."""
    results: list[dict[str, object]] = []

    closed_form = volume_by_closed_form()
    slice_value = volume_by_slice_quadrature()
    triple_value = volume_by_triple_quadrature()
    estimate, standard_error = volume_by_monte_carlo(400_000)

    print(f"closed form volume = {closed_form:.12f}")
    print(f"slice quadrature volume = {slice_value:.12f}")
    print(f"triple quadrature volume = {triple_value:.12f}")
    print(f"Monte Carlo volume = {estimate:.12f} standard error = {standard_error:.6f}")

    record(results, "volume: slice quadrature against closed form", slice_value, closed_form, 1e-8)
    record(results, "volume: triple quadrature against closed form", triple_value, closed_form, 1e-6)
    record(results, "volume: Monte Carlo against closed form, three standard errors",
           estimate, closed_form, 3.0 * standard_error)

    for abscissa in (-2.0, -0.5, 0.0, 1.5, 2.0):
        measured = section_area_by_grid(abscissa)
        record(results, f"section area at x = {abscissa:+.1f} against 9*pi",
               measured, math.pi * RADIUS**2, 0.25)

    for abscissa in (-2.2, 2.2):
        measured = section_area_by_grid(abscissa)
        record(results, f"section area at x = {abscissa:+.1f} against 0", measured, 0.0, 1e-12)

    boundary_probes = [
        ("cylinder point scaled by 0.999", (0.0, 2.1213203435596424 * 0.999,
                                            2.1213203435596424 * 0.999), True),
        ("cylinder point scaled by 1.001", (0.0, 2.1213203435596424 * 1.001,
                                            2.1213203435596424 * 1.001), False),
        ("plane point (2.0, 0, 0)", (2.0, 0.0, 0.0), True),
        ("plane point (2.001, 0, 0)", (2.001, 0.0, 0.0), False),
        ("centre point", (0.0, 0.0, 0.0), True),
        ("outside corner", (2.5, 2.5, 2.5), False),
    ]
    for label, point, expected_membership in boundary_probes:
        measured = is_inside_solid(*point)
        print(f"membership of {label}: {measured} expected {expected_membership}")
        if measured != expected_membership:
            raise AssertionError(f"membership of {label} is {measured}")
        results.append({
            "label": f"membership: {label}",
            "computed": float(measured),
            "expected": float(expected_membership),
            "difference": 0.0,
            "tolerance": 0.0,
            "passed": True,
        })

    generator = np.random.default_rng(RANDOM_SEED)
    pair_count = 3000
    yz_pairs = generator.uniform(-RADIUS, RADIUS, size=(pair_count, 2))
    xy_pairs = np.column_stack((
        generator.uniform(-HALF_LENGTH - 1.0, HALF_LENGTH + 1.0, size=pair_count),
        generator.uniform(-RADIUS - 0.5, RADIUS + 0.5, size=pair_count),
    ))
    xz_pairs = np.column_stack((
        generator.uniform(-HALF_LENGTH - 1.0, HALF_LENGTH + 1.0, size=pair_count),
        generator.uniform(-RADIUS - 0.5, RADIUS + 0.5, size=pair_count),
    ))

    mismatches_yz = sum(
        (first * first + second * second <= RADIUS * RADIUS) != lift_exists("x", float(first), float(second))
        for first, second in yz_pairs
    )
    mismatches_xy = sum(
        (abs(first) <= HALF_LENGTH and abs(second) <= RADIUS) != lift_exists("z", float(first), float(second))
        for first, second in xy_pairs
    )
    mismatches_xz = sum(
        (abs(first) <= HALF_LENGTH and abs(second) <= RADIUS) != lift_exists("y", float(first), float(second))
        for first, second in xz_pairs
    )
    print(f"projection mismatches: yz {mismatches_yz}, xy {mismatches_xy}, xz {mismatches_xz} "
          f"out of {pair_count} pairs each")
    for label, mismatches in (("yz projection on the plane x = 0", mismatches_yz),
                              ("xy projection on the plane z = 0", mismatches_xy),
                              ("xz projection on the plane y = 0", mismatches_xz)):
        record(results, f"{label}: sampled lift search against the closed criterion",
               float(mismatches), 0.0, 0.0)

    print("corners of the yz projection (disk radius 3): the disk has no corners")
    print("corners of the xy projection: (-2, -3), (2, -3), (2, 3), (-2, 3)")
    print("corners of the xz projection: (-2, -3), (2, -3), (2, 3), (-2, 3)")

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_PATH}")


if __name__ == "__main__":
    main()
