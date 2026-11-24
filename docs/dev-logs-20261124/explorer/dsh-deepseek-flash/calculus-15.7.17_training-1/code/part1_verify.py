"""Verify the three geometric facts about the solid E.

The solid E has the paraboloid x = 4 y^2 + 4 z^2 as its lower surface and the plane x = 4 as its
upper surface. The script checks the vertex, the intersection circle, and the projection disk.
"""

from __future__ import annotations

import numpy as np

PARABOLOID_FACTOR = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_X = 4.0
"""Coordinate x of the plane that closes the solid."""

INTERSECTION_RADIUS = 1.0
"""Radius in the yz-plane of the circle where the two surfaces meet."""

ZERO_TOLERANCE = 1.0e-12
"""Absolute tolerance for a residual that must vanish."""

AREA_TOLERANCE = 1.0e-2
"""Absolute tolerance for the Monte Carlo estimate of an area."""

RANDOM_SEED = 20261122
"""Seed of the random point sets of the membership test."""

NUMBER_OF_SAMPLES = 2_000_000
"""Number of random points in each membership test."""


def check(name: str, computed: float, expected: float, tolerance: float) -> bool:
    """Print one checked value and its expected value.

    Args:
        name: Short name of the checked fact.
        computed: Value that the script computed.
        expected: Value that the reasoning predicts.
        tolerance: Largest accepted absolute difference.

    Returns:
        True when the absolute difference is at most the tolerance.
    """
    difference = abs(computed - expected)
    passed = difference <= tolerance
    print(f"[{'PASS' if passed else 'FAIL'}] {name}")
    print(f"       computed   = {computed!r}")
    print(f"       expected   = {expected!r}")
    print(f"       difference = {difference:.3e}   tolerance = {tolerance:.1e}")
    return passed


def main() -> int:
    """Run the three geometric checks.

    Returns:
        The number of failed checks.
    """
    failures = 0
    print("Part 1: geometry of the solid E")
    print(f"paraboloid x = {PARABOLOID_FACTOR:g} (y^2 + z^2), plane x = {PLANE_X:g}")
    print("")

    # Fact 1. The paraboloid opens in the positive x direction and touches the origin once.
    axis = np.linspace(-1.2, 1.2, 401)
    y_grid, z_grid = np.meshgrid(axis, axis)
    surface_x = PARABOLOID_FACTOR * (y_grid**2 + z_grid**2)
    least_x = float(surface_x.min())
    number_of_lowest_points = int(np.count_nonzero(surface_x <= ZERO_TOLERANCE))
    print("Fact 1: least value of x on the paraboloid")
    failures += not check("least x on the paraboloid", least_x, 0.0, ZERO_TOLERANCE)
    failures += not check("number of points with x = 0", float(number_of_lowest_points), 1.0, 0.0)
    print("")

    # Fact 2. The two surfaces meet where 4 (y^2 + z^2) = 4.
    radius_from_equation = float(np.sqrt(PLANE_X / PARABOLOID_FACTOR))
    print("Fact 2: intersection of the paraboloid and the plane")
    failures += not check(
        "radius from 4 r^2 = 4", radius_from_equation, INTERSECTION_RADIUS, ZERO_TOLERANCE
    )
    angles = np.linspace(0.0, 2.0 * np.pi, 720, endpoint=False)
    residual = PARABOLOID_FACTOR * (np.cos(angles) ** 2 + np.sin(angles) ** 2) - PLANE_X
    failures += not check(
        "largest |4 r^2 - 4| on the circle r = 1", float(np.abs(residual).max()), 0.0,
        ZERO_TOLERANCE,
    )
    gap_inside = abs(PARABOLOID_FACTOR * 0.98**2 - PLANE_X)
    gap_outside = abs(PARABOLOID_FACTOR * 1.02**2 - PLANE_X)
    failures += not check("|4 r^2 - 4| at r = 0.98", gap_inside, 0.1584, 1.0e-12)
    failures += not check("|4 r^2 - 4| at r = 1.02", gap_outside, 0.1616, 1.0e-12)
    print("")

    # Fact 3. The projection of E on the yz-plane is the unit disk.
    generator = np.random.default_rng(RANDOM_SEED)
    sample_y = generator.uniform(-1.1, 1.1, NUMBER_OF_SAMPLES)
    sample_z = generator.uniform(-1.1, 1.1, NUMBER_OF_SAMPLES)
    radius_squared = sample_y**2 + sample_z**2
    inside_disk = radius_squared <= 1.0
    box_area = 2.2 * 2.2
    measured_area = box_area * float(inside_disk.mean())
    print("Fact 3: projection of E on the yz-plane")
    failures += not check("area of the unit disk", measured_area, float(np.pi), AREA_TOLERANCE)

    sample_x = generator.uniform(0.0, PLANE_X, NUMBER_OF_SAMPLES)
    in_solid = (sample_x >= PARABOLOID_FACTOR * radius_squared) & (sample_x <= PLANE_X)
    on_analytic_region = (radius_squared <= 1.0) & (sample_x >= PARABOLOID_FACTOR * radius_squared)
    disagreements = int(np.count_nonzero(in_solid != on_analytic_region))
    failures += not check("points where the two descriptions differ", float(disagreements), 0.0, 0.0)
    print(f"       sampled points in E: {int(in_solid.sum())}")
    print(f"       Monte Carlo standard error of the area: "
          f"{box_area * float(inside_disk.std()) / np.sqrt(NUMBER_OF_SAMPLES):.4e}")
    print("")

    print(f"checks failed: {failures}")
    return failures


if __name__ == "__main__":
    raise SystemExit(main())
