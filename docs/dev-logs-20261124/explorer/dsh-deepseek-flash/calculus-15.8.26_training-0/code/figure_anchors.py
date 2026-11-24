"""Hold the coordinates that the figures use as label positions and as marked points.

One module holds these coordinates, so that a figure and its check read the same
numbers. The check script ``part6_verify.py`` puts each coordinate into the equation
of the surface that the label names and prints the residual.
"""

from __future__ import annotations

from typing import Final

# Figure 1 and figure 2 work in the plane of the reference radius a = 1.

RADIAL_ANGLE: Final[float] = 0.7853981633974483  # pi / 4
CELL_INNER_RADIUS: Final[float] = 0.30
CELL_OUTER_RADIUS: Final[float] = 0.52
CELL_ANGLE_START: Final[float] = 0.35
CELL_ANGLE_END: Final[float] = 0.90
SIDE_VIEW_ANGLE: Final[float] = 0.60

# Three dimensional label positions. Each triple must satisfy the equation of the
# surface whose name the label carries.

SPHERE_LABEL_ANCHOR: Final[tuple[float, float, float]] = (-0.4479, -0.6171, 0.6469)
CYLINDER_LABEL_ANGLE: Final[float] = 1.15
CYLINDER_LABEL_HEIGHT: Final[float] = 0.55
SOLID_LABEL_RADIUS: Final[float] = 0.50
SOLID_LABEL_ANGLE: Final[float] = 0.40
SOLID_LABEL_HEIGHT: Final[float] = 0.0
AXIS_EXTENT: Final[float] = 1.30
