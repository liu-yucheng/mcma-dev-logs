"""Anchor points and sampling positions that the figures of the tutorial draw.

Every drawn shape that the tutorial also prints in a sentence takes its numbers from this module. A verification
script imports the module and asserts the property of each point, so the step text and the picture cannot
disagree.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

import numpy as np


@dataclass(frozen=True)
class SurfaceLabel:
    """One text label of a surface together with the point where the figure writes it.

    Attributes:
        surface_name: The name of the surface that the label names.
        label_text: The text of the label.
        anchor_point: The point (x, y, z) of the anchor.
        text_offset: The offset (dx, dy, dz) from the anchor point to the text.
    """

    surface_name: str
    label_text: str
    anchor_point: tuple[float, float, float]
    text_offset: tuple[float, float, float]


SURFACE_LABELS: tuple[SurfaceLabel, ...] = (
    SurfaceLabel(
        surface_name="parabolic cylinder z = 1 - y^2",
        label_text=r"$z = 1 - y^{2}$",
        anchor_point=(0.10, 0.5, 0.75),
        text_offset=(-0.12, 0.10, 0.14),
    ),
    SurfaceLabel(
        surface_name="plane x + z = 1",
        label_text=r"$x + z = 1$",
        anchor_point=(0.375, 0.0, 0.625),
        text_offset=(0.10, 0.0, 0.10),
    ),
    SurfaceLabel(
        surface_name="plane x = 0",
        label_text=r"$x = 0$",
        anchor_point=(0.0, 0.75, 0.15),
        text_offset=(-0.16, 0.06, 0.10),
    ),
    SurfaceLabel(
        surface_name="plane z = 0",
        label_text=r"$z = 0$",
        anchor_point=(0.5, -0.5, 0.0),
        text_offset=(0.05, 0.0, -0.14),
    ),
)
"""The four surface labels of figure 1, each with an anchor that its own equation satisfies."""

AXIS_ARROW_LENGTH: float = 1.35
"""The length of one axis arrow of the three-dimensional panel of figure 1."""

PROJECTION_CORNERS_XZ: tuple[tuple[float, float], ...] = ((0.0, 0.0), (1.0, 0.0), (0.0, 1.0))
"""The three corners of the projection of E on the plane y = 0, in the (x, z) coordinates of that plane."""

TRAPEZOID_LABEL_EPSILON: float = 0.15
"""The distance from the slanted edge at which figure 2 writes the label of the slanted edge."""

HEIGHTS_CHECKED_IN_FIGURE: tuple[float, ...] = (0.0, 0.5, 0.9)
"""The three heights at which figure 2 marks the section area."""

CENTER_OF_MASS_AXES: tuple[str, str] = ("x", "z")
"""The two coordinates that the plane of the projection keeps."""

CENTER_OF_MASS_POINT: tuple[float, float] = (float(Fraction(5, 14)), float(Fraction(2, 7)))
"""The exact center of mass in the (x, z) plane, written from the exact fractions."""

TRIANGLE_CENTROID_POINT: tuple[float, float] = (1.0 / 3.0, 1.0 / 3.0)
"""The centroid of the projection triangle, drawn beside the center of mass for comparison."""


def cylinder_residual(point: tuple[float, float, float]) -> float:
    """Return the residual z - (1 - y^2) of the cylinder equation at a point.

    Args:
        point: The point (x, y, z).

    Returns:
        The signed residual of the equation z = 1 - y^2.
    """
    return point[2] - (1.0 - point[1] ** 2)


def inclined_plane_residual(point: tuple[float, float, float]) -> float:
    """Return the residual x + z - 1 of the plane equation at a point.

    Args:
        point: The point (x, y, z).

    Returns:
        The signed residual of the equation x + z = 1.
    """
    return point[0] + point[2] - 1.0


def projection_polygon() -> np.ndarray:
    """Return the corners of the projection triangle as an array of shape (3, 2).

    Returns:
        The three corners in the (x, z) coordinates of the plane y = 0.
    """
    return np.array(PROJECTION_CORNERS_XZ, dtype=float)
