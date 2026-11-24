"""Anchor points and sizes that the figures and the verification scripts share.

Each anchor point lies on the surface that its name gives, so that a label sits on the surface that
it names. The verification scripts import this module and print the anchors, so that a step and its
figure cannot disagree about a drawn point or a drawn number.
"""

from __future__ import annotations

import math

CYLINDER_RADIUS = 3.0
SECTION_Y = 1.5
MONTE_CARLO_SAMPLE_COUNT = 2_000_000
MONTE_CARLO_SEED = 25

CYLINDER_LABEL_POINT = (0.30, 1.50, math.sqrt(9.0 - 1.50 ** 2))
CYLINDER_LABEL_OFFSET = (0.10, 0.85, 0.62)
ZERO_PLANE_LABEL_POINT = (0.25, 0.90, 0.0)
ZERO_PLANE_LABEL_OFFSET = (0.92, -0.55, 0.14)
X_ZERO_PLANE_LABEL_POINT = (0.0, 2.10, 0.90)
X_ZERO_PLANE_LABEL_OFFSET = (0.05, 0.65, 1.05)
PLANE_Y_EQUALS_3X_LABEL_POINT = (0.40, 1.20, 0.60)
PLANE_Y_EQUALS_3X_LABEL_OFFSET = (0.45, 0.0, 0.55)

SURFACE_LABEL_ANCHORS = {
    "cylinder": (CYLINDER_LABEL_POINT, CYLINDER_LABEL_OFFSET),
    "zero_plane": (ZERO_PLANE_LABEL_POINT, ZERO_PLANE_LABEL_OFFSET),
    "x_zero_plane": (X_ZERO_PLANE_LABEL_POINT, X_ZERO_PLANE_LABEL_OFFSET),
    "plane_y_equals_3x": (PLANE_Y_EQUALS_3X_LABEL_POINT, PLANE_Y_EQUALS_3X_LABEL_OFFSET),
}


def label_residual(surface: str, point: tuple[float, float, float]) -> float:
    """Return the residual of the point in the equation of the named surface."""
    x, y, z = point
    if surface == "cylinder":
        return abs(y * y + z * z - 9.0)
    if surface == "zero_plane":
        return abs(z)
    if surface == "x_zero_plane":
        return abs(x)
    if surface == "plane_y_equals_3x":
        return abs(y - 3.0 * x)
    raise ValueError(f"unknown surface: {surface}")
