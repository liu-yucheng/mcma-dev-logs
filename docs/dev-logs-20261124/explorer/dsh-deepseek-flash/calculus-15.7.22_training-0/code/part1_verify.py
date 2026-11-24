"""Verify the description of the solid of the exercise.

The script checks four claims of Part 1.
The first claim is that the cylinder x^2 + z^2 = 4 has radius 2.
The second claim is that the three inequalities accept the points between the two planes and reject the
points outside that interval.
The third claim is that the vertical thickness above a point (x, z) of the disk is 5 - z.
The fourth claim is that the thickness runs from 3 to 7 over the disk.

The script compares each value that one method computes with a value that a different method
computes. The membership test uses only the three defining inequalities. The thickness formula
uses only the two plane equations, and the scan in y uses only the membership test.
"""

import math
from typing import Final

import numpy as np

RANDOM_SEED: Final[int] = 20261122
"""Seed of the pseudo random number generator of the sampled points."""

SQUARED_RADIUS: Final[float] = 4.0
"""Right side of the cylinder equation x^2 + z^2 = 4."""

GRID_HALF_WIDTH: Final[float] = 2.5
"""Half width of the square grid that covers the disk."""

GRID_POINT_COUNT: Final[int] = 2001
"""Number of grid points on each side of the square grid."""

HEIGHT_SCAN_STEP: Final[float] = 1.0e-3
"""Step of the scan in y that measures the vertical interval."""

SAMPLE_POINT_COUNT: Final[int] = 200
"""Number of random points of the disk that the script tests."""

MEMBERSHIP_POINT_COUNT: Final[int] = 500
"""Number of constructed points of each class in the membership test."""

MEMBERSHIP_MARGIN: Final[float] = 0.05
"""Smallest distance of a rejected point from the top plane or the bottom plane."""

TOLERANCE: Final[float] = 1.0e-12
"""Tolerance of the membership test."""


def is_inside(x_value: float, y_value: float, z_value: float) -> bool:
    """Return True when the point satisfies the three inequalities of the solid."""
    inside_cylinder = x_value * x_value + z_value * z_value <= SQUARED_RADIUS + TOLERANCE
    above_bottom = y_value >= -1.0 - TOLERANCE
    below_top = y_value <= 4.0 - z_value + TOLERANCE
    return bool(inside_cylinder and above_bottom and below_top)


def thickness_formula(z_value: float) -> float:
    """Return the length of the vertical interval above (0, z) from the plane equations."""
    return (4.0 - z_value) - (-1.0)


def scan_vertical_interval(x_value: float, z_value: float) -> tuple[float, float]:
    """Measure the vertical interval above (x, z) with a scan in y.

    Args:
        x_value: First horizontal coordinate of the test point.
        z_value: Second horizontal coordinate of the test point.

    Returns:
        The first and the last height of the scan that lies inside the solid.
    """
    heights = np.arange(-1.5, 7.5 + HEIGHT_SCAN_STEP, HEIGHT_SCAN_STEP)
    measured = np.array([is_inside(x_value, float(height), z_value) for height in heights])
    if not measured.any():
        return (math.nan, math.nan)
    return (float(heights[measured][0]), float(heights[measured][-1]))


def build_membership_samples(
    generator: np.random.Generator, radius: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Build accepted points and rejected points from the two planes alone.

    The accepted points take a height between -1 and 4 - z. The rejected points take a height below
    -1 or above 4 - z, by at least MEMBERSHIP_MARGIN. The horizontal position of every point lies in
    the disk.

    Args:
        generator: Source of the pseudo random numbers.
        radius: Radius of the cylinder.

    Returns:
        The arrays of x, y, and z values of the accepted points followed by the rejected points.
    """
    radii = radius * np.sqrt(generator.random(MEMBERSHIP_POINT_COUNT))
    angles = 2.0 * math.pi * generator.random(MEMBERSHIP_POINT_COUNT)
    sample_x = radii * np.cos(angles)
    sample_z = radii * np.sin(angles)
    bottom = -1.0
    top = 4.0 - sample_z

    inside_y = bottom + (top - bottom) * generator.random(MEMBERSHIP_POINT_COUNT)

    below = generator.random(MEMBERSHIP_POINT_COUNT) < 0.5
    offset = MEMBERSHIP_MARGIN + generator.random(MEMBERSHIP_POINT_COUNT)
    outside_y = np.where(below, bottom - offset, top + offset)

    return (
        np.concatenate([sample_x, sample_x]),
        np.concatenate([inside_y, outside_y]),
        np.concatenate([sample_z, sample_z]),
    )


def main() -> None:
    """Run the four checks of Part 1 and print each computed value with its expected value."""
    generator = np.random.default_rng(RANDOM_SEED)

    axis = np.linspace(-GRID_HALF_WIDTH, GRID_HALF_WIDTH, GRID_POINT_COUNT)
    grid_x, grid_z = np.meshgrid(axis, axis)
    inside_disk = grid_x**2 + grid_z**2 <= SQUARED_RADIUS

    grid_radius = float(np.max(grid_x[inside_disk]))
    root_radius = float(np.max(np.roots([1.0, 0.0, -SQUARED_RADIUS])))
    cell_width = 2.0 * GRID_HALF_WIDTH / (GRID_POINT_COUNT - 1)
    print(f"check 1 radius: grid maximum {grid_radius:.6f}, positive root {root_radius:.6f}")
    assert abs(grid_radius - root_radius) <= 2.0 * cell_width, "the two radius values disagree"

    sample_x, sample_y, sample_z = build_membership_samples(generator, root_radius)
    accepted = np.array(
        [is_inside(float(x), float(y), float(z)) for x, y, z in zip(sample_x, sample_y, sample_z)]
    )
    accepted_count = int(np.count_nonzero(accepted[:MEMBERSHIP_POINT_COUNT]))
    rejected_count = int(np.count_nonzero(accepted[MEMBERSHIP_POINT_COUNT:]))
    print(f"check 2 accepted points: {accepted_count} of {MEMBERSHIP_POINT_COUNT}")
    print(f"check 2 rejected points that pass: {rejected_count} of {MEMBERSHIP_POINT_COUNT}")
    assert accepted_count == MEMBERSHIP_POINT_COUNT, "the inequalities reject an inside point"
    assert rejected_count == 0, "the inequalities accept a point between the planes and outside"

    radii = root_radius * np.sqrt(generator.random(SAMPLE_POINT_COUNT))
    angles = 2.0 * math.pi * generator.random(SAMPLE_POINT_COUNT)
    sample_x = radii * np.cos(angles)
    sample_z = radii * np.sin(angles)

    deviations = []
    for x_value, z_value in zip(sample_x, sample_z):
        low, high = scan_vertical_interval(float(x_value), float(z_value))
        measured_length = high - low + HEIGHT_SCAN_STEP
        deviations.append(abs(measured_length - thickness_formula(float(z_value))))
    largest_deviation = max(deviations)
    print(f"check 3 thickness: {SAMPLE_POINT_COUNT} points, largest deviation {largest_deviation:.6f}")
    print(f"check 3 tolerance: {2.0 * HEIGHT_SCAN_STEP:.6f}")
    assert largest_deviation <= 2.0 * HEIGHT_SCAN_STEP, "the measured interval differs from 5 - z"

    thickness_grid = 5.0 - grid_z[inside_disk]
    smallest_thickness = float(np.min(thickness_grid))
    largest_thickness = float(np.max(thickness_grid))
    expected_smallest = 5.0 - root_radius
    expected_largest = 5.0 + root_radius
    print(f"check 4 smallest thickness: grid {smallest_thickness:.6f}, formula {expected_smallest:.6f}")
    print(f"check 4 largest thickness:  grid {largest_thickness:.6f}, formula {expected_largest:.6f}")
    assert abs(smallest_thickness - expected_smallest) <= 1.0e-9, "the smallest thickness is wrong"
    assert abs(largest_thickness - expected_largest) <= 1.0e-9, "the largest thickness is wrong"
    assert smallest_thickness > 0.0, "the vertical interval is empty at one point"

    print("part 1: all checks passed")


if __name__ == "__main__":
    main()
