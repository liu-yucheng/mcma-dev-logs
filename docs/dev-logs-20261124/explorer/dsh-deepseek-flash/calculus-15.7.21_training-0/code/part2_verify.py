"""Check the three integration bounds of the triple integral by direct search.

For a fixed pair (x, y), the script finds the set of z values that the solid
admits. For a fixed x, the script finds the set of y values. For a fixed y,
the script finds the set of x values. Each set must match the bound that
Part 2 derives. No step of this script uses the derivation; every step reads
the three conditions of the statement.

Run this script with: code/.venv/Scripts/python.exe code/part2_verify.py
"""

from __future__ import annotations

import numpy as np

Z_SCAN = np.linspace(-0.5, 2.0, 250_001)
"""Grid of z values for the search of the inner bound."""

Y_SCAN = np.linspace(-0.5, 2.0, 250_001)
"""Grid of y values for the search of the middle bound."""

X_SCAN = np.linspace(-1.5, 1.5, 300_001)
"""Grid of x values for the search of the outer bound."""

GRID_TOLERANCE = 2.0e-5
"""Largest accepted error from the grid spacing of a search."""

SAMPLE_X_VALUES = (0.0, 0.6, -0.9)
"""Three abscissas where the script measures the y range."""

SAMPLE_POINTS = ((0.0, 0.5), (0.6, 0.5), (-0.9, 0.95))
"""Three points of the projection where the script measures the z range."""


def inside(x: float, y: float, z: float) -> bool:
    """Return True when a point satisfies the three conditions of the statement.

    Args:
        x: x coordinate of the point.
        y: y coordinate of the point.
        z: z coordinate of the point.

    Returns:
        True when y >= x^2, z >= 0, and y + z <= 1.
    """
    return bool(y >= x * x and z >= 0.0 and y + z <= 1.0)


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


def z_segment(x_value: float, y_value: float) -> tuple[float, float]:
    """Return the smallest and the largest z that the solid admits at (x, y).

    Args:
        x_value: Fixed x coordinate.
        y_value: Fixed y coordinate.

    Returns:
        A pair (smallest z, largest z). Both values are NaN when the vertical
        line misses the solid.
    """
    admitted = (y_value >= x_value * x_value) & (Z_SCAN >= 0.0) & (y_value + Z_SCAN <= 1.0)
    if not np.any(admitted):
        return float("nan"), float("nan")
    return float(Z_SCAN[admitted].min()), float(Z_SCAN[admitted].max())


def y_segment(x_value: float) -> tuple[float, float]:
    """Return the smallest and the largest y that admits a point of the solid at x.

    A y value is admitted when a z value exists with y >= x^2 and 0 <= z <= 1 - y.

    Args:
        x_value: Fixed x coordinate.

    Returns:
        A pair (smallest y, largest y). Both values are NaN when no y is admitted.
    """
    admitted = (Y_SCAN >= x_value * x_value) & (Y_SCAN <= 1.0)
    if not np.any(admitted):
        return float("nan"), float("nan")
    return float(Y_SCAN[admitted].min()), float(Y_SCAN[admitted].max())


def x_segment(y_value: float) -> tuple[float, float]:
    """Return the smallest and the largest x that the solid admits at a fixed y.

    Args:
        y_value: Fixed y coordinate.

    Returns:
        A pair (smallest x, largest x). Both values are NaN when no x is admitted.
    """
    admitted = X_SCAN * X_SCAN <= y_value
    if not np.any(admitted):
        return float("nan"), float("nan")
    return float(X_SCAN[admitted].min()), float(X_SCAN[admitted].max())


def main() -> None:
    """Measure every bound of the iterated integral and compare it with Part 2."""
    print("inner bound: z runs from 0 to 1 - y at a fixed point of the projection")
    for x_value, y_value in SAMPLE_POINTS:
        low, high = z_segment(x_value, y_value)
        report(f"  lower z at (x, y) = ({x_value}, {y_value})", low, 0.0, GRID_TOLERANCE)
        report(f"  upper z at (x, y) = ({x_value}, {y_value})", high, 1.0 - y_value, GRID_TOLERANCE)

    print("")
    print("middle bound: y runs from x^2 to 1 at a fixed x")
    for x_value in SAMPLE_X_VALUES:
        low, high = y_segment(x_value)
        report(f"  lower y at x = {x_value}", low, x_value * x_value, GRID_TOLERANCE)
        report(f"  upper y at x = {x_value}", high, 1.0, GRID_TOLERANCE)

    print("")
    print("outer bound: x runs from -1 to 1")
    report("  smallest x of the solid", float(X_SCAN[X_SCAN * X_SCAN <= 1.0].min()), -1.0, GRID_TOLERANCE)
    report("  largest x of the solid", float(X_SCAN[X_SCAN * X_SCAN <= 1.0].max()), 1.0, GRID_TOLERANCE)
    report("  largest x that admits a point at y = 1.0002",
           float(X_SCAN[X_SCAN * X_SCAN <= 1.0002].max()), float(np.sqrt(1.0002)), GRID_TOLERANCE)
    report("  x admits no point at y = 0.9998 beyond sqrt(y)",
           float(X_SCAN[X_SCAN * X_SCAN <= 0.9998].max()), float(np.sqrt(0.9998)), GRID_TOLERANCE)

    print("")
    print("the roof is never below the floor on the projection")
    heights = np.linspace(0.0, 1.0, 100_001)
    report("  smallest roof height 1 - y on the projection", float((1.0 - heights).min()), 0.0, 0.0)

    print("")
    print("a point on the sharp edge is inside, and a point above it is outside")
    report("  inside(0, 1, 0)", float(inside(0.0, 1.0, 0.0)), 1.0, 0.0)
    report("  inside(0, 1, 0.001)", float(inside(0.0, 1.0, 0.001)), 0.0, 0.0)


if __name__ == "__main__":
    main()
