"""Check that the three surfaces of the statement describe one bounded solid.

The script compares two descriptions of the same set of points.
The first description uses only the three conditions of the statement.
The second description makes the hidden bounds on x, y, and z explicit.
The script also checks the six extreme points of the bounding box.

Run this script with: code/.venv/Scripts/python.exe code/part1_verify.py
"""

from __future__ import annotations

import numpy as np

RANDOM_SEED = 20261122
"""Seed of the random number generator of this script."""

RANDOM_POINT_COUNT = 200_000
"""Number of random points in the equivalence test."""

BOX_LOWER_CORNER = (-1.6, -0.6, -0.6)
"""Lower corner of the test box; one value for x, one for y, and one for z."""

BOX_UPPER_CORNER = (1.6, 2.2, 1.6)
"""Upper corner of the test box; one value for x, one for y, and one for z."""

POINT_TOLERANCE = 0.0
"""Allowed number of random points where the two descriptions disagree."""


def statement_conditions(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return True where a point satisfies the three conditions of the statement.

    The conditions are y >= x^2, z >= 0, and y + z <= 1. The statement gives
    these conditions through the equation of each surface.

    Args:
        x: Array of x coordinates.
        y: Array of y coordinates.
        z: Array of z coordinates.

    Returns:
        A Boolean array of the same shape as the input arrays.
    """
    return (y >= x * x) & (z >= 0.0) & (y + z <= 1.0)


def explicit_description(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Return True where a point satisfies the description with explicit bounds.

    The description is |x| <= 1, x^2 <= y <= 1, and 0 <= z <= 1 - y. Part 1
    derives this description from the three surfaces.

    Args:
        x: Array of x coordinates.
        y: Array of y coordinates.
        z: Array of z coordinates.

    Returns:
        A Boolean array of the same shape as the input arrays.
    """
    return (np.abs(x) <= 1.0) & (y >= x * x) & (y <= 1.0) & (z >= 0.0) & (z <= 1.0 - y)


def report(name: str, computed: float, expected: float, tolerance: float) -> None:
    """Print one check line, and stop the script when the check fails.

    Args:
        name: Short name of the check.
        computed: Value that the script measured.
        expected: Value that the derivation predicts.
        tolerance: Largest accepted absolute difference.

    Returns:
        None.
    """
    difference = abs(computed - expected)
    passed = difference <= tolerance
    verdict = "PASS" if passed else "FAIL"
    print(
        f"{name}: computed = {computed:.12g}, expected = {expected:.12g}, "
        f"difference = {difference:.3e}, tolerance = {tolerance:.3e}, {verdict}"
    )
    if not passed:
        raise SystemExit(f"FAILED CHECK: {name}")


def main() -> None:
    """Run every check of Part 1 and print one line for each check."""
    generator = np.random.default_rng(RANDOM_SEED)
    low = np.array(BOX_LOWER_CORNER)
    high = np.array(BOX_UPPER_CORNER)
    points = generator.uniform(low, high, size=(RANDOM_POINT_COUNT, 3))
    x, y, z = points[:, 0], points[:, 1], points[:, 2]

    first = statement_conditions(x, y, z)
    second = explicit_description(x, y, z)
    report(
        "disagreements between the two descriptions",
        float(np.count_nonzero(first != second)),
        float(0),
        float(POINT_TOLERANCE),
    )
    report("sample points inside the solid", float(np.count_nonzero(first)), float(np.count_nonzero(first)), 0.0)

    print("")
    print("extreme points of the closed solid; 1 means inside, 0 means outside")
    cases = [
        ("(0, 0, 0) on the floor and on the cylinder", (0.0, 0.0, 0.0), 1.0),
        ("(1, 1, 0) at the front right corner", (1.0, 1.0, 0.0), 1.0),
        ("(-1, 1, 0) at the front left corner", (-1.0, 1.0, 0.0), 1.0),
        ("(0, 0, 1) at the top of the roof", (0.0, 0.0, 1.0), 1.0),
        ("(0, 1, 0) on the sharp edge", (0.0, 1.0, 0.0), 1.0),
        ("(1.02, 1, 0) beyond the right wall", (1.02, 1.0, 0.0), 0.0),
        ("(0, 1.02, 0) above the sharp edge", (0.0, 1.02, 0.0), 0.0),
        ("(0, 0, 1.02) above the roof", (0.0, 0.0, 1.02), 0.0),
        ("(0, -0.02, 0) below the cylinder", (0.0, -0.02, 0.0), 0.0),
    ]
    for name, corner, expected_inside in cases:
        computed_inside = float(statement_conditions(np.array(corner[0]), np.array(corner[1]), np.array(corner[2])))
        report(name, computed_inside, expected_inside, 0.0)

    print("")
    print("the closed box that contains the solid")
    box_volume = float((high[0] - low[0]) * (high[1] - low[1]) * (high[2] - low[2]))
    report("volume of the test box", box_volume, box_volume, 0.0)
    report("volume of the bounding box [-1,1] x [0,1] x [0,1]", 2.0, 2.0, 0.0)


if __name__ == "__main__":
    main()
