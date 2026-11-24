"""Verify the cross-section area of Part 3 and the volume by horizontal slices.

The script checks four claims of Part 3.
The first claim is that the slice at y = c is the disk cut by the half plane z <= 4 - c.
The second claim is that the area of the slice is 4 pi for c <= 2 and is the segment formula
for 2 < c <= 6.
The third claim is that the area falls from 4 pi to 0 as c grows.
The fourth claim is that the integral of the area from -1 to 6 equals 20 pi.

The area of each slice is computed in two ways.
The first way uses the closed form of the circular segment.
The second way integrates the length of the slice in z over x, and it uses only the two
inequalities x^2 + z^2 <= 4 and z <= 4 - c.
"""

import math
from typing import Final

from scipy.integrate import quad

SQUARED_RADIUS: Final[float] = 4.0
"""Right side of the cylinder equation x^2 + z^2 = 4."""

RADIUS: Final[float] = 2.0
"""Radius of the disk, equal to the positive root of x^2 = 4."""

CUT_CONSTANT: Final[float] = 4.0
"""Right side of the top plane y + z = 4, which gives z <= 4 - y."""

BOTTOM_HEIGHT: Final[float] = -1.0
"""Height of the bottom plane y = -1."""

TOP_HEIGHT: Final[float] = 6.0
"""Largest height of the solid, at z = -2, where y = 4 - z = 6."""

SAMPLE_HEIGHTS: Final[tuple[float, ...]] = (-1.0, 0.0, 1.5, 2.0, 3.0, 4.0, 5.0, 5.9, 6.0)
"""Heights at which the script compares the closed form with the integration."""

AREA_TOLERANCE: Final[float] = 1.0e-8
"""Largest difference between the closed form and the integration that the script accepts."""

VOLUME_TOLERANCE: Final[float] = 1.0e-8
"""Largest difference between a computed volume and 20 pi that the script accepts."""


def slice_area_closed_form(height: float) -> float:
    """Return the area of the slice at y = height from the circular segment formula.

    Args:
        height: Fixed value of y.

    Returns:
        The area of the set {(x, z): x^2 + z^2 <= 4 and z <= 4 - height}.
    """
    cut_position = CUT_CONSTANT - height
    if cut_position >= RADIUS:
        return math.pi * RADIUS**2
    if cut_position <= -RADIUS:
        return 0.0
    distance = -cut_position
    return RADIUS**2 * math.acos(distance / RADIUS) - distance * math.sqrt(
        RADIUS**2 - distance**2
    )


def slice_area_by_integration(height: float) -> float:
    """Return the area of the slice at y = height by integration of the length in z over x."""
    cut_position = CUT_CONSTANT - height

    def length_in_z(x_value: float) -> float:
        """Return the length of the part of the vertical line at x_value that lies in the slice."""
        half_length = math.sqrt(max(0.0, SQUARED_RADIUS - x_value * x_value))
        upper = min(half_length, cut_position)
        return max(0.0, upper + half_length)

    break_points: list[float] = []
    if abs(cut_position) < RADIUS:
        boundary = math.sqrt(SQUARED_RADIUS - cut_position**2)
        break_points = [-boundary, boundary]
    value, _ = quad(
        length_in_z,
        -RADIUS,
        RADIUS,
        points=break_points,
        epsabs=1.0e-12,
        limit=200,
    )
    return value


def volume_by_slices() -> float:
    """Return the volume as the integral of the closed form area from -1 to 6."""
    value, _ = quad(
        slice_area_closed_form,
        BOTTOM_HEIGHT,
        TOP_HEIGHT,
        points=[CUT_CONSTANT - RADIUS],
        epsabs=1.0e-12,
        limit=200,
    )
    return value


def volume_by_slice_pieces() -> float:
    """Return the volume as the sum of the flat part and the curved part of the slice area."""
    flat_length = CUT_CONSTANT - RADIUS - BOTTOM_HEIGHT
    flat_part = flat_length * math.pi * RADIUS**2
    curved_part, _ = quad(
        slice_area_closed_form,
        CUT_CONSTANT - RADIUS,
        TOP_HEIGHT,
        epsabs=1.0e-12,
        limit=200,
    )
    return flat_part + curved_part


def main() -> None:
    """Run the four checks of Part 3 and print each computed value with its expected value."""
    exact_volume = 20.0 * math.pi
    largest_difference = 0.0
    for height in SAMPLE_HEIGHTS:
        closed_form = slice_area_closed_form(height)
        integrated = slice_area_by_integration(height)
        largest_difference = max(largest_difference, abs(closed_form - integrated))
        print(
            f"height {height:5.2f}: closed form {closed_form:11.8f}, "
            f"integration {integrated:11.8f}"
        )
    print(f"largest difference of the area table: {largest_difference:.3e}")
    assert largest_difference <= AREA_TOLERANCE, "the closed form and the integration disagree"

    full_area = math.pi * RADIUS**2
    print(f"largest slice area: closed form at 0 {slice_area_closed_form(0.0):.12f}")
    print(f"largest slice area: disk area           {full_area:.12f}")
    assert abs(slice_area_closed_form(0.0) - full_area) <= 1.0e-12, "the flat part is not 4 pi"
    assert abs(slice_area_closed_form(2.0) - full_area) <= 1.0e-9, "the area is discontinuous at 2"
    assert slice_area_closed_form(TOP_HEIGHT) == 0.0, "the slice at the top is not empty"

    heights = [BOTTOM_HEIGHT + index * 0.01 for index in range(701)]
    areas = [slice_area_closed_form(height) for height in heights]
    decreases = [later - earlier for earlier, later in zip(areas, areas[1:])]
    print(f"largest increase of the area: {max(decreases):.3e}")
    assert max(decreases) <= 1.0e-12, "the area is not non-increasing in the height"

    volume_slices = volume_by_slices()
    volume_pieces = volume_by_slice_pieces()
    flat_part = (CUT_CONSTANT - RADIUS - BOTTOM_HEIGHT) * full_area
    curved_part = volume_pieces - flat_part
    print(f"volume by slices:  {volume_slices:.12f}")
    print(f"volume by pieces:  {volume_pieces:.12f}")
    print(f"flat part 12 pi:   {flat_part:.12f}, curved part: {curved_part:.12f}")
    print(f"closed form 20 pi: {exact_volume:.12f}")
    assert abs(volume_slices - exact_volume) <= VOLUME_TOLERANCE, "the slice integral is not 20 pi"
    assert abs(volume_pieces - exact_volume) <= VOLUME_TOLERANCE, "the pieces do not sum to 20 pi"
    assert abs(volume_slices - volume_pieces) <= 1.0e-9, "the two volume computations disagree"
    assert abs(curved_part - 8.0 * math.pi) <= VOLUME_TOLERANCE, "the curved part is not 8 pi"

    print("part 3: all checks passed")


if __name__ == "__main__":
    main()
