"""Verify the projection and the drawing recipe of Part 6.

Each check compares two computations: the projection of the body from the ceiling inequality
against the silhouette of the drawing, the half width of the silhouette from a scan of the
membership test against the closed form, and a polyline length against the closed form.
"""

import math

import numpy as np

from figure_anchors import (
    AXIS_LABEL_INSET,
    AXIS_X_MAXIMUM,
    AXIS_X_MINIMUM,
    AXIS_Y_MAXIMUM,
    AXIS_Y_MINIMUM,
    AXIS_Z_MAXIMUM,
    AXIS_Z_MINIMUM,
    label_anchor_table,
    meridian_half_width,
    zoom_limits,
)
from silo_geometry import (
    APEX_HEIGHT,
    CAP_RADIUS,
    CAP_CENTER_HEIGHT,
    CYLINDER_HEIGHT,
    CYLINDER_RADIUS,
    base_mesh,
    cap_mesh,
    cap_residual,
    lateral_mesh,
    lateral_residual,
    projection_region_from_ceiling,
    projection_region_from_shapes,
    surface_area_by_mesh,
    exposed_surface_area,
)
from verification_report import CheckLog

GRID_X_COUNT = 481
"""Number of sampled values of x in the projection comparison."""

GRID_Z_COUNT = 451
"""Number of sampled values of z in the projection comparison."""

COARSE_RESOLUTION = 12
"""Resolution of the coarse mesh of the drawing figure."""

FINE_RESOLUTION = 72
"""Resolution of the fine mesh of the drawing figure."""

TOLERANCE = 1.0e-12
"""Tolerance of an algebraic identity, in the unit of length of the exercise."""


def projection_disagreement_count() -> int:
    """Return the number of sampled points where the two projection descriptions disagree."""
    disagreements = 0
    for x_value in np.linspace(-3.6, 3.6, GRID_X_COUNT):
        for z_value in np.linspace(-0.3, 13.3, GRID_Z_COUNT):
            if projection_region_from_ceiling(float(x_value), float(z_value)) != (
                projection_region_from_shapes(float(x_value), float(z_value))
            ):
                disagreements += 1
    return disagreements


def half_width_by_scan(height: float) -> float:
    """Return the half width of the projection at a height, by a bisection on the inequality."""
    if not projection_region_from_ceiling(0.0, height):
        return 0.0
    low = 0.0
    high = 4.0
    for _ in range(120):
        middle = 0.5 * (low + high)
        if projection_region_from_ceiling(middle, height):
            low = middle
        else:
            high = middle
    return 0.5 * (low + high)


def outline_length() -> float:
    """Return the length of the outline of the meridian silhouette as a polyline."""
    points = [(-CYLINDER_RADIUS, 0.0)]
    for height in np.linspace(0.0, APEX_HEIGHT, 4001):
        points.append((meridian_half_width(float(height)), float(height)))
    for height in np.linspace(APEX_HEIGHT, 0.0, 4001):
        points.append((-meridian_half_width(float(height)), float(height)))
    points.append((-CYLINDER_RADIUS, 0.0))
    total = 0.0
    for index in range(len(points) - 1):
        first = points[index]
        second = points[index + 1]
        total += math.hypot(second[0] - first[0], second[1] - first[1])
    return total


def main() -> None:
    """Run every check of Part 6 and write the summary table."""
    log = CheckLog("part6")

    disagreements = projection_disagreement_count()
    sample_count = GRID_X_COUNT * GRID_Z_COUNT
    log.record(
        f"C1 projection: ceiling inequality against the rectangle plus half disk on "
        f"{sample_count} points",
        float(disagreements),
        0.0,
        float(disagreements),
        disagreements == 0,
    )

    panel = (0.0, 4.0, 9.0, 10.0, 11.5, 12.5, 12.95)
    errors = []
    print("height | half width by scan | meridian half width", flush=True)
    for height in panel:
        by_scan = half_width_by_scan(height)
        by_formula = meridian_half_width(height)
        errors.append(abs(by_scan - by_formula))
        print(f"{height:6.2f} | {by_scan:.12f} | {by_formula:.12f}", flush=True)
    worst = max(errors)
    log.record(
        "C2 silhouette: scan of the inequality against the meridian formula, 7 heights",
        worst,
        0.0,
        worst,
        worst < 1.0e-6,
    )

    lateral_nodes, _lateral_triangles = lateral_mesh(48, 40)
    cap_nodes, _cap_triangles = cap_mesh(48, 24)
    base_nodes, _base_triangles = base_mesh(48, 24)
    lateral_error = max(abs(lateral_residual(*node)) for node in lateral_nodes)
    cap_error = max(abs(cap_residual(*node)) for node in cap_nodes)
    base_error = max(abs(node[2]) for node in base_nodes)
    log.record(
        "C3 mesh nodes: lateral, cap, and base residuals against their own equations",
        max(lateral_error, cap_error, base_error),
        0.0,
        max(lateral_error, cap_error, base_error),
        max(lateral_error, cap_error, base_error) < TOLERANCE,
    )

    z_headroom = AXIS_Z_MAXIMUM - APEX_HEIGHT
    x_headroom = AXIS_X_MAXIMUM - CYLINDER_RADIUS
    y_headroom = AXIS_Y_MAXIMUM - CYLINDER_RADIUS
    log.record(
        "C4 drawing headroom: z headroom, x headroom, y headroom against the label inset",
        min(z_headroom, x_headroom, y_headroom),
        AXIS_LABEL_INSET,
        min(z_headroom, x_headroom, y_headroom) - AXIS_LABEL_INSET,
        min(z_headroom, x_headroom, y_headroom) > AXIS_LABEL_INSET,
    )

    anchor_failures = 0
    x_minimum, x_maximum, y_minimum, y_maximum, z_minimum, z_maximum = zoom_limits()
    for _name, point, _equation in label_anchor_table():
        if not (x_minimum <= point[0] <= x_maximum):
            anchor_failures += 1
        if not (y_minimum <= point[1] <= y_maximum):
            anchor_failures += 1
        if not (z_minimum <= point[2] <= z_maximum):
            anchor_failures += 1
    log.record(
        "C5 label anchors: distance from the axes box, three anchors against three limits",
        float(anchor_failures),
        0.0,
        float(anchor_failures),
        anchor_failures == 0,
    )

    numeric_outline = outline_length()
    closed_outline = 2.0 * CYLINDER_HEIGHT + 2.0 * CYLINDER_RADIUS + math.pi * CAP_RADIUS
    log.record(
        "C6 outline: polyline length against $2\\cdot 10+2\\cdot 3+3\\pi$",
        numeric_outline,
        closed_outline,
        abs(numeric_outline - closed_outline),
        abs(numeric_outline - closed_outline) < 1.0e-3,
    )

    coarse_area = surface_area_by_mesh(COARSE_RESOLUTION)
    fine_area = surface_area_by_mesh(FINE_RESOLUTION)
    coarse_error = abs(coarse_area - exposed_surface_area())
    fine_error = abs(fine_area - exposed_surface_area())
    log.record(
        "C7 mesh resolution: coarse error against fine error, the fine error must be smaller",
        coarse_error,
        fine_error,
        coarse_error - fine_error,
        fine_error < coarse_error / 10.0,
    )

    node_counts = (len(lateral_nodes) + len(cap_nodes) + len(base_nodes))
    coarse_nodes = len(lateral_mesh(COARSE_RESOLUTION, COARSE_RESOLUTION)[0])
    print(f"heights of the silhouette panel: {panel}", flush=True)
    print(f"outline length {numeric_outline:.9f}, closed form {closed_outline:.9f}", flush=True)
    print(f"fine mesh nodes {node_counts}, coarse lateral nodes {coarse_nodes}", flush=True)
    print(f"coarse area {coarse_area:.6f}, fine area {fine_area:.6f}, "
          f"closed form {exposed_surface_area():.6f}", flush=True)
    log.require_all_passed()
    log.write()


if __name__ == "__main__":
    main()
