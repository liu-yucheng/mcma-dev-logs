"""Verify the geometric facts of the solid that the two paraboloids enclose.

The problem gives the lower surface y = x**2 + z**2 and the upper surface
y = 8 - x**2 - z**2. This script checks four facts:

1. The two surfaces meet at the radius 2, and the meeting height is 4.
2. The vertical thickness is positive inside the radius 2 and negative outside it.
3. The projection of the solid on the horizontal plane is the disk of radius 2,
   and the area of that disk is 4 * pi.
4. The lowest point of the solid is y = 0 and the highest point is y = 8.

Every check prints the computed value and the expected value.
"""

import math

import numpy as np
from scipy.optimize import brentq

# The lower surface is y = radius**2, so its coefficient is 1.
LOWER_SURFACE_COEFFICIENT = 1.0
# The upper surface is y = 8 - radius**2, so its constant term is 8.
UPPER_SURFACE_CONSTANT = 8.0
# The two surfaces meet where radius**2 = 8 - radius**2, that is, at radius 2.
EXPECTED_INTERSECTION_RADIUS = 2.0
# At the meeting radius the common height is 2**2 = 4.
EXPECTED_INTERSECTION_HEIGHT = 4.0
# The numerical comparison uses this absolute tolerance.
COMPARISON_TOLERANCE = 1.0e-9


def lower_height(radius: float) -> float:
    """Return the height of the lower paraboloid at the given radius."""
    return LOWER_SURFACE_COEFFICIENT * radius**2


def upper_height(radius: float) -> float:
    """Return the height of the upper paraboloid at the given radius."""
    return UPPER_SURFACE_CONSTANT - radius**2


def vertical_thickness(radius: float) -> float:
    """Return the vertical distance from the lower surface to the upper surface."""
    return upper_height(radius) - lower_height(radius)


def report(name: str, computed: float, expected: float) -> None:
    """Print one checked value, its expected value, and the absolute difference."""
    difference = abs(computed - expected)
    print(f"{name}: computed = {computed!r}, expected = {expected!r}, difference = {difference:.3e}")


def main() -> None:
    """Run every geometric check of part 1."""
    print("Part 1: geometry of the enclosed solid")

    # Check 1: the meeting radius is the positive root of the vertical thickness.
    meeting_radius = brentq(vertical_thickness, 0.0, 4.0, xtol=1.0e-14)
    report("meeting radius", meeting_radius, EXPECTED_INTERSECTION_RADIUS)
    assert abs(meeting_radius - EXPECTED_INTERSECTION_RADIUS) < COMPARISON_TOLERANCE

    # Check 2: both surfaces take the height 4 at the meeting radius.
    lower_value = lower_height(EXPECTED_INTERSECTION_RADIUS)
    upper_value = upper_height(EXPECTED_INTERSECTION_RADIUS)
    report("lower surface at radius 2", lower_value, EXPECTED_INTERSECTION_HEIGHT)
    report("upper surface at radius 2", upper_value, EXPECTED_INTERSECTION_HEIGHT)
    assert abs(lower_value - EXPECTED_INTERSECTION_HEIGHT) < COMPARISON_TOLERANCE
    assert abs(upper_value - EXPECTED_INTERSECTION_HEIGHT) < COMPARISON_TOLERANCE
    report("gap between the two surfaces at radius 2", upper_value - lower_value, 0.0)
    assert abs(upper_value - lower_value) < COMPARISON_TOLERANCE

    # Check 3: the thickness is positive inside the disk and negative outside it.
    inner_radii = np.linspace(0.0, 1.999, 400)
    outer_radii = np.linspace(2.001, 3.0, 200)
    inner_minimum = float(np.min(vertical_thickness(inner_radii)))
    outer_maximum = float(np.max(vertical_thickness(outer_radii)))
    expected_inner_minimum = float(UPPER_SURFACE_CONSTANT - 2.0 * inner_radii.max() ** 2)
    expected_outer_maximum = float(UPPER_SURFACE_CONSTANT - 2.0 * outer_radii.min() ** 2)
    report("smallest thickness on 0 <= radius <= 1.999", inner_minimum, expected_inner_minimum)
    report("largest thickness on 2.001 <= radius <= 3", outer_maximum, expected_outer_maximum)
    assert abs(inner_minimum - expected_inner_minimum) < COMPARISON_TOLERANCE
    assert abs(outer_maximum - expected_outer_maximum) < COMPARISON_TOLERANCE
    assert inner_minimum > 0.0
    assert outer_maximum < 0.0

    # Check 4: the solid projects onto the disk of radius 2, whose area is 4 * pi.
    projected_area = math.pi * EXPECTED_INTERSECTION_RADIUS**2
    report("area of the projection disk", projected_area, 4.0 * math.pi)
    assert abs(projected_area - 4.0 * math.pi) < COMPARISON_TOLERANCE

    # Check 5: eight points of the meeting curve satisfy both surface equations.
    angles = np.linspace(0.0, 2.0 * math.pi, 9)[:-1]
    worst_lower_gap = 0.0
    worst_upper_gap = 0.0
    for angle in angles:
        horizontal_x = EXPECTED_INTERSECTION_RADIUS * math.cos(angle)
        horizontal_z = EXPECTED_INTERSECTION_RADIUS * math.sin(angle)
        squared_radius = horizontal_x**2 + horizontal_z**2
        worst_lower_gap = max(worst_lower_gap, abs(EXPECTED_INTERSECTION_HEIGHT - squared_radius))
        worst_upper_gap = max(
            worst_upper_gap, abs(EXPECTED_INTERSECTION_HEIGHT - (UPPER_SURFACE_CONSTANT - squared_radius))
        )
    report("largest residual of the meeting curve on the lower surface", worst_lower_gap, 0.0)
    report("largest residual of the meeting curve on the upper surface", worst_upper_gap, 0.0)
    assert worst_lower_gap < COMPARISON_TOLERANCE
    assert worst_upper_gap < COMPARISON_TOLERANCE

    # Check 6: the lowest point is 0 and the highest point is 8.
    lowest_height = lower_height(0.0)
    highest_height = upper_height(0.0)
    report("lowest point of the solid", lowest_height, 0.0)
    report("highest point of the solid", highest_height, UPPER_SURFACE_CONSTANT)
    assert abs(lowest_height) < COMPARISON_TOLERANCE
    assert abs(highest_height - UPPER_SURFACE_CONSTANT) < COMPARISON_TOLERANCE

    print("Part 1: all checks passed")


if __name__ == "__main__":
    main()
