"""Verify Part 1: the two paraboloids and the curve where the two surfaces meet.

Each check compares a value that one method computes with a value that a second
method computes.  Each check prints the computed value and the expected value,
and it stops with an error when the two values differ by more than the stated
tolerance.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from scipy.optimize import brentq

RANDOM_SEED = 20261123
SAMPLE_COUNT = 200000
RADIUS_TOLERANCE = 1.0e-12
HEIGHT_TOLERANCE = 1.0e-12


def lower_surface(x_values: np.ndarray, y_values: np.ndarray) -> np.ndarray:
    """Return the height of the paraboloid z = x^2 + y^2 at each point."""
    return x_values ** 2 + y_values ** 2


def upper_surface(x_values: np.ndarray, y_values: np.ndarray) -> np.ndarray:
    """Return the height of the paraboloid z = 5 - x^2 - y^2 at each point."""
    return 5.0 - x_values ** 2 - y_values ** 2


def height_difference(radius: float) -> float:
    """Return upper height minus lower height at the radius r, that is 5 - 2 r^2."""
    return (5.0 - radius ** 2) - radius ** 2


# BEGIN CHECK cylindrical_identity
def check_cylindrical_identity() -> None:
    """Check that the height of each surface depends on the squared radius only."""
    generator = np.random.default_rng(RANDOM_SEED)
    x_values = generator.uniform(-2.0, 2.0, SAMPLE_COUNT)
    y_values = generator.uniform(-2.0, 2.0, SAMPLE_COUNT)
    cartesian_lower = lower_surface(x_values, y_values)
    radius = np.hypot(x_values, y_values)
    radius_lower = radius ** 2
    cartesian_upper = upper_surface(x_values, y_values)
    radius_upper = 5.0 - radius ** 2
    lower_gap = float(np.max(np.abs(cartesian_lower - radius_lower)))
    upper_gap = float(np.max(np.abs(cartesian_upper - radius_upper)))
    print("[cylindrical_identity] lower surface, largest gap between x^2 + y^2 and r^2")
    print(f"    computed {lower_gap:.3e}   expected 0.000e+00   tolerance {RADIUS_TOLERANCE:.1e}")
    print("[cylindrical_identity] upper surface, largest gap between 5 - x^2 - y^2 and 5 - r^2")
    print(f"    computed {upper_gap:.3e}   expected 0.000e+00   tolerance {RADIUS_TOLERANCE:.1e}")
    assert lower_gap < RADIUS_TOLERANCE
    assert upper_gap < RADIUS_TOLERANCE

    radius_grid = np.linspace(0.0, math.sqrt(2.5), 200)
    step = float(radius_grid[1] - radius_grid[0])
    middle_radius = 0.5 * (radius_grid[1:] + radius_grid[:-1])
    numeric_lower_slope = np.diff(lower_surface(radius_grid, np.zeros_like(radius_grid))) / step
    numeric_upper_slope = np.diff(upper_surface(radius_grid, np.zeros_like(radius_grid))) / step
    analytic_lower_slope = 2.0 * middle_radius
    analytic_upper_slope = -2.0 * middle_radius
    lower_slope_gap = float(np.max(np.abs(numeric_lower_slope - analytic_lower_slope)))
    upper_slope_gap = float(np.max(np.abs(numeric_upper_slope - analytic_upper_slope)))
    print("[cylindrical_identity] slope of the lower surface along r, finite difference against 2 r")
    print(f"    computed {lower_slope_gap:.3e}   expected 0.000e+00   tolerance 1.0e-03")
    print("[cylindrical_identity] slope of the upper surface along r, finite difference against -2 r")
    print(f"    computed {upper_slope_gap:.3e}   expected 0.000e+00   tolerance 1.0e-03")
    assert lower_slope_gap < 1.0e-3
    assert upper_slope_gap < 1.0e-3
# END CHECK cylindrical_identity


# BEGIN CHECK meeting_curve_root
def check_meeting_curve_root() -> None:
    """Check the radius at which the two heights are equal against the root of 5 - 2 r^2."""
    numeric_radius = float(brentq(height_difference, 0.0, 2.0, xtol=1.0e-15, rtol=1.0e-15))
    algebraic_radius = math.sqrt(2.5)
    radius_gap = abs(numeric_radius - algebraic_radius)
    print("[meeting_curve_root] radius of the meeting circle, root of 5 - 2 r^2 against sqrt(5/2)")
    print(f"    computed {numeric_radius:.15f}   expected {algebraic_radius:.15f}")
    print(f"    difference {radius_gap:.3e}   tolerance {RADIUS_TOLERANCE:.1e}")
    assert radius_gap < RADIUS_TOLERANCE

    angle_values = np.linspace(0.0, 2.0 * math.pi, 72, endpoint=False)
    x_values = numeric_radius * np.cos(angle_values)
    y_values = numeric_radius * np.sin(angle_values)
    lower_heights = lower_surface(x_values, y_values)
    upper_heights = upper_surface(x_values, y_values)
    height_gap = float(np.max(np.abs(lower_heights - upper_heights)))
    height_value = float(np.max(np.abs(lower_heights - 2.5)))
    print("[meeting_curve_root] 72 points of the circle, largest gap between the two heights")
    print(f"    computed {height_gap:.3e}   expected 0.000e+00   tolerance {HEIGHT_TOLERANCE:.1e}")
    print("[meeting_curve_root] the same 72 points, largest gap between the common height and 2.5")
    print(f"    computed {height_value:.3e}   expected 0.000e+00   tolerance {HEIGHT_TOLERANCE:.1e}")
    assert height_gap < HEIGHT_TOLERANCE
    assert height_value < HEIGHT_TOLERANCE

    radius_grid = np.linspace(0.0, 2.0, 401)
    difference_values = height_difference(radius_grid)
    derivative_values = np.diff(difference_values) / float(radius_grid[1] - radius_grid[0])
    greatest_derivative = float(np.max(derivative_values[1:]))
    print("[meeting_curve_root] largest slope of 5 - 2 r^2 away from r = 0, a negative value means one root")
    print(f"    computed {greatest_derivative:.6f}   expected a value below 0.000000")
    assert greatest_derivative < 0.0
# END CHECK meeting_curve_root


# BEGIN CHECK above_below_order
def check_above_below_order() -> None:
    """Check which surface is higher on each side of the meeting radius."""
    squared_radius_values = [Fraction(0), Fraction(1), Fraction(2), Fraction(5, 2), Fraction(3), Fraction(4)]
    exact_differences = [Fraction(5) - Fraction(2) * value for value in squared_radius_values]
    print("[above_below_order] height of the upper surface minus the height of the lower surface")
    print("    r^2        exact difference      floating difference")
    for squared_radius, exact_difference in zip(squared_radius_values, exact_differences):
        radius = math.sqrt(float(squared_radius))
        floating_difference = height_difference(radius)
        print(f"    {float(squared_radius):5.2f}   {str(exact_difference):>12}   {floating_difference: .6f}")
    assert exact_differences[0] > 0
    assert exact_differences[1] > 0
    assert exact_differences[2] > 0
    assert exact_differences[3] == 0
    assert exact_differences[4] < 0
    assert exact_differences[5] < 0

    inside = [
        height_difference(math.sqrt(float(value)))
        for value in squared_radius_values
        if value < Fraction(5, 2)
    ]
    outside = [
        height_difference(math.sqrt(float(value)))
        for value in squared_radius_values
        if value > Fraction(5, 2)
    ]
    print("[above_below_order] smallest difference inside the circle against largest difference outside")
    print(f"    computed {min(inside):.6f} and {max(outside):.6f}   expected two values of opposite sign")
    assert min(inside) > 0.0
    assert max(outside) < 0.0
# END CHECK above_below_order


def main() -> None:
    """Run every check of Part 1."""
    check_cylindrical_identity()
    check_meeting_curve_root()
    check_above_below_order()
    print("part1_verify.py: every check of Part 1 passed")


if __name__ == "__main__":
    main()
