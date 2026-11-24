"""Hold the geometric constants that the figures and the verification scripts share.

A number that a figure draws must come from this module, so that a script can print the same number.
"""

from __future__ import annotations

CYLINDER_RADIUS = 3.0
"""Radius of the cylinder, the square root of the number 9 of the statement."""

PLANE_SLOPE = 3.0
"""Slope of the plane that the statement writes as y = 3x."""

SAMPLE_HEIGHTS_Y = (0.6, 1.5, 2.7)
"""Heights y at which the verification script samples the area of a slice at fixed y."""

SAMPLE_HEIGHTS_Z = (0.0, 1.5, 3.0)
"""Heights z at which the verification script samples the area of a slice at fixed z."""

SHAPE_HEIGHTS_Y = (0.0, 1.5, 3.0)
"""Heights y, including both limits, at which the shape table names the slice."""

SHAPE_HEIGHTS_Z = (0.0, 1.5, 3.0)
"""Heights z, including both limits, at which the shape table names the slice."""

DEMO_HEIGHT_Y = 1.5
"""Height y of the slice that the slice figure draws and that the page quotes."""

SURFACE_LABEL_POINTS = {
    "cylinder": (0.80, 2.598076211353316, 1.50),
    "plane_x_zero": (0.00, 0.60, 2.60),
    "plane_y_three_x": (0.60, 1.80, 1.00),
    "plane_z_zero": (0.50, 1.50, 0.00),
}
"""One point for each boundary surface, chosen on that surface and inside the solid."""

SURFACE_ALPHA = 0.55
"""Opacity of each boundary surface, above one half so that the solid reads as a closed body."""

FIGURE_DPI = 190
"""Resolution of every exported figure."""

GRID_SIDE = 2001
"""Number of sample points on each side of a two-dimensional counting grid."""

RANDOM_SEED = 20261123
"""Seed of every random sample of the session."""

MONTE_CARLO_SAMPLE_COUNT = 4_000_000
"""Number of points of the Monte Carlo estimate of the integral."""
