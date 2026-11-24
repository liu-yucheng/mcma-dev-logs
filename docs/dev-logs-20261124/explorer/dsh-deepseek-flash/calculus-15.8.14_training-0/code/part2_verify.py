"""Verify Part 2: the projection of the solid and the area of a horizontal section.

Each check compares a value that one method computes with a value that a second
method computes.  Each check prints the computed value and the expected value,
and it stops with an error when the two values differ by more than the stated
tolerance.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

GRID_HALF_WIDTH = 2.0
GRID_STEP = 0.005
HEIGHT_VALUES = (0.5, 2.5, 4.5)
AREA_TOLERANCE = 1.0e-10
COUNT_TOLERANCE = 1.0e-2


def inside_height_interval(x_values: np.ndarray, y_values: np.ndarray, height: float) -> np.ndarray:
    """Return True where the height lies between the two surfaces at that point."""
    squared_radius = x_values ** 2 + y_values ** 2
    return (squared_radius <= height) & (height <= 5.0 - squared_radius)


def largest_squared_radius_at_height(height: float) -> float:
    """Return the squared radius of the section at one height, from the two inequalities.

    The section at the height z holds the points that satisfy r^2 <= z and
    r^2 <= 5 - z at the same time.  The largest allowed squared radius is the
    root of min(z, 5 - z) - r^2, found here by bisection and not by a formula.
    """
    allowed = min(height, 5.0 - height)
    return float(brentq(lambda squared_radius: allowed - squared_radius, 0.0, 3.0, xtol=1.0e-15))


# BEGIN CHECK projection_membership
def check_projection_membership() -> None:
    """Check the projection of the solid against the disk x^2 + y^2 <= 5/2."""
    coordinate_values = np.arange(-GRID_HALF_WIDTH, GRID_HALF_WIDTH + GRID_STEP / 2.0, GRID_STEP)
    x_grid, y_grid = np.meshgrid(coordinate_values, coordinate_values, indexing="ij")
    squared_radius = x_grid ** 2 + y_grid ** 2
    lower_height = squared_radius
    upper_height = 5.0 - squared_radius
    feasible_from_surfaces = lower_height <= upper_height
    feasible_from_inequality = 2.0 * squared_radius <= 5.0
    mismatch_count = int(np.count_nonzero(feasible_from_surfaces != feasible_from_inequality))
    print("[projection_membership] grid points whose verdict differs, surface test against 2 r^2 <= 5")
    print(f"    computed {mismatch_count}   expected 0   grid {coordinate_values.size} by {coordinate_values.size}")
    assert mismatch_count == 0

    witness_height = 0.5 * (lower_height + upper_height)
    witness_holds = (witness_height >= lower_height) & (witness_height <= upper_height)
    witness_fraction = float(np.mean(witness_holds[feasible_from_surfaces]))
    gap_values = upper_height[~feasible_from_surfaces] - lower_height[~feasible_from_surfaces]
    greatest_gap = float(np.min(gap_values))
    print("[projection_membership] share of the feasible points whose middle height lies in the interval")
    print(f"    computed {witness_fraction:.6f}   expected 1.000000")
    print("[projection_membership] smallest upper-minus-lower height at the points outside the region")
    print(f"    computed {greatest_gap:.6f}   expected a value below 0.000000")
    assert abs(witness_fraction - 1.0) < 1.0e-12
    assert greatest_gap < 0.0

    feasible_radius = np.sqrt(squared_radius[feasible_from_surfaces])
    grid_radius = float(np.max(feasible_radius))
    exact_radius = math.sqrt(2.5)
    print("[projection_membership] largest radius of a feasible grid point against sqrt(5/2)")
    print(f"    computed {grid_radius:.6f}   expected {exact_radius:.6f}   grid step {GRID_STEP:.3f}")
    assert abs(grid_radius - exact_radius) < GRID_STEP
# END CHECK projection_membership


# BEGIN CHECK section_area_three_heights
def check_section_area_three_heights() -> None:
    """Check the area of the section at three heights by an integral and by a cell count."""
    print("[section_area_three_heights] area of the section at one height")
    print("    z      integral of 2 pi r      pi min(z, 5 - z)     cell count")
    for height in HEIGHT_VALUES:
        squared_radius_limit = largest_squared_radius_at_height(height)
        radius_limit = math.sqrt(squared_radius_limit)
        integral_area = float(quad(lambda radius: 2.0 * math.pi * radius, 0.0, radius_limit, limit=200)[0])
        formula_area = math.pi * min(height, 5.0 - height)
        coordinate_values = np.arange(-GRID_HALF_WIDTH, GRID_HALF_WIDTH + GRID_STEP / 2.0, GRID_STEP)
        x_grid, y_grid = np.meshgrid(coordinate_values, coordinate_values, indexing="ij")
        inside = inside_height_interval(x_grid, y_grid, height)
        counted_area = float(np.count_nonzero(inside)) * GRID_STEP ** 2
        print(f"    {height:3.1f}   {integral_area:.9f}          {formula_area:.9f}         {counted_area:.6f}")
        assert abs(integral_area - formula_area) < AREA_TOLERANCE * max(1.0, formula_area)
        assert abs(counted_area - formula_area) < COUNT_TOLERANCE * formula_area
    print("[section_area_three_heights] the largest area of the three rows sits at z = 2.5")
    area_at_middle = math.pi * min(2.5, 5.0 - 2.5)
    area_at_low = math.pi * min(0.5, 5.0 - 0.5)
    area_at_high = math.pi * min(4.5, 5.0 - 4.5)
    print(f"    computed {area_at_middle:.9f}   against {area_at_low:.9f} and {area_at_high:.9f}")
    assert area_at_middle > area_at_low
    assert area_at_middle > area_at_high
# END CHECK section_area_three_heights


# BEGIN CHECK widest_section
def check_widest_section() -> None:
    """Check the height and the area of the widest horizontal section."""
    height_grid = np.linspace(0.0, 5.0, 200001)
    area_grid = math.pi * np.minimum(height_grid, 5.0 - height_grid)
    grid_index = int(np.argmax(area_grid))
    grid_height = float(height_grid[grid_index])
    grid_area = float(area_grid[grid_index])
    equality_height = float(brentq(lambda height: height - (5.0 - height), 0.0, 5.0, xtol=1.0e-14))
    exact_area = math.pi * 2.5
    print("[widest_section] height of the widest section, grid maximum against the equality of the two surfaces")
    print(f"    computed {grid_height:.9f}   expected {equality_height:.9f}")
    print(f"    difference {abs(grid_height - equality_height):.3e}   tolerance 1.0e-4")
    assert abs(grid_height - equality_height) < 1.0e-4

    radius_limit = math.sqrt(largest_squared_radius_at_height(equality_height))
    integral_area = float(quad(lambda radius: 2.0 * math.pi * radius, 0.0, radius_limit, limit=200)[0])
    print("[widest_section] area of the widest section, integral against pi times the squared radius 5/2")
    print(f"    computed {integral_area:.12f}   expected {exact_area:.12f}")
    print(f"    difference {abs(integral_area - exact_area):.3e}   tolerance 1.0e-10")
    assert abs(integral_area - exact_area) < 1.0e-10
    print(f"[widest_section] grid maximum of the area is {grid_area:.12f}")
    assert abs(grid_area - exact_area) < 1.0e-10
# END CHECK widest_section


def main() -> None:
    """Run every check of Part 2."""
    check_projection_membership()
    check_section_area_three_heights()
    check_widest_section()
    print("part2_verify.py: every check of Part 2 passed")


if __name__ == "__main__":
    main()
