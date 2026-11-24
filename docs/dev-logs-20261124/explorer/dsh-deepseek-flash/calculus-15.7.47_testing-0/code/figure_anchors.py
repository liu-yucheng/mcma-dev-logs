"""Drawing constants of the three figures, shared with the verification scripts.

A verification script imports this module, so a number that the page prints and a
shape that a figure draws come from one source. Each surface label sits at a point
that satisfies the equation of its surface.
"""

from __future__ import annotations

import math

Z_SLICES: tuple[float, ...] = (0.0, 0.5, 0.8)
"""Heights of the three sections at a fixed z that Figure 2 draws."""

Y_SLICES: tuple[float, ...] = (0.25, 0.5, 1.0)
"""Values of y of the three sections at a fixed y that Figure 2 draws."""

BOUNDARY_Y_VALUES: tuple[float, ...] = (0.0, 1.0)
"""End values of y, where the section changes shape."""

BOUNDARY_Z_VALUES: tuple[float, ...] = (0.0, 1.0)
"""End values of z, where the section changes shape."""

CYLINDER_LABEL_POINT: tuple[float, float, float] = (0.55, 0.3025, 0.55)
"""Point of the label of the cylinder y = x^2. The point satisfies y = x^2."""

FLOOR_LABEL_POINT: tuple[float, float, float] = (-0.55, 0.72, 0.0)
"""Point of the label of the plane z = 0. The point satisfies z = 0."""

TOP_LABEL_POINT: tuple[float, float, float] = (0.0, 0.32, 0.68)
"""Point of the label of the plane y + z = 1. The point satisfies y + z = 1."""

APEX_POINT: tuple[float, float, float] = (0.0, 0.0, 1.0)
"""Highest point of the solid, where the cylinder meets the plane y + z = 1."""

CORNER_POINTS: tuple[tuple[float, float, float], ...] = (
    (-1.0, 1.0, 0.0),
    (1.0, 1.0, 0.0),
    (0.0, 0.0, 0.0),
)
"""Three points that fix the outline of the solid: the two rim corners and the origin."""


def residuals() -> dict[str, float]:
    """Return the value of the left side minus the right side at each label point.

    Returns:
        One dictionary from the surface name to the residual of its equation at
        the point where the figure writes the label.
    """
    cylinder_x, cylinder_y, _ = CYLINDER_LABEL_POINT
    _, floor_y, floor_z = FLOOR_LABEL_POINT
    _, top_y, top_z = TOP_LABEL_POINT
    return {
        "cylinder y = x^2": cylinder_y - cylinder_x**2,
        "plane z = 0": floor_z - 0.0,
        "plane y + z = 1": (top_y + top_z) - 1.0,
    }


def section_extent_at_y(y: float) -> tuple[float, float, float]:
    """Return the half width in x and the height in z of the section at one y.

    Args:
        y: Value of the second coordinate.

    Returns:
        The tuple (half width, height, area) of the rectangular section.
    """
    half_width = math.sqrt(y)
    height = 1.0 - y
    return half_width, height, 2.0 * half_width * height


def section_extent_at_z(z: float) -> tuple[float, float]:
    """Return the half width in x and the area of the section at one z.

    Args:
        z: Value of the third coordinate.

    Returns:
        The tuple (half width, area) of the parabolic section.
    """
    half_width = math.sqrt(max(0.0, 1.0 - z))
    return half_width, (4.0 / 3.0) * (1.0 - z) ** 1.5
