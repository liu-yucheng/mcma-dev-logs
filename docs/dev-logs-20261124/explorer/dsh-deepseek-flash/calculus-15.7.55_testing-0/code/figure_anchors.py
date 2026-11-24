"""Drawing constants for the figures of Problem 15.7.55.

The figure scripts and the verification scripts import this module, so that every number and every
geometric description of a drawn shape has one source.
"""

from __future__ import annotations

import math

import support

SECTION_HEIGHT = 0.4
"""The height of the drawn cross section of the ellipsoid."""

AXIS_ARROW_LENGTH = 1.28
"""The length of each drawn coordinate arrow, measured in units of the longest semi-axis."""

SURFACE_LABEL_POINT = (0.30, 0.30)
"""The pair $(x, y)$ of the surface point that carries the label of the boundary."""

SURFACE_LABEL_OFFSET = (34.0, 18.0)
"""The offset in points from the surface point to the boundary label."""

AXIS_LABEL_OFFSET = (8.0, 6.0)
"""The offset in points from an arrow tip to its axis letter."""

SECTION_LABEL_OFFSET = (26.0, -22.0)
"""The offset in points from the section edge to the section label."""

CANDIDATE_ORDER = ("unit ball", "unit cube", "scaled 0.8", "scaled 1.25", "ellipsoid P")
"""The order of the candidate regions in the bar chart."""

BAR_REFERENCE_LABEL_OFFSET = (0.0, 14.0)
"""The offset in points from the reference line to its label."""

RADIAL_SAMPLE_COUNT = 400
"""The number of sample radii of the integrand panel."""

RADIAL_MAXIMUM_RADIUS = 1.0
"""The outer radius of the radial panel."""

CUMULATIVE_RADII = tuple(0.05 * step for step in range(1, 21))
"""The radii at which the cumulative integral is plotted."""

CUMULATIVE_REFERENCE_OFFSET = 0.0035
"""The vertical offset of the reference line from the limit value, in units of the integral."""


def surface_label_height() -> float:
    """Return the $z$ of the surface point that carries the boundary label."""
    x, y = SURFACE_LABEL_POINT
    remaining = 1.0 - support.quadratic_form(x, y, 0.0)
    return math.sqrt(max(0.0, remaining / support.COEFFICIENT_Z_SQUARED))


def section_semi_axes() -> tuple[float, float]:
    """Return the two semi-axes of the drawn cross section."""
    return support.cross_section_semi_axes(SECTION_HEIGHT)


def section_quarter_point() -> tuple[float, float, float]:
    """Return the point of the drawn section edge at the parameter angle of one quarter turn."""
    first, second = section_semi_axes()
    angle = 0.6
    return (first * math.cos(angle), second * math.sin(angle), SECTION_HEIGHT)


def radial_integrand(radius: float) -> float:
    """Return $r^2 (1 - r^2)$, the radial factor of the integral."""
    return radius * radius * (1.0 - radius * radius)
