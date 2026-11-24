"""Label anchors, view settings, and axis extents of every figure of this tutorial.

Every figure script reads this module, and every verification script reads this module.  A point
that a figure labels is therefore a point that a check tests against the equation of its own
surface.  A label sits at the anchor point, and the leader line leaves the anchor point, so no
label floats away from the surface that its equation names.
"""

import math

from silo_geometry import (
    APEX_HEIGHT,
    CAP_RADIUS,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    cap_point,
    lateral_point,
    lower_face_point,
)

LATERAL_LABEL_ANGLE_DEGREES = -64.0
"""Angle of the point of the lateral face that its label names."""

LATERAL_LABEL_HEIGHT = 6.4
"""Height of the point of the lateral face that its label names."""

LOWER_FACE_LABEL_RADIUS = 1.7
"""Radius of the point of the lower disk that its label names."""

LOWER_FACE_LABEL_ANGLE_DEGREES = 28.0
"""Angle of the point of the lower disk that its label names."""

CAP_LABEL_INCLINATION_DEGREES = 44.0
"""Inclination of the point of the cap that its label names, from the pole of the cap."""

CAP_LABEL_AZIMUTH_DEGREES = -112.0
"""Azimuth of the point of the cap that its label names."""

RIM_LABEL_ANGLE_DEGREES = -18.0
"""Angle of the point of the rim circle that its label names."""

SLICE_HEIGHTS = (3.0, 10.0, 11.5)
"""Heights of the three horizontal sections that Part 2 checks and Figure 2 marks."""

SECTION_HEIGHT_SHOWN = 8.0
"""Height of the section that the section panel of Figure 1 fills."""

AXIS_X_MINIMUM = -4.4
"""Smallest drawn value of the x axis of Figure 1."""

AXIS_X_MAXIMUM = 4.4
"""Largest drawn value of the x axis of Figure 1."""

AXIS_Y_MINIMUM = -4.4
"""Smallest drawn value of the y axis of Figure 1."""

AXIS_Y_MAXIMUM = 4.4
"""Largest drawn value of the y axis of Figure 1."""

AXIS_Z_MINIMUM = -0.6
"""Smallest drawn value of the z axis of Figure 1."""

AXIS_Z_MAXIMUM = 15.2
"""Largest drawn value of the z axis of Figure 1."""

AXIS_LABEL_INSET = 0.55
"""Distance from the tip of an axis to the letter that names the axis, in data units."""

VIEW_ELEVATION_DEGREES = 16.0
"""Elevation of the three-dimensional view of Figure 1."""

VIEW_AZIMUTH_DEGREES = -58.0
"""Azimuth of the three-dimensional view of Figure 1."""

WALL_ALPHA = 0.62
"""Opacity of the lateral face, above one half so that the body reads as a closed solid."""

CAP_ALPHA = 0.42
"""Opacity of the cap, low enough to show the section inside the body."""


def lateral_label_anchor() -> tuple[float, float, float]:
    """Return the point of the lateral face that its label names."""
    return lateral_point(math.radians(LATERAL_LABEL_ANGLE_DEGREES), LATERAL_LABEL_HEIGHT)


def lower_face_label_anchor() -> tuple[float, float, float]:
    """Return the point of the lower disk that its label names."""
    return lower_face_point(
        LOWER_FACE_LABEL_RADIUS, math.radians(LOWER_FACE_LABEL_ANGLE_DEGREES)
    )


def cap_label_anchor() -> tuple[float, float, float]:
    """Return the point of the hemispherical cap that its label names."""
    return cap_point(
        math.radians(CAP_LABEL_INCLINATION_DEGREES), math.radians(CAP_LABEL_AZIMUTH_DEGREES)
    )


def rim_label_anchor() -> tuple[float, float, float]:
    """Return the point of the rim circle that its label names."""
    return lateral_point(math.radians(RIM_LABEL_ANGLE_DEGREES), CYLINDER_HEIGHT)


def label_anchor_table() -> list[tuple[str, tuple[float, float, float], str]]:
    """Return the name, the point, and the equation of every surface label anchor.

    The table holds the three faces of the boundary of the body.  The disk at the height 10 does
    not appear: the cap covers it, so the disk is not part of the boundary.
    """
    return [
        ("lateral face", lateral_label_anchor(), "x^2+y^2=9"),
        ("lower disk", lower_face_label_anchor(), "z=0"),
        ("cap", cap_label_anchor(), "x^2+y^2+(z-10)^2=9"),
    ]


def zoom_limits() -> tuple[float, float, float, float, float, float]:
    """Return the six limits of the three-dimensional axes of Figure 1."""
    return (
        AXIS_X_MINIMUM,
        AXIS_X_MAXIMUM,
        AXIS_Y_MINIMUM,
        AXIS_Y_MAXIMUM,
        AXIS_Z_MINIMUM,
        AXIS_Z_MAXIMUM,
    )


def apex_point() -> tuple[float, float, float]:
    """Return the highest point of the body."""
    return (0.0, 0.0, APEX_HEIGHT)


def rim_radius_check() -> float:
    """Return the distance of the rim anchor from the z axis, for a check against 3."""
    x_value, y_value, _z_value = rim_label_anchor()
    return math.hypot(x_value, y_value)


def cap_anchor_height_above_base() -> float:
    """Return the height of the cap anchor above the base of the cap, for a check."""
    return cap_label_anchor()[2] - CYLINDER_HEIGHT


def meridian_half_width(height: float) -> float:
    """Return the half width of the meridian section of the body at the given height."""
    if height < 0.0 or height > APEX_HEIGHT:
        return 0.0
    if height <= CYLINDER_HEIGHT:
        return CYLINDER_RADIUS
    return math.sqrt(max(0.0, CAP_RADIUS**2 - (height - CYLINDER_HEIGHT) ** 2))
