"""Draw Figure 1: the solid E and one section of E at a fixed x.

The left panel draws the four surfaces that bound E, and it labels each surface at a point that
satisfies the equation of that surface. The right panel draws the section of E at x = 0.6. The
section is the triangle 0 <= z <= y <= Y, where Y = sqrt(1 - 0.6^2). The script writes
`code/figures/part1_figure1.png` and it asserts that every annotation and the legend lie inside
the box of their axes.
"""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

import common_region as region

SECTION_X = 0.6
"""The fixed x of the section that the right panel draws."""

SURFACE_LABELS = (
    ("$x^2+y^2=1$", (0.5817, 0.8134, 0.35)),
    ("$z=y$", (0.25, 0.60, 0.60)),
    ("$z=0$", (0.25, 0.30, 0.0)),
    ("$x=0$", (0.0, 0.95, 0.85)),
)
"""The label of each boundary surface and one point that satisfies its equation."""


def draw_solid(axes: plt.Axes) -> None:
    """Draw the four boundary surfaces of E in a three-dimensional box."""
    angle = np.linspace(0.0, math.pi / 2.0, 61)
    cosine = np.cos(angle)
    sine = np.sin(angle)

    wall_angle, wall_height = np.meshgrid(angle, np.linspace(0.0, 1.0, 31))
    wall_x = np.cos(wall_angle)
    wall_y = np.sin(wall_angle)
    wall_z = wall_height * np.sin(wall_angle)
    axes.plot_surface(wall_x, wall_y, wall_z, color="#4c78a8", alpha=0.55, linewidth=0.0)

    radius = np.linspace(0.0, 1.0, 41)
    disk_angle, disk_radius = np.meshgrid(angle, radius)
    disk_x = disk_radius * np.cos(disk_angle)
    disk_y = disk_radius * np.sin(disk_angle)
    axes.plot_surface(disk_x, disk_y, np.zeros_like(disk_x), color="#54a24b", alpha=0.55, linewidth=0.0)
    axes.plot_surface(disk_x, disk_y, disk_y, color="#e45756", alpha=0.55, linewidth=0.0)

    wall_side_y, wall_side_z = np.meshgrid(np.linspace(0.0, 1.0, 31), np.linspace(0.0, 1.0, 31))
    keep = wall_side_z <= np.minimum(wall_side_y, np.sqrt(np.maximum(0.0, 1.0 - wall_side_y**2)))
    axes.plot_surface(
        np.zeros_like(wall_side_y),
        np.where(keep, wall_side_y, np.nan),
        np.where(keep, wall_side_z, np.nan),
        color="#b279a2",
        alpha=0.55,
        linewidth=0.0,
    )
    axes.plot(cosine, sine, np.zeros_like(angle), color="#1f1f1f", linewidth=1.6)
    axes.plot(
        [math.cos(math.pi / 4)] * 2,
        [math.sin(math.pi / 4)] * 2,
        [0.0, math.sin(math.pi / 4)],
        color="#1f1f1f",
        linewidth=1.2,
        linestyle=":",
    )
    for text, point in SURFACE_LABELS:
        axes.text(point[0], point[1], point[2], text, fontsize=11, color="#1f1f1f")
    axes.set_xlim(0.0, 1.05)
    axes.set_ylim(0.0, 1.05)
    axes.set_zlim(0.0, 1.05)
    axes.set_xlabel("$x$")
    axes.set_ylabel("$y$")
    axes.set_zlabel("$z$")
    axes.set_title("The solid $E$ in the first octant", fontsize=12)
    axes.view_init(elev=24.0, azim=-52.0)


def draw_section(axes: plt.Axes) -> None:
    """Draw the section of E at the fixed x of the module."""
    outer = region.outer_radius(SECTION_X)
    vertices = region.triangle_vertices(outer)
    polygon = np.array(vertices + [vertices[0]])
    axes.fill(polygon[:, 0], polygon[:, 1], color="#4c78a8", alpha=0.35, linewidth=0.0)
    axes.plot(polygon[:, 0], polygon[:, 1], color="#1f1f1f", linewidth=1.6)
    axes.plot([outer * 0.45] * 2, [0.0, outer * 0.45], color="#e45756", linewidth=1.8)
    axes.annotate(
        "$z$ runs from $0$ to $y$",
        xy=(outer * 0.45, outer * 0.22),
        xytext=(outer * 0.10, outer * 0.80),
        fontsize=10,
        arrowprops={"arrowstyle": "-|>", "color": "#e45756", "shrinkB": 6.0},
    )
    axes.text(outer * 0.10, outer * 0.08, "$(0,0)$", fontsize=10)
    axes.text(outer * 0.55, -0.09 * outer, "$(Y,0)$", fontsize=10)
    axes.text(outer * 0.80, outer * 0.93, "$(Y,Y)$", fontsize=10)
    axes.set_xlim(-0.10 * outer, 1.28 * outer)
    axes.set_ylim(-0.16 * outer, 1.22 * outer)
    axes.set_xlabel("$y$")
    axes.set_ylabel("$z$")
    axes.set_aspect("equal")
    area = region.polygon_area(vertices)
    axes.set_title(
        f"Section at $x={SECTION_X}$, $Y=\\sqrt{{1-x^2}}={outer:.3f}$, area $Y^2/2={area:.4f}$",
        fontsize=10,
    )


def assert_inside_axes(figure: plt.Figure, axes: plt.Axes, name: str) -> None:
    """Assert that the legend and every text of one axes lie inside the axes box."""
    renderer = figure.canvas.get_renderer()
    axes_box = axes.get_window_extent(renderer=renderer)
    items: list[tuple[str, matplotlib.transforms.Bbox]] = []
    legend = axes.get_legend()
    if legend is not None:
        items.append(("legend", legend.get_window_extent(renderer=renderer)))
    for index, text in enumerate(axes.texts):
        items.append((f"text {index} {text.get_text()!r}", text.get_window_extent(renderer=renderer)))
    for label, box in items:
        inside = (
            box.x0 >= axes_box.x0
            and box.x1 <= axes_box.x1
            and box.y0 >= axes_box.y0
            and box.y1 <= axes_box.y1
        )
        print(f"[place] {name}: {label} inside the axes box: {inside}")
        if not inside:
            raise AssertionError(f"{name}: {label} leaves the axes box {axes_box} with {box}")


def main() -> None:
    """Draw both panels, check the label placement, and write the figure."""
    figure = plt.figure(figsize=(11.6, 4.8))
    solid_axes = figure.add_subplot(1, 2, 1, projection="3d")
    solid_axes.set_box_aspect((1.0, 1.0, 1.0))
    section_axes = figure.add_subplot(1, 2, 2)
    draw_solid(solid_axes)
    draw_section(section_axes)
    figure.tight_layout()
    figure.canvas.draw()
    assert_inside_axes(figure, section_axes, "section panel")
    region.FIGURE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    path = region.FIGURE_DIRECTORY / "part1_figure1.png"
    figure.savefig(path, dpi=170)
    print(f"[figure] wrote {path}")
    plt.close(figure)


if __name__ == "__main__":
    main()
