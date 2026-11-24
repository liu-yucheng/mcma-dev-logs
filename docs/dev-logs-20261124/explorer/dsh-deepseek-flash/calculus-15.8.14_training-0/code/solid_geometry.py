"""Build the geometry of the drawing: the two surfaces, the meeting circle, and the label anchors.

The module holds one definition of the drawing so that the figure scripts and the
verification scripts read the same numbers.  Every anchor of a surface label is a
point that the equation of that surface satisfies, and the verification script of
Part 5 checks each anchor against its equation.
"""

from __future__ import annotations

import math

import numpy as np

RIM_SQUARED_RADIUS = 2.5
MEETING_HEIGHT = 2.5
AXIS_LIMIT = 2.0
TOP_HEIGHT = 5.0
RADIUS_COUNT = 41
ANGLE_COUNT = 145
CIRCLE_COUNT = 361


def build_surface_meshes() -> dict[str, np.ndarray]:
    """Return the x, y, and z arrays of the two surfaces over the projection disk.

    The mesh runs over the closed disk of squared radius 5/2, so the two surfaces
    meet along the edge of the mesh and the pair reads as a closed body.
    """
    radius_values = np.linspace(0.0, math.sqrt(RIM_SQUARED_RADIUS), RADIUS_COUNT)
    angle_values = np.linspace(0.0, 2.0 * math.pi, ANGLE_COUNT)
    radius_grid, angle_grid = np.meshgrid(radius_values, angle_values, indexing="ij")
    x_values = radius_grid * np.cos(angle_grid)
    y_values = radius_grid * np.sin(angle_grid)
    squared_radius = radius_grid ** 2
    return {
        "x": x_values,
        "y": y_values,
        "lower": squared_radius,
        "upper": 5.0 - squared_radius,
        "radius": radius_grid,
    }


def build_meeting_circle() -> dict[str, np.ndarray]:
    """Return the circle where the two surfaces meet, at the height 5/2."""
    angle_values = np.linspace(0.0, 2.0 * math.pi, CIRCLE_COUNT)
    radius = math.sqrt(RIM_SQUARED_RADIUS)
    return {
        "x": radius * np.cos(angle_values),
        "y": radius * np.sin(angle_values),
        "z": np.full(angle_values.shape, MEETING_HEIGHT),
    }


def build_label_anchors() -> tuple[dict[str, object], ...]:
    """Return the anchor point and the equation name of each surface label.

    Each entry holds the text key, the three coordinates of the anchor, and the
    name of the surface that the anchor belongs to.  The anchor of the lower
    surface satisfies z = x^2 + y^2, the anchor of the upper surface satisfies
    z = 5 - x^2 - y^2, and the anchor of the circle satisfies both equations.
    """
    lower_radius = 1.25
    lower_angle = math.radians(200.0)
    upper_radius = 1.15
    upper_angle = math.radians(140.0)
    circle_radius = math.sqrt(RIM_SQUARED_RADIUS)
    circle_angle = math.radians(25.0)
    return (
        {
            "key": "lower",
            "text": r"$z = x^{2} + y^{2}$",
            "x": lower_radius * math.cos(lower_angle),
            "y": lower_radius * math.sin(lower_angle),
            "z": lower_radius**2,
            "surface": "lower",
        },
        {
            "key": "upper",
            "text": r"$z = 5 - x^{2} - y^{2}$",
            "x": upper_radius * math.cos(upper_angle),
            "y": upper_radius * math.sin(upper_angle),
            "z": 5.0 - upper_radius**2,
            "surface": "upper",
        },
        {
                        "key": "circle",
            "text": r"$x^{2} + y^{2} = \frac{5}{2}$, $z = \frac{5}{2}$",
            "x": circle_radius * math.cos(circle_angle),
            "y": circle_radius * math.sin(circle_angle),
            "z": MEETING_HEIGHT,
            "surface": "circle",
        },
    )
