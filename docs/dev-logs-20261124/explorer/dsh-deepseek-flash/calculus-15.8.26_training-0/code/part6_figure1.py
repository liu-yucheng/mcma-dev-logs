"""Draw figure 3: the sphere and the cylinder on the same screen, with their cut.

The sphere has radius $a$. The cylinder is the sheet $r = a\cos\theta$, drawn only
between the two heights that the sphere allows, so that the drawn sheet is the wall
of the solid of part (a). The thick curve is the intersection of the two surfaces.

Run with ``code/.venv/Scripts/python.exe code/part6_figure1.py``.
"""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

import figure_anchors as anchors
import figure_helpers as helpers
import solid_geometry as geometry

RADIUS = geometry.REFERENCE_RADIUS


def sphere_mesh(sample_count: int = 70) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return one mesh of the sphere of the reference radius.

    Args:
        sample_count: Number of samples of each parameter.

    Returns:
        The arrays of the three coordinates.
    """
    polar = np.linspace(0.0, math.pi, sample_count)
    azimuth = np.linspace(0.0, 2.0 * math.pi, 2 * sample_count)
    polar_grid, azimuth_grid = np.meshgrid(polar, azimuth)
    return (
        RADIUS * np.sin(polar_grid) * np.cos(azimuth_grid),
        RADIUS * np.sin(polar_grid) * np.sin(azimuth_grid),
        RADIUS * np.cos(polar_grid),
    )


def cylinder_mesh(sample_count: int = 60) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return one mesh of the wall that the cylinder cuts out of the sphere.

    Args:
        sample_count: Number of samples of the angle.

    Returns:
        The arrays of the three coordinates.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, sample_count)
    heights = np.linspace(-1.0, 1.0, sample_count)
    angle_grid, height_grid = np.meshgrid(angles, heights)
    radial = RADIUS * np.cos(angle_grid)
    return (
        radial * np.cos(angle_grid),
        radial * np.sin(angle_grid),
        height_grid * RADIUS * np.abs(np.sin(angle_grid)),
    )


def intersection_curve(sample_count: int = 400) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return both branches of the curve where the two surfaces meet.

    Args:
        sample_count: Number of samples of the angle.

    Returns:
        The arrays of the three coordinates of the upper branch and of the lower branch.
    """
    angles = np.linspace(-math.pi / 2.0, math.pi / 2.0, sample_count)
    radial = RADIUS * np.cos(angles)
    x_values = radial * np.cos(angles)
    y_values = radial * np.sin(angles)
    z_values = RADIUS * np.abs(np.sin(angles))
    return x_values, y_values, z_values


def main() -> None:
    """Draw the three surfaces of part (b) and check the label positions."""
    helpers.apply_style()
    figure = plt.figure(figsize=(6.8, 6.0))
    axes = figure.add_subplot(111, projection="3d")
    figure.subplots_adjust(left=0.0, right=1.0, bottom=0.02, top=0.98)

    sphere_x, sphere_y, sphere_z = sphere_mesh()
    axes.plot_surface(
        sphere_x,
        sphere_y,
        sphere_z,
        color=helpers.SPHERE_FILL,
        alpha=0.16,
        linewidth=0.0,
        shade=False,
        zorder=2,
    )

    wall_x, wall_y, wall_z = cylinder_mesh()
    axes.plot_surface(
        wall_x,
        wall_y,
        wall_z,
        color=helpers.CYLINDER_FILL,
        alpha=0.55,
        linewidth=0.0,
        shade=False,
        zorder=4,
    )

    for angle_value in (-1.2, -0.8, -0.4, 0.0, 0.4, 0.8, 1.2):
        radial_value = RADIUS * math.cos(angle_value)
        heights = np.linspace(-RADIUS * abs(math.sin(angle_value)), RADIUS * abs(math.sin(angle_value)), 40)
        axes.plot(
            np.full_like(heights, radial_value * math.cos(angle_value)),
            np.full_like(heights, radial_value * math.sin(angle_value)),
            heights,
            color="#a97c37",
            linewidth=0.6,
            zorder=6,
        )
    for latitude in (-0.6, -0.3, 0.3, 0.6):
        chord = math.sqrt(RADIUS**2 - latitude**2)
        angles = np.linspace(0.0, 2.0 * math.pi, 200)
        axes.plot(
            chord * np.cos(angles),
            chord * np.sin(angles),
            np.full_like(angles, latitude),
            color="#9bb3c2",
            linewidth=0.6,
            zorder=3,
        )

    curve_x, curve_y, curve_z = intersection_curve()
    axes.plot(curve_x, curve_y, curve_z, color=helpers.CURVE_COLOR, linewidth=2.1, zorder=10)
    axes.plot(curve_x, curve_y, -curve_z, color=helpers.CURVE_COLOR, linewidth=2.1, zorder=10)

    extent = anchors.AXIS_EXTENT
    geometry.draw_arrowed_axis(axes, (0.0, 0.0, 0.0), (extent, 0.0, 0.0))
    geometry.draw_arrowed_axis(axes, (0.0, 0.0, 0.0), (0.0, extent, 0.0))
    geometry.draw_arrowed_axis(axes, (0.0, 0.0, -extent), (0.0, 0.0, extent))

    texts = [
        geometry.place_axis_letter(axes, "$x$", (extent + 0.06, 0.0, 0.0)),
        geometry.place_axis_letter(axes, "$y$", (0.0, extent + 0.06, 0.0)),
        geometry.place_axis_letter(axes, "$z$", (0.0, 0.0, extent + 0.07)),
        geometry.draw_numeric_tick(axes, (RADIUS, 0.0, 0.0), (0.0, -0.10, 0.0), r"$a$"),
    ]

    sphere_label = anchors.SPHERE_LABEL_ANCHOR
    texts.append(
        axes.text(
            sphere_label[0],
            sphere_label[1],
            sphere_label[2],
            r"$x^{2} + y^{2} + z^{2} = a^{2}$",
            fontsize=9.5,
            color=helpers.MUTED,
            ha="center",
            va="center",
            zorder=30,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2, "alpha": 0.85},
        )
    )

    wall_radius = RADIUS * math.cos(anchors.CYLINDER_LABEL_ANGLE)
    wall_x_point = wall_radius * math.cos(anchors.CYLINDER_LABEL_ANGLE)
    wall_y_point = wall_radius * math.sin(anchors.CYLINDER_LABEL_ANGLE)
    texts.append(
        axes.text(
            wall_x_point,
            wall_y_point,
            anchors.CYLINDER_LABEL_HEIGHT,
            r"$r = a\cos\theta$",
            fontsize=9.5,
            color="#8a6224",
            ha="center",
            va="center",
            zorder=30,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2, "alpha": 0.85},
        )
    )

    solid_radius = anchors.SOLID_LABEL_RADIUS
    texts.append(
        axes.text(
            solid_radius * math.cos(anchors.SOLID_LABEL_ANGLE),
            solid_radius * math.sin(anchors.SOLID_LABEL_ANGLE),
            anchors.SOLID_LABEL_HEIGHT,
            r"solid $E$",
            fontsize=9.5,
            color=helpers.INK,
            ha="center",
            va="center",
            zorder=30,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2, "alpha": 0.85},
        )
    )

    axes.set_xlim(-1.15, 1.45)
    axes.set_ylim(-1.45, 1.45)
    axes.set_zlim(-1.35, 1.35)
    axes.set_box_aspect((1.0, 1.0, 0.95))
    axes.view_init(elev=20.0, azim=-60.0)
    axes.set_axis_off()

    assert len(texts) >= 7, "the figure must carry three axis letters, one tick, and three labels"
    margins = helpers.content_margins(figure)
    smallest = min(margins.values())
    assert smallest >= 4, f"the drawn content reaches the canvas edge, smallest margin {smallest} pixels"
    print(f"CHECK figure3_content_inside_canvas min_margin={smallest} pixels")
    helpers.save_figure(figure, "part6_figure1.png")


if __name__ == "__main__":
    main()
