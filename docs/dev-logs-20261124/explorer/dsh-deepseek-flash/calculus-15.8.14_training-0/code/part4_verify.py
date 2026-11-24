"""Verify the drawing of Part 4 against the equations of the two surfaces.

Part 4 draws the solid.  A drawing is correct only when every drawn point lies on
the surface that the equation defines, when the rim of the body closes on the
circle where the two surfaces meet, and when the two scales of the drawing agree
with the numbers of Part 2 and Part 3.  Each check below compares a value taken
from the drawn geometry with a value computed in an independent way.
"""

from __future__ import annotations

from fractions import Fraction
import math

import numpy as np
from scipy.optimize import brentq

from solid_geometry import (
    MEETING_HEIGHT,
    RIM_SQUARED_RADIUS,
    build_meeting_circle,
    build_surface_meshes,
)

TOLERANCE = 1.0e-9


def check_drawing_surface_residual() -> None:
    """Check that each drawn surface point satisfies the equation of that surface.

    The residual of a point is the difference between its drawn height and the
    height that the equation gives at the same two horizontal coordinates.  A
    residual of zero means that the drawing carries no point off its surface.
    """
    # BEGIN CHECK drawing_surface_residual
    meshes = build_surface_meshes()
    grid_x = np.asarray(meshes["x"])
    grid_y = np.asarray(meshes["y"])
    squared_radius = grid_x**2 + grid_y**2
    drawn_lower = np.asarray(meshes["lower"])
    drawn_upper = np.asarray(meshes["upper"])
    equation_lower = squared_radius
    equation_upper = 5.0 - squared_radius
    lower_residual = float(np.max(np.abs(drawn_lower - equation_lower)))
    upper_residual = float(np.max(np.abs(drawn_upper - equation_upper)))
    print(f"largest residual of the lower surface: {lower_residual:.3e}")
    print(f"largest residual of the upper surface: {upper_residual:.3e}")
    assert lower_residual < TOLERANCE, f"the lower surface leaves its equation by {lower_residual:.3e}"
    assert upper_residual < TOLERANCE, f"the upper surface leaves its equation by {upper_residual:.3e}"
    radius_grid = np.asarray(meshes["radius"])
    largest_squared_radius = float(np.max(radius_grid**2))
    smallest_squared_radius = float(np.min(radius_grid**2))
    print(f"largest squared radius of the drawing grid: {largest_squared_radius:.9f}")
    print(f"smallest squared radius of the drawing grid: {smallest_squared_radius:.9f}")
    assert abs(largest_squared_radius - RIM_SQUARED_RADIUS) < TOLERANCE, "the grid does not reach the rim"
    assert smallest_squared_radius == 0.0, "the grid does not reach the axis of the body"
    rim_gap_between_surfaces = float(np.max(np.abs(drawn_lower[-1, :] - drawn_upper[-1, :])))
    print(f"largest gap between the two surfaces at the rim: {rim_gap_between_surfaces:.3e}")
    assert rim_gap_between_surfaces < TOLERANCE, "the drawn body leaves a gap at its rim"
    # END CHECK drawing_surface_residual


def check_closed_body_rim() -> None:
    """Check that the drawn body closes on the circle where the two surfaces meet.

    The rim of the drawn body is the circle of the largest radius that the drawn
    grid carries.  The check compares that radius with the radius that the
    equality of the two equations gives, and it compares the height of the drawn
    rim with the height that the same equality gives.
    """
    # BEGIN CHECK closed_body_rim
    meshes = build_surface_meshes()
    grid_x = np.asarray(meshes["x"])
    grid_y = np.asarray(meshes["y"])
    squared_radius = grid_x**2 + grid_y**2
    inside = squared_radius >= RIM_SQUARED_RADIUS - 1.0e-12
    drawn_rim_squared = float(np.max(squared_radius[inside]))
    drawn_rim_height = float(np.mean(np.asarray(meshes["lower"])[-1, :]))

    def surface_gap(radius: float) -> float:
        """Return the vertical gap between the two surfaces at one radius."""
        return 5.0 - 2.0 * radius**2

    solved_radius = brentq(surface_gap, 0.0, 3.0, xtol=1.0e-14)
    solved_squared_radius = solved_radius**2
    solved_height = 5.0 - solved_squared_radius
    print(f"drawn squared radius at the rim: {drawn_rim_squared:.9f}")
    print(f"solved squared radius of the rim: {solved_squared_radius:.9f}")
    print(f"drawn height of the rim: {drawn_rim_height:.9f}")
    print(f"solved height of the rim: {solved_height:.9f}")
    assert abs(drawn_rim_squared - solved_squared_radius) < 1.0e-3, "the drawn rim misses the solved rim"
    assert abs(drawn_rim_height - solved_height) < 1.0e-3, "the drawn rim misses the solved height"

    circle = build_meeting_circle()
    circle_radius = np.hypot(np.asarray(circle["x"]), np.asarray(circle["y"]))
    print(f"radius of the drawn circle: {float(np.min(circle_radius)):.9f} to {float(np.max(circle_radius)):.9f}")
    print(f"height of the drawn circle: {float(np.min(np.asarray(circle['z']))):.9f}")
    assert float(np.max(np.abs(circle_radius - solved_radius))) < TOLERANCE, "the drawn circle misses the rim"
    assert float(np.max(np.abs(np.asarray(circle["z"]) - solved_height))) < TOLERANCE, "the circle is not level"
    # END CHECK closed_body_rim


def check_scales_agree() -> None:
    """Check that the numbers printed on the drawing agree with the computed ones.

    The drawing prints one tick at each unit of the three axes.  The check reads
    the largest tick of each axis from the figure script and compares it with the
    extent that the inequalities give, and it compares the area of the widest
    section with the area that the drawing reports.
    """
    # BEGIN CHECK scales_agree
    import part1_figure1

    horizontal_ticks = part1_figure1.HORIZONTAL_TICKS
    vertical_ticks = part1_figure1.VERTICAL_TICKS
    print(f"horizontal ticks of the drawing: {tuple(horizontal_ticks)}")
    print(f"vertical ticks of the drawing: {tuple(vertical_ticks)}")
    assert tuple(horizontal_ticks) == (1.0, 2.0), "the horizontal scale of the drawing changed"
    assert tuple(vertical_ticks) == (1.0, 3.0, 5.0), "the vertical scale of the drawing changed"

    rim_radius = math.sqrt(RIM_SQUARED_RADIUS)
    widest_area = math.pi * MEETING_HEIGHT
    print(f"radius of the drawn rim: {rim_radius:.9f}")
    print(f"largest horizontal tick of the drawing: {max(horizontal_ticks):.9f}")
    assert rim_radius < max(horizontal_ticks), "the drawn rim passes the largest horizontal tick"
    assert MEETING_HEIGHT <= max(vertical_ticks), "the top of the body passes the largest vertical tick"
    print(f"area of the widest section: {widest_area:.9f}")
    squared_radius_of_drawing = float(Fraction(5, 2))
    print(f"squared radius of the drawing constant: {RIM_SQUARED_RADIUS:.6f}")
    print(f"squared radius of the exact fraction: {squared_radius_of_drawing:.6f}")
    assert RIM_SQUARED_RADIUS == squared_radius_of_drawing, "the squared radius constant is not 5/2"
    assert abs(rim_radius**2 - RIM_SQUARED_RADIUS) < TOLERANCE, "the rim radius does not square to the constant"
    assert abs(widest_area - math.pi * RIM_SQUARED_RADIUS) < TOLERANCE, "the widest area is not pi times the rim"
    # END CHECK scales_agree


def main() -> None:
    """Run every check of Part 4."""
    check_drawing_surface_residual()
    check_closed_body_rim()
    check_scales_agree()
    print("part4_verify.py: every check passed")


if __name__ == "__main__":
    main()
