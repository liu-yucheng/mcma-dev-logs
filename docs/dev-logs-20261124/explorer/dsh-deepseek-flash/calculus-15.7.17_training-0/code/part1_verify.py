"""Verify the geometry of the solid region E of the problem.

The region E is bounded by the paraboloid x = 4*y^2 + 4*z^2 and by the plane x = 4.
This module checks four facts that the tutorial states in Part 1:

1. the two surfaces meet on the circle y^2 + z^2 = 1 in the plane x = 4;
2. the projection of E onto the yz plane is the closed unit disk;
3. the segment 4*(y^2 + z^2) <= x <= 4 is nonempty exactly on that disk;
4. the region is rotationally symmetric about the x axis.

Every check prints the computed value, the expected value, and the verdict.
"""

from __future__ import annotations

import math

import numpy as np

PARABOLOID_COEFFICIENT: float = 4.0
"""Coefficient of y^2 + z^2 in the equation of the paraboloid."""

PLANE_POSITION: float = 4.0
"""Position of the flat boundary plane x = PLANE_POSITION."""

INTERSECTION_RADIUS: float = 1.0
"""Radius of the circle where the paraboloid meets the plane."""

TOLERANCE: float = 1.0e-12
"""Absolute tolerance for a comparison of two floating point numbers."""

RANDOM_SEED: int = 20261122
"""Seed of the pseudo random generator that this module uses."""


def paraboloid_height(y_coordinate: float, z_coordinate: float) -> float:
    """Return the x coordinate of the paraboloid above the point (y, z).

    Args:
        y_coordinate: The y coordinate of a point of the yz plane.
        z_coordinate: The z coordinate of a point of the yz plane.

    Returns:
        The value 4*(y^2 + z^2), which is the smallest x of the region above (y, z).
    """
    return PARABOLOID_COEFFICIENT * (y_coordinate**2 + z_coordinate**2)


def radial_distance(y_coordinate: float, z_coordinate: float) -> float:
    """Return the distance of the point (y, z) from the x axis.

    Args:
        y_coordinate: The y coordinate of a point of the yz plane.
        z_coordinate: The z coordinate of a point of the yz plane.

    Returns:
        The nonnegative value sqrt(y^2 + z^2).
    """
    return math.hypot(y_coordinate, z_coordinate)


def is_inside_region(x_coordinate: float, y_coordinate: float, z_coordinate: float) -> bool:
    """Report whether a point belongs to the solid region E.

    Args:
        x_coordinate: The x coordinate of the point.
        y_coordinate: The y coordinate of the point.
        z_coordinate: The z coordinate of the point.

    Returns:
        True when 4*(y^2 + z^2) <= x <= 4, and False otherwise.
    """
    lower_bound = paraboloid_height(y_coordinate, z_coordinate)
    return lower_bound <= x_coordinate <= PLANE_POSITION


def segment_length(y_coordinate: float, z_coordinate: float) -> float:
    """Return the length of the vertical segment of E above the point (y, z).

    Args:
        y_coordinate: The y coordinate of a point of the yz plane.
        z_coordinate: The z coordinate of a point of the yz plane.

    Returns:
        The length 4 - 4*(y^2 + z^2) when it is positive, and 0 otherwise.
    """
    return max(0.0, PLANE_POSITION - paraboloid_height(y_coordinate, z_coordinate))


def report(check_name: str, computed_value: float, expected_value: float, tolerance: float) -> bool:
    """Print one comparison and return its verdict.

    Args:
        check_name: A short name of the checked fact.
        computed_value: The value that the computation produced.
        expected_value: The value that the tutorial states.
        tolerance: The largest accepted absolute difference.

    Returns:
        True when the difference is within the tolerance, and False otherwise.
    """
    difference = abs(computed_value - expected_value)
    verdict = "PASS" if difference <= tolerance else "FAIL"
    print(f"{check_name:<52} computed={computed_value: .12f} expected={expected_value: .12f} "
          f"difference={difference:.3e} {verdict}")
    return verdict == "PASS"


def check_intersection_circle() -> bool:
    """Check that the two surfaces meet exactly on the circle of radius 1.

    Returns:
        True when every check passes.
    """
    all_passed = True
    all_passed &= report(
        "paraboloid height at radius 1 equals 4",
        paraboloid_height(INTERSECTION_RADIUS, 0.0),
        PLANE_POSITION,
        TOLERANCE,
    )
    all_passed &= report(
        "paraboloid height at radius 0.5 is 1",
        paraboloid_height(0.5, 0.0),
        1.0,
        TOLERANCE,
    )
    boundary_points = [(INTERSECTION_RADIUS * math.cos(t), INTERSECTION_RADIUS * math.sin(t))
                       for t in np.linspace(0.0, 2.0 * math.pi, 17)[:-1]]
    worst_gap = max(abs(paraboloid_height(y_value, z_value) - PLANE_POSITION)
                    for y_value, z_value in boundary_points)
    all_passed &= report("largest height gap on the circle of radius 1", worst_gap, 0.0, 1.0e-12)
    inner_height = paraboloid_height(0.99, 0.0)
    outer_height = paraboloid_height(1.01, 0.0)
    print(f"{'height at radius 0.99 is below 4':<52} computed={inner_height: .6f} "
          f"expected<4.0 {'PASS' if inner_height < PLANE_POSITION else 'FAIL'}")
    print(f"{'height at radius 1.01 is above 4':<52} computed={outer_height: .6f} "
          f"expected>4.0 {'PASS' if outer_height > PLANE_POSITION else 'FAIL'}")
    all_passed &= bool(inner_height < PLANE_POSITION and outer_height > PLANE_POSITION)
    return all_passed


def check_projection_is_unit_disk() -> bool:
    """Check that the projection of E onto the yz plane is the closed unit disk.

    Returns:
        True when every check passes.
    """
    generator = np.random.default_rng(RANDOM_SEED)
    sample_count = 200000
    y_values = generator.uniform(-1.4, 1.4, sample_count)
    z_values = generator.uniform(-1.4, 1.4, sample_count)
    radii = np.hypot(y_values, z_values)
    lengths = np.maximum(0.0, PLANE_POSITION - PARABOLOID_COEFFICIENT * radii**2)
    inside_sample = radii <= INTERSECTION_RADIUS
    positive_sample = lengths > 0.0
    agreement = float(np.mean(inside_sample == positive_sample))
    return report("random points: nonempty segment iff radius <= 1", agreement, 1.0, 1.0e-12)


def check_region_volume_by_counting() -> bool:
    """Check the volume of E against the closed form 2*pi by a Monte Carlo count.

    Returns:
        True when the counted volume agrees with 2*pi within the statistical error.
    """
    generator = np.random.default_rng(RANDOM_SEED + 1)
    sample_count = 2000000
    y_values = generator.uniform(-1.0, 1.0, sample_count)
    z_values = generator.uniform(-1.0, 1.0, sample_count)
    x_values = generator.uniform(0.0, PLANE_POSITION, sample_count)
    lower_bounds = PARABOLOID_COEFFICIENT * (y_values**2 + z_values**2)
    inside = (lower_bounds <= x_values) & (x_values <= PLANE_POSITION)
    box_volume = 2.0 * 2.0 * PLANE_POSITION
    counted_volume = box_volume * float(np.mean(inside))
    statistical_error = box_volume * math.sqrt(float(np.mean(inside)) *
                                               (1.0 - float(np.mean(inside))) / sample_count)
    print(f"{'counted volume of E':<52} computed={counted_volume: .6f} "
          f"expected={2.0 * math.pi: .6f} error={statistical_error:.6f}")
    return abs(counted_volume - 2.0 * math.pi) <= 4.0 * statistical_error


def check_rotational_symmetry() -> bool:
    """Check that a rotation about the x axis keeps a point inside or outside E.

    Returns:
        True when every rotated sample keeps its membership.
    """
    generator = np.random.default_rng(RANDOM_SEED + 2)
    sample_count = 20000
    radii = generator.uniform(0.0, 1.3, sample_count)
    angles = generator.uniform(0.0, 2.0 * math.pi, sample_count)
    x_values = generator.uniform(-0.5, 4.5, sample_count)
    membership_before = np.array([is_inside_region(x_value, radius, 0.0)
                                 for x_value, radius in zip(x_values, radii)])
    membership_after = np.array([is_inside_region(x_value, radius * math.cos(angle),
                                                 radius * math.sin(angle))
                                 for x_value, radius, angle in zip(x_values, radii, angles)])
    agreement = float(np.mean(membership_before == membership_after))
    return report("rotation about the x axis keeps membership", agreement, 1.0, 1.0e-12)


def main() -> int:
    """Run every geometry check of Part 1.

    Returns:
        The process exit status: 0 when every check passes, and 1 otherwise.
    """
    print("Part 1 verification: geometry of the solid region E")
    print(f"Paraboloid x = {PARABOLOID_COEFFICIENT:g}*(y^2 + z^2), plane x = {PLANE_POSITION:g}")
    print("-" * 100)
    results = [
        check_intersection_circle(),
        check_projection_is_unit_disk(),
        check_rotational_symmetry(),
        check_region_volume_by_counting(),
    ]
    print("-" * 100)
    print(f"All Part 1 checks passed: {all(results)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
