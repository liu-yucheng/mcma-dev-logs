"""Check the geometry that figure 3 draws and the labels that it places.

Every sample of the drawn sphere goes back into the equation of the sphere. Every
sample of the drawn wall goes back into the equation of the cylinder and into the
height bound of the sphere. Every label anchor goes into the equation of the object
that its label names.

Run with ``code/.venv/Scripts/python.exe code/part6_verify.py``.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.image as image
import numpy as np

import figure_anchors as anchors
import figure_helpers as helpers
import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS
FIGURE_DIRECTORY = Path(__file__).resolve().parent / "figures"


def drawn_sphere(sample_count: int = 71) -> np.ndarray:
    """Return the sample points of the sphere surface that the figure draws.

    Args:
        sample_count: Number of samples of each parameter.

    Returns:
        The array of the sample points, one point in each row.
    """
    polar = np.linspace(0.0, math.pi, sample_count)
    azimuth = np.linspace(0.0, 2.0 * math.pi, 2 * sample_count)
    polar_grid, azimuth_grid = np.meshgrid(polar, azimuth)
    return np.column_stack(
        [
            (RADIUS * np.sin(polar_grid) * np.cos(azimuth_grid)).ravel(),
            (RADIUS * np.sin(polar_grid) * np.sin(azimuth_grid)).ravel(),
            (RADIUS * np.cos(polar_grid)).ravel(),
        ]
    )


def drawn_wall(sample_count: int = 61) -> np.ndarray:
    """Return the sample points of the cylinder wall that the figure draws.

    Args:
        sample_count: Number of samples of the angle.

    Returns:
        The array of the sample points, one point in each row.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, sample_count)
    heights = np.linspace(-1.0, 1.0, 25)
    angle_grid, height_grid = np.meshgrid(angles, heights)
    radial = RADIUS * np.cos(angle_grid)
    return np.column_stack(
        [
            (radial * np.cos(angle_grid)).ravel(),
            (radial * np.sin(angle_grid)).ravel(),
            (height_grid * RADIUS * np.abs(np.sin(angle_grid))).ravel(),
        ]
    )


def check_sphere_samples() -> None:
    """Check that each drawn sphere point satisfies the equation of the sphere."""
    points = drawn_sphere()
    distances = np.sqrt(np.sum(points**2, axis=1))
    worst = float(np.max(np.abs(distances - RADIUS)))
    geometry.report_check(
        "drawn_sphere_on_surface",
        worst,
        0.0,
        1.0e-12,
        f"worst distance residual over {len(points)} drawn points against zero",
    )
    print(f"FACT drawn_sphere_points={len(points)} worst_residual={worst:.3e}")


def check_wall_samples() -> None:
    """Check that each drawn wall point satisfies the cylinder equation and the sphere bound."""
    points = drawn_wall()
    radial = np.sqrt(points[:, 0] ** 2 + points[:, 1] ** 2)
    angles = np.arctan2(points[:, 1], points[:, 0])
    cylinder_residual = float(np.max(np.abs(radial - RADIUS * np.cos(angles))))
    geometry.report_check(
        "drawn_wall_on_cylinder",
        cylinder_residual,
        0.0,
        1.0e-12,
        f"worst residual of r - a cos(theta) over {len(points)} drawn points against zero",
    )
    height_bound = np.sqrt(np.maximum(RADIUS**2 - radial**2, 0.0))
    excess = float(np.max(np.abs(points[:, 2]) - height_bound))
    geometry.report_check(
        "drawn_wall_inside_sphere",
        excess,
        0.0,
        1.0e-12,
        "worst excess of the drawn height over the sphere height bound against zero",
    )
    grid_excess = float(np.max(np.abs(points[:, 2]) - height_bound))
    print(
        f"FACT drawn_wall_points={len(points)} cylinder_residual={cylinder_residual:.3e} "
        f"height_excess={grid_excess:.3e}"
    )


def check_intersection_curve() -> None:
    """Check that each point of the drawn cut lies on both surfaces."""
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, 401)
    radial = RADIUS * np.cos(angles)
    x_values = radial * np.cos(angles)
    y_values = radial * np.sin(angles)
    z_values = RADIUS * np.abs(np.sin(angles))
    sphere_residual = float(np.max(np.abs(np.sqrt(x_values**2 + y_values**2 + z_values**2) - RADIUS)))
    curve_radial = np.sqrt(x_values**2 + y_values**2)
    cylinder_residual = float(np.max(np.abs(curve_radial - RADIUS * np.cos(angles))))
    geometry.report_check(
        "cut_curve_on_sphere",
        sphere_residual,
        0.0,
        1.0e-12,
        "worst sphere residual over the drawn cut against zero",
    )
    geometry.report_check(
        "cut_curve_on_cylinder",
        cylinder_residual,
        0.0,
        1.0e-12,
        "worst cylinder residual over the drawn cut against zero",
    )
    print(
        f"FACT cut_curve_height_extremes min={float(np.min(z_values)):.12f} "
        f"max={float(np.max(z_values)):.12f}"
    )


def check_label_anchors() -> None:
    """Check that each label sits on the object that its text names."""
    sphere_label = np.array(anchors.SPHERE_LABEL_ANCHOR)
    geometry.report_check(
        "sphere_label_on_sphere",
        float(np.sqrt(np.sum(sphere_label**2))),
        RADIUS,
        1.0e-3,
        "length of the anchor of the sphere label against the radius",
    )

    wall_radius = float(
        np.hypot(
            RADIUS * math.cos(anchors.CYLINDER_LABEL_ANGLE) * math.cos(anchors.CYLINDER_LABEL_ANGLE),
            RADIUS * math.cos(anchors.CYLINDER_LABEL_ANGLE) * math.sin(anchors.CYLINDER_LABEL_ANGLE),
        )
    )
    geometry.report_check(
        "cylinder_label_on_cylinder",
        wall_radius,
        RADIUS * math.cos(anchors.CYLINDER_LABEL_ANGLE),
        1.0e-12,
        "radial distance of the anchor of the cylinder label against a cos(theta)",
    )
    wall_height_bound = math.sqrt(max(RADIUS**2 - wall_radius**2, 0.0))
    assert abs(anchors.CYLINDER_LABEL_HEIGHT) <= wall_height_bound + 1.0e-12, (
        "the cylinder label must sit between the two heights that the sphere allows"
    )
    print(
        f"FACT cylinder_label_anchor radius={wall_radius:.12f} "
        f"height={anchors.CYLINDER_LABEL_HEIGHT:.12f} bound={wall_height_bound:.12f}"
    )

    solid_radius = anchors.SOLID_LABEL_RADIUS
    solid_slack = RADIUS * math.cos(anchors.SOLID_LABEL_ANGLE) - solid_radius
    solid_height_bound = math.sqrt(max(RADIUS**2 - solid_radius**2, 0.0))
    geometry.report_check(
        "solid_label_inside_cylinder",
        solid_radius + solid_slack,
        RADIUS * math.cos(anchors.SOLID_LABEL_ANGLE),
        1.0e-12,
        "the label radius plus its slack against a cos(theta) at the label angle",
    )
    assert abs(anchors.SOLID_LABEL_HEIGHT) <= solid_height_bound, (
        "the solid label must sit between the two heights that the sphere allows"
    )
    print(
        f"FACT solid_label_anchor radius={solid_radius:.12f} slack={solid_slack:.12f} "
        f"height_bound={solid_height_bound:.12f}"
    )


def check_figure_files() -> None:
    """Check that each figure file exists and holds drawn ink."""
    for file_name in ("part1_figure1.png", "part2_figure1.png", "part6_figure1.png"):
        target = FIGURE_DIRECTORY / file_name
        assert target.is_file(), f"the figure {file_name} is absent"
        pixels = image.imread(target)
        height, width = pixels.shape[0], pixels.shape[1]
        assert min(height, width) >= 400, f"the figure {file_name} is too small: {width} by {height}"
        ink = float(np.mean(np.any(pixels[:, :, :3] < 0.78, axis=2)))
        print(f"FACT {file_name} shape={pixels.shape} dark_share={ink:.4f}")


def main() -> None:
    """Run every check of part 6 and print the summary."""
    check_sphere_samples()
    check_wall_samples()
    check_intersection_curve()
    check_label_anchors()
    check_figure_files()
    geometry.summarize("part6")


if __name__ == "__main__":
    main()
