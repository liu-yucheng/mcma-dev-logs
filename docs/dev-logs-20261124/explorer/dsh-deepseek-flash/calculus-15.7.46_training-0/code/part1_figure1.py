"""Draw Figure 1: the solid cone, its base disk, and one horizontal slice.

The figure labels each surface at a point that the equation of that surface
satisfies. It uses one axis-label mechanism for each axis, sets a tick on every
axis, and asserts that each text box lies inside the axes box before it writes
the PNG file.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.text import Text
from mpl_toolkits.mplot3d import proj3d
import importlib.metadata
import platform

HEIGHT = 1.0
"""The height h of the cone."""

SLICE_HEIGHT = 0.6
"""The height z0 of the drawn horizontal slice."""

FIGURE_PATH = Path(__file__).resolve().parent / "figures" / "part1_figure1.png"
"""The output path of the figure."""

WALL_ALPHA = 0.62
"""The opacity of the cone wall, above 0.5 so that the body reads as closed."""


def cone_surface(radius: np.ndarray, angle: np.ndarray) -> tuple[np.ndarray, ...]:
    """Return the Cartesian coordinates of the cone surface z = r.

    Args:
        radius: The array of radii from the z axis.
        angle: The array of angles in radians.

    Returns:
        The arrays x, y, and z of the surface.
    """
    radius_grid, angle_grid = np.meshgrid(radius, angle)
    return radius_grid * np.cos(angle_grid), radius_grid * np.sin(angle_grid), radius_grid


def disk(radius: float, height: float) -> tuple[np.ndarray, ...]:
    """Return the Cartesian coordinates of a horizontal disk.

    Args:
        radius: The radius of the disk.
        height: The z coordinate of the disk.

    Returns:
        The arrays x, y, and z of the disk.
    """
    angle = np.linspace(0.0, 2.0 * np.pi, 181)
    radius_grid = np.linspace(0.0, radius, 60)
    radius_mesh, angle_mesh = np.meshgrid(radius_grid, angle)
    return (radius_mesh * np.cos(angle_mesh), radius_mesh * np.sin(angle_mesh),
            np.full_like(radius_mesh, height))


def inside_axes(axes: plt.Axes, text: Text, renderer: object) -> bool:
    """Return True when the drawn box of a three-dimensional text lies inside the axes box.

    The projection of the anchor point comes from ``proj3d.proj_transform``, and the size of
    the box comes from the text renderer, because a three-dimensional text reports a box in
    data units and not in display units.

    Args:
        axes: The axes that holds the text.
        text: The text object.
        renderer: The renderer of the canvas.

    Returns:
        True when the text box lies fully inside the axes box.
    """
    position = text.get_position_3d()
    projected = proj3d.proj_transform(position[0], position[1], position[2], axes.get_proj())
    display_x, display_y = axes.transData.transform((projected[0], projected[1]))
    width, height, _ = renderer.get_text_width_height_descent(
        text.get_text(), text.get_fontproperties(), ismath=True
    )
    axes_box = axes.bbox
    return bool(
        display_x - width / 2.0 >= axes_box.x0
        and display_y - height / 2.0 >= axes_box.y0
        and display_x + width / 2.0 <= axes_box.x1
        and display_y + height / 2.0 <= axes_box.y1
    )


def report_environment() -> None:
    """Print the version of each tool, so that the figure repeats."""
    package_names = ("numpy", "matplotlib")
    versions = ", ".join(
        f"{name} {importlib.metadata.version(name)}" for name in package_names
    )
    print(f"Python {platform.python_version()}, {versions}")


def main() -> None:
    """Draw the figure, check the label positions, and write the PNG file."""
    report_environment()
    figure = plt.figure(figsize=(7.4, 6.6))
    axes = figure.add_subplot(111, projection="3d")
    axes.computed_zorder = False

    radius = np.linspace(0.0, HEIGHT, 60)
    angle = np.linspace(0.0, 2.0 * np.pi, 121)
    x_surface, y_surface, z_surface = cone_surface(radius, angle)
    axes.plot_surface(x_surface, y_surface, z_surface, color="#8fbde4", alpha=WALL_ALPHA,
                      linewidth=0.0, antialiased=True, zorder=2)
    boundary_angle = np.linspace(0.0, 2.0 * np.pi, 361)
    axes.plot(HEIGHT * np.cos(boundary_angle), HEIGHT * np.sin(boundary_angle),
              np.full_like(boundary_angle, HEIGHT), color="#1f4e79", linewidth=1.6, zorder=3)

    x_base, y_base, z_base = disk(HEIGHT, HEIGHT)
    axes.plot_surface(x_base, y_base, z_base, color="#f0c98a", alpha=0.42, linewidth=0.0,
                      zorder=3)
    x_slice, y_slice, z_slice = disk(SLICE_HEIGHT, SLICE_HEIGHT)
    axes.plot_surface(x_slice, y_slice, z_slice, color="#eaa07f", alpha=0.88, linewidth=0.0,
                      zorder=4)
    axes.plot(SLICE_HEIGHT * np.cos(boundary_angle), SLICE_HEIGHT * np.sin(boundary_angle),
              np.full_like(boundary_angle, SLICE_HEIGHT), color="#8c2f1e", linewidth=2.4,
              zorder=5)

    axes.plot([0.0, 0.0], [0.0, 0.0], [0.0, 1.18 * HEIGHT], color="#333333", linewidth=1.0,
              linestyle="--", zorder=1.5)
    axes.plot([0.0, SLICE_HEIGHT - 0.07], [0.0, 0.0], [SLICE_HEIGHT, SLICE_HEIGHT],
              color="#8c2f1e", linewidth=1.8, zorder=6)

    label_box = {"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "#c8ccd2",
                 "alpha": 0.92}
    cone_anchor = (-0.40 * np.cos(np.deg2rad(18.0)), -0.40 * np.sin(np.deg2rad(18.0)), 0.40)
    cone_label_point = (-0.86, -0.16, 0.52)
    axes.plot([cone_anchor[0] * 1.08, cone_label_point[0] + 0.06],
              [cone_anchor[1] * 1.08, cone_label_point[1] + 0.012],
              [cone_anchor[2] * 1.08, cone_label_point[2] - 0.004],
              color="#5a6b7d", linewidth=0.8)
    label_cone = axes.text(
        cone_label_point[0], cone_label_point[1], cone_label_point[2],
        r"$z=\sqrt{x^{2}+y^{2}}$", fontsize=11, color="#1f4e79", ha="center", va="center",
        bbox=label_box, zorder=20,
    )

    base_anchor = (HEIGHT * np.cos(np.deg2rad(24.0)), HEIGHT * np.sin(np.deg2rad(24.0)), HEIGHT)
    base_label_point = (0.92, 0.52, 1.16)
    axes.plot([base_anchor[0] * 0.98, base_label_point[0] - 0.03],
              [base_anchor[1] * 0.98, base_label_point[1] - 0.03],
              [HEIGHT + 0.004, base_label_point[2] - 0.008],
              color="#5a6b7d", linewidth=0.8)
    label_base = axes.text(
        base_label_point[0], base_label_point[1], base_label_point[2],
        r"$z=h$", fontsize=11, color="#7a5310", ha="center", va="center",
        bbox=label_box, zorder=20,
    )

    slice_anchor = (SLICE_HEIGHT * np.cos(np.deg2rad(-42.0)),
                    SLICE_HEIGHT * np.sin(np.deg2rad(-42.0)), SLICE_HEIGHT)
    slice_label_point = (0.62, -0.86, 0.50)
    axes.plot([slice_anchor[0] * 1.06, slice_label_point[0] - 0.02],
              [slice_anchor[1] * 1.06, slice_label_point[1] + 0.02],
              [SLICE_HEIGHT, slice_label_point[2] + 0.04],
              color="#b5432f", linewidth=0.9)
    label_slice = axes.text(
        slice_label_point[0], slice_label_point[1], slice_label_point[2],
        r"slice at $z=z_{0}$", fontsize=10.5, color="#b5432f", ha="center", va="center",
        bbox=label_box, zorder=20,
    )

    label_radius = axes.text(
        0.30, 0.0, SLICE_HEIGHT + 0.03, r"$r=z_{0}$", fontsize=10, color="#8c2f1e",
        ha="center", va="bottom", bbox=label_box, zorder=20,
    )

    axes.set_xlabel("$x$", fontsize=12, labelpad=1)
    axes.set_ylabel("$y$", fontsize=12, labelpad=1)
    axes.set_zlabel("$z$", fontsize=12, labelpad=2)
    axes.set_xticks([-HEIGHT, 0.0, HEIGHT])
    axes.set_yticks([-HEIGHT, 0.0, HEIGHT])
    axes.set_zticks([0.0, HEIGHT / 2.0, HEIGHT])
    axes.set_xticklabels(["$-h$", "$0$", "$h$"], fontsize=9)
    axes.set_yticklabels(["$-h$", "$0$", "$h$"], fontsize=9)
    axes.set_zticklabels(["$0$", "$h/2$", "$h$"], fontsize=9)
    axes.set_xlim(-1.05 * HEIGHT, 1.05 * HEIGHT)
    axes.set_ylim(-1.05 * HEIGHT, 1.05 * HEIGHT)
    axes.set_zlim(0.0, 1.22 * HEIGHT)
    axes.view_init(elev=20.0, azim=-56.0)
    axes.set_box_aspect((1.0, 1.0, 0.95))
    axes.set_title("Solid cone $\\sqrt{x^{2}+y^{2}}\\leq z\\leq h$ with one slice", fontsize=12)

    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    for name, text in (("cone", label_cone), ("base", label_base), ("slice", label_slice),
                       ("radius", label_radius)):
        inside = inside_axes(axes, text, renderer)
        print(f"label {name} inside the axes box: computed = {inside}, expected = True")
        assert inside, f"the label {name} leaves the axes box"
    for name, point in (("cone", cone_anchor), ("base", base_anchor), ("slice", slice_anchor)):
        print(f"label {name} at a point of its surface: z = {point[2]:.4f}, "
              f"r = {float(np.hypot(point[0], point[1])):.4f}")

    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(FIGURE_PATH, dpi=200, bbox_inches="tight")
    print(f"figure written: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
